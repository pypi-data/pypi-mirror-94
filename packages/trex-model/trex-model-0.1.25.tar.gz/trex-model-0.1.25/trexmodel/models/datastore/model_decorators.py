'''
Created on 27 Jan 2021

@author: jacklok
'''
import functools
from google.cloud import ndb
import logging

import time
logger = logging.getLogger('model')

def model_transactional(
        retries = 1,
        read_only=False,
        join=True,
        xg=True,
        propagation=None,
        desc=None):
    
    if desc is None:
        desc=''
    
    
    def transactional_wrapper(wrapped):
        @functools.wraps(wrapped)
        def transactional_inner_wrapper(*args, **kwargs):
            @ndb.transactional(retries=retries, read_only=read_only, join=join, xg=xg, propagation=propagation)
            def callback():
                start = time.time()
                try:
                    result =  wrapped(*args, **kwargs)
                except:
                    pass
                end = time.time()
                total_nanoseconds = int((end-start) * 1000000)
                logger.debug('-------------------{}--------------------------'.format(desc))
                logger.debug('transaction took %s nanoseconds', total_nanoseconds)
                logger.debug('----------------------------------------------------------')
                return result
            
            return callback()

        return transactional_inner_wrapper

    return transactional_wrapper
    
        
