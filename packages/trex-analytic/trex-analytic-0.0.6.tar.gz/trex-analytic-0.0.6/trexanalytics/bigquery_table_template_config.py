'''
Created on 11 Jan 2021

@author: jacklok
'''
from google.cloud import bigquery


__REGISTERED_USER_SCHEMA = {
                        
                            #customer key
                            bigquery.SchemaField('Key', 'STRING'),
                            bigquery.SchemaField('UserKey', 'STRING'),
                            bigquery.SchemaField('DOB', 'DATE'),
                            bigquery.SchemaField('Gender', 'STRING'),
                            bigquery.SchemaField('MobilePhone', 'STRING'),
                            bigquery.SchemaField('Email', 'STRING'),
                            bigquery.SchemaField('MobileAppDownload', 'BOOLEAN'),
                            bigquery.SchemaField('RegisteredDateTime', 'DATETIME'),
                            bigquery.SchemaField('UpdatedDateTime', 'DATETIME'),
                            }

__REGISTERED_CUSTOMER_SCHEMA = {
                        
                            #customer key
                            bigquery.SchemaField('Key', 'STRING'),
                            bigquery.SchemaField('UserKey', 'STRING'),
                            bigquery.SchemaField('CustomerKey', 'STRING'),
                            bigquery.SchemaField('MerchantKey', 'STRING'),
                            bigquery.SchemaField('DOB', 'DATE'),
                            bigquery.SchemaField('Gender', 'STRING'),
                            bigquery.SchemaField('MobilePhone', 'STRING'),
                            bigquery.SchemaField('Email', 'STRING'),
                            bigquery.SchemaField('MobileAppInstall', 'BOOLEAN'),
                            bigquery.SchemaField('RegisteredDateTime', 'DATETIME'),
                            bigquery.SchemaField('RegisteredOutlet', 'STRING'),
                            bigquery.SchemaField('UpdatedDateTime', 'DATETIME'),
                            }

__MERCHANT_REGISTERED_CUSTOMER_SCHEMA = {
                        
                            #customer key
                            bigquery.SchemaField('Key', 'STRING'),
                            bigquery.SchemaField('UserKey', 'STRING'),
                            bigquery.SchemaField('CustomerKey', 'STRING'),
                            bigquery.SchemaField('DOB', 'DATE'),
                            bigquery.SchemaField('Gender', 'STRING'),
                            bigquery.SchemaField('MobilePhone', 'STRING'),
                            bigquery.SchemaField('Email', 'STRING'),
                            bigquery.SchemaField('MobileAppInstall', 'BOOLEAN'),
                            bigquery.SchemaField('RegisteredDateTime', 'DATETIME'),
                            bigquery.SchemaField('RegisteredOutlet', 'STRING'),
                            bigquery.SchemaField('UpdatedDateTime', 'DATETIME'),
                            }

__REGISTERED_MERCHANT_SCHEMA = {
                        
                            #customer key
                            bigquery.SchemaField('Key', 'STRING'),
                            bigquery.SchemaField('MerchantKey', 'STRING'),
                            bigquery.SchemaField('CompanyName', 'STRING'),
                            bigquery.SchemaField('RegisteredDateTime', 'DATETIME'),
                            bigquery.SchemaField('UpdatedDateTime', 'DATETIME'),
                            }
    

REGISTERED_USER_TEMPLATE                    = 'registered_user'
REGISTERED_CUSTOMER_TEMPLATE                = 'registered_customer'
REGISTERED_MERCHANT_TEMPLATE                = 'registered_merchant'
MERCHANT_REGISTERED_CUSTOMER_TEMPLATE       = 'merchant_registered_customer'
    

TABLE_SCHEME_TEMPLATE = {
                    REGISTERED_USER_TEMPLATE                :  __REGISTERED_USER_SCHEMA,
                    REGISTERED_CUSTOMER_TEMPLATE            :  __REGISTERED_CUSTOMER_SCHEMA,
                    REGISTERED_MERCHANT_TEMPLATE            :  __REGISTERED_MERCHANT_SCHEMA,
                    MERCHANT_REGISTERED_CUSTOMER_TEMPLATE   : __MERCHANT_REGISTERED_CUSTOMER_SCHEMA,
    }
