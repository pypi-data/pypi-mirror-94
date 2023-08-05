'''
Created on 13 Jan 2021

@author: jacklok
'''
from flask import Blueprint, render_template, request, Response, current_app
from flask_restful import Resource
from trexlib.utils.google.cloud_tasks_util import create_task
from trexanalytics import conf as analytics_conf
import logging
from trexlib.utils.log_util import get_tracelog
from trexlib.utils.string_util import random_string

logger = logging.getLogger('import')

class TriggerImportDataBaseResource(Resource):
    
    def output_html(self, content, code=200, headers=None):
        resp = Response(content, mimetype='text/html', headers=headers)
        resp.status_code = code
        return resp
    
    def post(self):
        return self.get()
    
    def get(self):
        try:
            task_url    = analytics_conf.UPSTREAM_BASE_URL + self.get_task_url()
            queue_name  = self.get_task_queue()
            payload     = self.get_data_payload()or {}
            
            logger.debug('task_url=%s', task_url)
            logger.debug('queue_name=%s', queue_name)
            logger.debug('payload=%s', payload)
            
            payload['batch_id'] = random_string(8, is_human_mistake_safe=True)
            
            create_task(task_url, queue_name, in_seconds=self.get_task_delay_in_seconds(), 
                        http_method = self.get_task_http_method(), payload=payload,
                        )
        except:
            logger.debug(get_tracelog())
        
        return self.output_html("Triggered task_url=%s"% (task_url))
    
    def get_task_url(self):
        pass
    
    def get_task_queue(self):
        pass
    
    def get_task_delay_in_seconds(self):
        return 1
    
    def get_task_http_method(self):
        return 'post'
        
    def get_data_payload(self):
        pass

class InitImportDataBaseResource(TriggerImportDataBaseResource):
    
    def post(self):
        return self.get()
    
    def get(self):
        content         = request.json or request.args or {}
        batch_id        = content.get('batch_id')
        
        data_payload    = self.get_data_payload() or {}
        task_url        = None
        
        logger.debug('InitImportDataBaseResource: data_payload=%s', data_payload)
        
        try:
            
            total_count     = self.get_import_data_count(**data_payload) or 0
            
            if total_count>0:
                try:
                    page_size   = self.get_import_data_page_size()
                    task_count  = int(total_count/page_size)
                    remaining   = total_count % page_size
                    
                    if remaining>0:
                        task_count = task_count +1
                        
                        
                    
                    payload = {
                                'task_count'    : task_count,
                                'total_count'   : total_count,
                                'task_index'    : 1,
                                'page_size'     : page_size, 
                                'batch_id'      : batch_id,
                                }
                    
                    if data_payload is not None:
                        payload.update(data_payload)
                    
                    
                    task_url    = self.get_task_url()
                    if task_url:
                        task_url    = analytics_conf.UPSTREAM_BASE_URL + task_url
                        queue_name  = self.get_task_queue()
                        
                        logger.debug('InitImportDataBaseResource: task_url=%s', task_url)
                        logger.debug('InitImportDataBaseResource: queue_name=%s', queue_name)
                        
                        create_task(task_url, queue_name, payload=payload, 
                                    in_seconds=self.get_task_delay_in_seconds(), 
                                    http_method = self.get_task_http_method(),
                                    )
                    
                        
                except:
                    logger.debug(get_tracelog())
                    return
        except:
            logger.error('Faield due to %s', get_tracelog()) 
        
        return self.output_html("Init %s" % task_url)
        
    
    def get_import_data_count(self, **kwargs):
        pass
    
    def get_import_data_page_size(self):
        pass
    
    def get_task_url(self):
        pass
    
    def get_task_queue(self):
        pass
    
    def get_task_http_method(self):
        return 'post'
    
class ImportDataBaseResource(InitImportDataBaseResource):    
    
    def get(self):
        content         = request.json or request.args or {}
        
        logger.debug('content=%s', content)
        logger.debug('***********************************************************')
        logger.debug('ImportDataBaseResource: content=%s', content)
        logger.debug('***********************************************************')
        
        
        task_count      = content.get('task_count')
        total_count     = content.get('total_count')
        task_index      = content.get('task_index')
        page_size       = content.get('page_size')
        start_cursor    = content.get('start_cursor')
        batch_id        = content.get('batch_id')
        
        data_payload    = self.get_data_payload() or {}
        
        data_payload.update(content)
        
        data_payload ['start_cursor'] = start_cursor 
        
        logger.debug('***********************************************************')
        logger.debug('ImportDataBaseResource: data_payload( %s- %d )=%s', batch_id, task_index, data_payload)
        logger.debug('***********************************************************')
        
        offset = 0
        if task_index>1:
            offset = (task_index-1) * page_size
        
        if task_index == task_count:
            #should complete here
            self.import_data(offset, page_size, **data_payload)
            
            logger.debug('Completed all import task')
            return self.output_html("Completed")
        
        elif task_index<task_count:
            #process import then pass to another task
            
            next_cursor         = self.import_data(offset, page_size, **data_payload)
            
            logger.debug('=========================== next_cursor=%s', next_cursor)
            
            existing_playload   = data_payload
            new_payload         = {
                                    'task_count'    : task_count,
                                    'total_count'   : total_count,
                                    'task_index'    : task_index + 1,
                                    'page_size'     : page_size, 
                                    'start_cursor'  : next_cursor,
                                    'batch_id'      : batch_id,
                                    }
            
            existing_playload.update(new_payload)
            
            logger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>> updated existing_playload=%s', existing_playload)
            
            task_url    = analytics_conf.UPSTREAM_BASE_URL + self.get_task_url()
            queue_name  = self.get_task_queue()
            
            logger.debug('ImportDataBaseResource: task_url=%s', task_url)
            logger.debug('ImportDataBaseResource: queue_name=%s', queue_name)
            
            create_task(task_url, queue_name, payload=existing_playload, 
                        in_seconds=self.get_task_delay_in_seconds(), 
                        http_method = self.get_task_http_method(),
                        )
            
            logger.debug('Completed partial import task, pass to next task')
            
            return self.output_html("Pass to next task")
    
    
    
    def import_data(self, offset, limit, **kwargs):
        pass
        