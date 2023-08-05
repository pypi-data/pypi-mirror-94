'''
Created on 18 Jan 2021

@author: jacklok
'''
from flask import Blueprint
import logging
from trexlib.utils.google.bigquery_util import process_job_result_into_category_and_count, execute_query
from trexanalytics.controllers.bigquery.query_base_routes import CategoryAndCountQueryBaseResource
from flask_restful import Api
from trexanalytics.conf import BIGQUERY_GCLOUD_PROJECT_ID, SYSTEM_DATASET, MERCHANT_DATASET


query_customer_data_bp = Blueprint('query_customer_data_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/biqquery/customer')

logger = logging.getLogger('debug')

query_customer_data_api = Api(query_customer_data_bp)

@query_customer_data_bp.route('/index')
def query_customer_index(): 
    return 'ping', 200


class QueryAllCustomerGrowthByYearMonth(CategoryAndCountQueryBaseResource):
    def prepare_query(self, **kwrgs):
        
        year_month_from   = kwrgs.get('year_month_from')
        year_month_to     = kwrgs.get('year_month_to')
        
        where_condition  = ''
        
        if year_month_from and year_month_to:
            where_condition = "WHERE _TABLE_SUFFIX BETWEEN '{year_month_from}' and '{year_month_to}'".format(year_month_from=year_month_from, 
                                                                                                         year_month_to=year_month_to)
        
        query = '''
            SELECT FORMAT_DATETIME('%Y-%m', RegisteredDateTime) as year_month, sum(count_by_date) as count
            FROM (
            SELECT RegisteredDateTime, count(*) as count_by_date FROM
                (
                        SELECT CustomerKey, RegisteredDateTime
                        FROM `{project_id}.{dataset_name}.registered_customer_*`
                        {where_condition}
                        GROUP BY CustomerKey, RegisteredDateTime
                ) GROUP BY RegisteredDateTime       
            ) GROUP BY year_month            
            '''.format(project_id=BIGQUERY_GCLOUD_PROJECT_ID, dataset_name=SYSTEM_DATASET, where_condition=where_condition)    
            
        logger.debug('execute_all_registered_customer_by_year_month: query=%s', query)
    
        return query 
    
class QueryMerchantCustomerGrowthByYearMonth(CategoryAndCountQueryBaseResource):
    def prepare_query(self, **kwrgs):
        account_code      = kwrgs.get('account_code')
        year_month_from   = kwrgs.get('year_month_from')
        year_month_to     = kwrgs.get('year_month_to')
        
        account_code = account_code.replace('-','')
        
        where_condition  = ''
        
        if year_month_from and year_month_to:
            where_condition = "WHERE _TABLE_SUFFIX BETWEEN '{year_month_from}' and '{year_month_to}'".format(year_month_from=year_month_from, 
                                                                                                         year_month_to=year_month_to)
        
        query = '''
            SELECT FORMAT_DATETIME('%Y-%m', RegisteredDateTime) as year_month, sum(count_by_date) as count
            FROM (
            SELECT RegisteredDateTime, count(*) as count_by_date FROM
                (
                        SELECT CustomerKey, RegisteredDateTime
                        FROM `{project_id}.{dataset_name}.merchant_registered_customer_{account_code}_*`
                        {where_condition}
                        GROUP BY CustomerKey, RegisteredDateTime
                ) GROUP BY RegisteredDateTime       
            ) GROUP BY year_month            
            '''.format(project_id=BIGQUERY_GCLOUD_PROJECT_ID, dataset_name=MERCHANT_DATASET, where_condition=where_condition, account_code=account_code)    
            
        logger.debug('execute_all_registered_customer_by_year_month: query=%s', query)
    
        return query        
    

def execute_all_registered_customer_by_year_month(bg_client, project_id, dataset_name):
    
    query = '''
            SELECT FORMAT_DATETIME('%Y-%m-%d', RegisteredDateTime) as year_month, sum(count_by_date) as count
            FROM (
            SELECT RegisteredDateTime, count(*) as count_by_date
                        FROM `{project_id}.{dataset_name}.registered_customer_*`
                        GROUP BY RegisteredDateTime
            ) GROUP BY year_month            
            '''.format(project_id=project_id, dataset_name=dataset_name)
    
    logger.debug('execute_all_registered_customer_by_year_month: query=%s', query)
    
    return execute_query(bg_client, query)


def process_all_registered_customer_by_year_month(job_result_rows):
    return process_job_result_into_category_and_count(job_result_rows)

query_customer_data_api.add_resource(QueryAllCustomerGrowthByYearMonth,   '/all-customer-growth-by-year-month')
query_customer_data_api.add_resource(QueryMerchantCustomerGrowthByYearMonth,   '/merchant-customer-growth-by-year-month')
        
