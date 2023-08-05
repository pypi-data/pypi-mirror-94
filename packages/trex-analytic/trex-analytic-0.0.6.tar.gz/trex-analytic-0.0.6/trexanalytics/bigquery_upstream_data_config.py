'''
Created on 26 Jan 2021

@author: jacklok
'''
from trexanalytics.conf import UPSTREAM_UPDATED_DATETIME_FIELD_NAME, MERCHANT_DATASET, SYSTEM_DATASET
import uuid, logging
from trexmodel.models.datastore.analytic_models import UpstreamData
from trexanalytics.bigquery_table_template_config import REGISTERED_CUSTOMER_TEMPLATE, REGISTERED_MERCHANT_TEMPLATE, MERCHANT_REGISTERED_CUSTOMER_TEMPLATE 
from trexlib.utils.google.bigquery_util import default_serializable
from datetime import datetime

__REGISTERED_MERCHANT_TEMPLATE_UPSTREAM_SCHEMA = { 
                                                'MerchantKey'           : 'key_in_str',
                                                'CompanyName'           : 'company_name',
                                                'RegisteredDateTime'    : 'registered_datetime',
                                            }

__REGISTERED_CUSTOMER_TEMPLATE_UPSTREAM_SCHEMA = {
                                                'UserKey'           : 'registered_user_acct_key',
                                                'CustomerKey'       : 'key_in_str',
                                                'MerchantKey'       : 'registered_merchant_acct_key',
                                                'DOB'               : 'birth_date',
                                                'Gender'            : 'gender',
                                                'MobilePhone'       : 'mobile_phone',
                                                'Email'             : 'email',
                                                'MobileAppInstall'  : 'mobile_app_installed',
                                                'RegisteredDateTime': 'registered_datetime',
                                                'RegisteredOutlet'  : 'registered_outlet_key',
                                                }

__MERCHANT_REGISTERED_CUSTOMER_TEMPLATE_UPSTREAM_SCHEMA = {
                                                        'UserKey'           : 'registered_user_acct_key',
                                                        'CustomerKey'       : 'key_in_str',
                                                        'DOB'               : 'birth_date',
                                                        'Gender'            : 'gender',
                                                        'MobilePhone'       : 'mobile_phone',
                                                        'Email'             : 'email',
                                                        'MobileAppInstall'  : 'mobile_app_installed',
                                                        'RegisteredDateTime': 'registered_datetime',
                                                        'RegisteredOutlet'  : 'registered_outlet_key',
                                                        }

upstream_schema_config = {
                            REGISTERED_MERCHANT_TEMPLATE            : __REGISTERED_MERCHANT_TEMPLATE_UPSTREAM_SCHEMA,
                            REGISTERED_CUSTOMER_TEMPLATE            : __REGISTERED_CUSTOMER_TEMPLATE_UPSTREAM_SCHEMA,
                            MERCHANT_REGISTERED_CUSTOMER_TEMPLATE   : __MERCHANT_REGISTERED_CUSTOMER_TEMPLATE_UPSTREAM_SCHEMA
                            
                            }

logger = logging.getLogger('upstream')

def __create_upstream(upstream_entity, upstream_template, dataset_name, table_name, update_datetime=None):
    upstream_json = {}
    if upstream_entity:
        schema = upstream_schema_config.get(upstream_template)
        for upstrem_field_name, attr_name in schema.items():
            upstream_json[upstrem_field_name] = default_serializable(getattr(upstream_entity, attr_name))
    
    if update_datetime is None:
        update_datetime = datetime.now()
            
    upstream_json['Key'] = uuid.uuid1().hex
    upstream_json[UPSTREAM_UPDATED_DATETIME_FIELD_NAME] = default_serializable(update_datetime)
    logger.debug('-------------------------------------------------')
    logger.debug('upstream_json=%s', upstream_json)
    logger.debug('-------------------------------------------------')
    UpstreamData.create(dataset_name, table_name, upstream_template, [upstream_json])
    

def create_registered_customer_upstream_for_system(customer):
    update_datetime     = datetime.now()
    table_name          = REGISTERED_CUSTOMER_TEMPLATE
    final_table_name    = '{}_{}'.format(table_name, update_datetime.strftime('%Y%m%d'))
    
    __create_upstream(customer, REGISTERED_CUSTOMER_TEMPLATE, SYSTEM_DATASET, final_table_name, update_datetime=update_datetime)
    
def create_merchant_registered_customer_upstream_for_merchant(customer):
    update_datetime     = datetime.now()
    table_name          = MERCHANT_REGISTERED_CUSTOMER_TEMPLATE
    merchant_acct       = customer.registered_merchant_acct
    account_code        = merchant_acct.account_code.replace('-','')
    final_table_name    = '{}_{}_{}'.format(table_name, account_code, update_datetime.strftime('%Y%m%d'))
    
    __create_upstream(customer, MERCHANT_REGISTERED_CUSTOMER_TEMPLATE, MERCHANT_DATASET, final_table_name, update_datetime=update_datetime)    
    




