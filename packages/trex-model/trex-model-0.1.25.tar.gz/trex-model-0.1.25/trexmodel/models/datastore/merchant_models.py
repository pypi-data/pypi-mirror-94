'''
Created on 15 May 2020

@author: jacklok
'''

from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel, FullTextSearchable
from trexmodel.models.datastore.system_models import SentEmail
from trexmodel.models.datastore.user_models import UserMin
import trexmodel.conf as model_conf
from trexlib.utils.security_util import generate_user_id, hash_password
from trexlib.utils.string_util import random_number
import logging
from datetime import datetime, timedelta
from trexlib.utils.common.date_util import parse_datetime
from trexmodel import conf
from google.auth._default import default


logger = logging.getLogger('model')

class MerchantMin(BaseNModel, DictModel, FullTextSearchable):
    
    company_name            = ndb.StringProperty(required=True)
    contact_name            = ndb.StringProperty(required=False)
    address                 = ndb.StringProperty(required=False)
    office_phone            = ndb.StringProperty(required=False)
    mobile_phone            = ndb.StringProperty(required=False)
    fax_phone               = ndb.StringProperty(required=False)
    email                   = ndb.StringProperty(required=False)
    status                  = ndb.StringProperty(required=False)
    
    modified_datetime       = ndb.DateTimeProperty(required=True, auto_now=True)
    registered_datetime     = ndb.DateTimeProperty(required=True, auto_now_add=True)
    plan_start_date         = ndb.DateProperty(required=True)
    plan_end_date           = ndb.DateProperty(required=True)
    
    fulltextsearch_field_name   = 'company_name'
    
    

class MerchantAcct(MerchantMin):
    account_code                = ndb.StringProperty(required=False)
    logo_public_url             = ndb.StringProperty(required=False)
    logo_storage_filename       = ndb.StringProperty(required=False)
    dashboard_stat_figure       = ndb.JsonProperty()
    currency_code               = ndb.StringProperty(required=False, default='myr')
    
    stat_figure_update_interval_in_minutes  = conf.MERCHANT_STAT_FIGURE_UPDATE_INTERVAL_IN_MINUTES
    stat_figure_update_datetime_format      = '%d-%m-%Y %H:%M:%S'
    
    dict_properties = ['company_name', 'contact_name', 'mobile_phone', 'office_phone', 'fax_phone', 'email', 'account_code', 
                       'registered_datetime', 'modified_datetime', 'plan_start_date', 'plan_end_date', 'currency_code']
    
    def update_stat_details(self, stat_dict):
        dashboard_stat_figure = self.dashboard_stat_figure
        logger.debug('update_stat_figure: dashboard_stat_figure=%s', dashboard_stat_figure)
        
        next_updated_datetime = datetime.now() + timedelta(minutes=int(self.stat_figure_update_interval_in_minutes))
        
        logger.debug('update_stat_figure: next_updated_datetime=%s', next_updated_datetime)
        
        dashboard_stat_figure = {
                                'next_updated_datetime' : next_updated_datetime.strftime(self.stat_figure_update_datetime_format),
                                'stat_details'          : stat_dict,
                             }
            
        self.dashboard_stat_figure = dashboard_stat_figure
        self.put()
    
    def get_stat_details(self):
        dashboard_stat_figure = self.dashboard_stat_figure
        
        logger.debug('get_stat_figure: dashboard_stat_figure=%s', dashboard_stat_figure)
        
        if dashboard_stat_figure is not None and dashboard_stat_figure.get('next_updated_datetime'):
            next_updated_datetime = dashboard_stat_figure.get('next_updated_datetime')
            
            logger.debug('get_stat_figure: next_updated_datetime=%s', next_updated_datetime)
            
            if next_updated_datetime:
                next_updated_datetime = datetime.strptime(next_updated_datetime, self.stat_figure_update_datetime_format)
                now = datetime.now()
                if now > next_updated_datetime:
                    return None
                else:
                    return dashboard_stat_figure.get('stat_details')
        
        return None
    
    @staticmethod
    def create(company_name=None, contact_name=None, email=None, mobile_phone=None, office_phone=None, plan_start_date=None, plan_end_date=None, 
               account_code=None, currency_code=None):
        
        if account_code is None:
            account_code    = "%s-%s-%s-%s" % (random_number(4),random_number(4),random_number(4),random_number(4))
            
        merchant_acct   = MerchantAcct(
                                       company_name     = company_name, 
                                       contact_name     = contact_name,
                                       email            = email,
                                       mobile_phone     = mobile_phone,
                                       office_phone     = office_phone,
                                       plan_start_date  = plan_start_date, 
                                       plan_end_date    = plan_end_date,
                                       currency_code    = currency_code
                                       )
        
        logging.debug('account_code=%s', account_code)
        
        merchant_acct.account_code = account_code
        
        merchant_acct.put()
        
        return merchant_acct
    
    @staticmethod
    def get_by_account_code(account_code):
        return MerchantAcct.query(ndb.AND(MerchantAcct.account_code==account_code)).get()
        
    
    @staticmethod
    def list(offset=0, limit=10):
        return MerchantAcct.query().order(-MerchantAcct.registered_datetime).fetch(offset=offset, limit=limit)
    
    def delete_and_related(self):
        
        @ndb.transactional()
        def start_transaction(merchant_acct):
            merchant_user_key_list = MerchantUser.list_by_merchant_account(merchant_acct, keys_only=True)
            if merchant_user_key_list:
                ndb.delete_multi(merchant_user_key_list)
            
            merchant_acct.delete()
            logger.debug('after deleted merchant acct and merchant user')
            
        
        start_transaction(self)
        
class MerchantSentEmail(SentEmail):
    '''
    Merchant account as Ancestor
    '''
    pass

class MerchantUser(UserMin):
    
    '''
    parent is MerchantAcct
    '''
    username                = ndb.StringProperty(required=True)
    permission              = ndb.JsonProperty()
    is_admin                = ndb.BooleanProperty(required=True, default=False)
    
    dict_properties         = ['key', 'user_id', 'name', 'username', 'permission', 
                                'created_datetime', 'active', 'is_admin', 'permission', 
                                'is_super_user', 'is_admin_user', 'is_merchant_user']
    
    @property
    def is_super_user(self):
        return False
    
    @property
    def is_admin_user(self):
        return self.is_admin
    
    @property
    def is_merchant_user(self):
        return True
    
    @property
    def merchant_acct(self):
        return MerchantAcct.fetch(self.key.parent().urlsafe())
    
    @property
    def granted_outlet(self):
        return self.permission.get('granted_outlet')
    
    @property
    def granted_access(self):
        return self.permission.get('granted_access')
    
    @staticmethod
    def update_permission(merchant_user, access_permission, outlet_permission, is_admin=False):
        if access_permission is None:
            access_permission = []
            
        if outlet_permission is None:
            outlet_permission = []
            
        merchant_user.is_admin = is_admin
        merchant_user.permission = {'granted_access': access_permission, 'granted_outlet': outlet_permission}
        merchant_user.put()
    
    @staticmethod
    def create(merchant_acct=None, name=None, 
               username=None,
               password=None):
        
        check_unique_merchant_user = MerchantUser.get_by_username(username)
        
        if check_unique_merchant_user is None:
            user_id = generate_user_id()
            created_user = MerchantUser(
                                parent = merchant_acct.create_ndb_key(),
                                user_id=user_id, 
                                name=name, 
                                username=username
                                )
            
            hashed_password = hash_password(user_id, password)
            created_user.password = hashed_password
                
            created_user.put()
            
            return created_user
        else:
            raise Exception('Username have been used')
    
    @staticmethod
    def count_by_merchant_account(merchant_acct):
        condition_query = MerchantUser.query(ancestor = merchant_acct.create_ndb_key())
        return MerchantUser.count_with_condition_query(condition_query, limit=model_conf.MAX_FETCH_RECORD)  
    
    @staticmethod
    def list_by_merchant_account(merchant_acct, keys_only=False):
        return MerchantUser.query(ancestor = merchant_acct.create_ndb_key()).order(-MerchantUser.created_datetime).fetch(limit=model_conf.MAX_FETCH_RECORD, keys_only=keys_only)
    
    @staticmethod
    def list_all_by_merchant_account(merchant_acct, offset=None, start_cursor=None, return_with_cursor=False, keys_only=False, limit = model_conf.MAX_FETCH_RECORD):
        condition_query =  MerchantUser.query(ancestor = merchant_acct.create_ndb_key()).order(-MerchantUser.created_datetime)
        return MerchantUser.list_all_with_condition_query(
                                        condition_query, 
                                        offset=offset, 
                                        start_cursor=start_cursor, 
                                        return_with_cursor=return_with_cursor, 
                                        keys_only=keys_only, 
                                        limit=limit)
    
    @staticmethod
    def get_by_username(username):
        return MerchantUser.query(ndb.AND(MerchantUser.username==username)).get()
    
    
    @staticmethod
    def get_merchant_acct_by_merchant_user(merchant_user):
        return MerchantAcct.fetch(merchant_user.key.parent().urlsafe())
    
class Outlet(BaseNModel, DictModel, FullTextSearchable):
    merchant_acct           = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct)
    name                    = ndb.StringProperty(required=True)
    address                 = ndb.StringProperty(required=False)
    office_phone            = ndb.StringProperty(required=False)
    fax_phone               = ndb.StringProperty(required=False)
    email                   = ndb.StringProperty(required=False)
    business_hour           = ndb.StringProperty(required=False)
    is_physical_store       = ndb.BooleanProperty(required=False, default=True)
    geo_location            = ndb.GeoPtProperty(required=False)
    created_datetime        = ndb.DateTimeProperty(required=True, auto_now_add=True)
    
    searchable_field_name   = 'name'
    
    dict_properties         = ['key', 'name', 'address', 'office_phone', 
                                'fax_phone', 'email', 'business_hour', 'is_physical_store', 
                                'geo_location', 'created_datetime']
    
    @property
    def outlet_key(self):
        return self.key.urlsafe()
    
    @staticmethod
    def create(merchant_acct=None,name=None, address=None, email=None, fax_phone=None, 
               office_phone=None, business_hour=None, geo_location=None, is_physical_store=True):
        
        outlet   = Outlet(
                            parent              = merchant_acct.create_ndb_key(),
                            name                = name, 
                            address             = address,
                            email               = email,
                            fax_phone           = fax_phone,
                            office_phone        = office_phone,
                            business_hour       = business_hour,
                            geo_location        = geo_location,
                            is_physical_store   = is_physical_store,
                            )
        
        outlet.put()
        
        return outlet
    
    @staticmethod
    def list_by_merchant_acct(merchant_acct):
        return Outlet.query(ancestor = merchant_acct.create_ndb_key()).fetch(limit=model_conf.MAX_FETCH_RECORD)
    