# This module contains a class for interacting with the Handler collection in the MongoDB database.

import os
import datetime


class CrudHandler:
    def __init__(self, mongo):
        self.mongo = mongo
        self.collection_name='handler'
        self.db_name = os.environ['ARIA_DATABASE']


    def insert_execution(self, request, next_function, failed=False, error_message=None):
        self.mongo.select_db_and_collection(self.db_name, collection_name=self.collection_name)
        execution_id = datetime.datetime.now().strftime("%m%d%Y_%H%M%S%f")
        status_from_id = request.get('action', {}).get('source_status')
        status_to_id = request.get('action', {}).get('target_status')
        handler_data = {
            "execution_id": execution_id,
            "aria_wi_id": request.get('document', {}).get('id'),
            "app_id": request.get('document', {}).get('app_id'),
            "user_id": request.get('document', {}).get('aria_assigned_to'),
            "user_name": request.get('document', {}).get('aria_user'),
            "action_id": request.get('action', {}).get('action_id'),
            "action_name": request.get('action', {}).get('action_label'),
            "status_from": request.get('status', {}).get(status_from_id, {}).get('label'),
            "status_from_id": status_from_id,
            "status_to": request.get('status', {}).get(status_to_id, {}).get('label'),
            "status_to_id": status_to_id,
            "next_function": next_function,
            "status": "Pending" if not failed else "Failed",
            "error_message": error_message
        }
        self.mongo.insert_one(handler_data)
        return execution_id
    
    def mark_as_failed(self, execution_id, error_message=None):
        self.mongo.select_db_and_collection(self.db_name, collection_name=self.collection_name)
        self.mongo.update_one(
            filter={"execution_id": execution_id},
            data={"$set": {"status": "Failed", "error_message": error_message}}
        )

    def mark_as_completed(self, execution_id):
        self.mongo.select_db_and_collection(self.db_name, collection_name=self.collection_name)
        self.mongo.update_one(
            filter={"execution_id": execution_id},
            data={"$set": {"status": "Completed"}}
        )
