# This module contains a class for interacting with the Handler collection in the MongoDB database.

import os
import datetime



class CrudStatuses:
    def __init__(self, mongo):
        self.mongo = mongo
        self.collection_name = 'aria_status'
        self.db_name = os.environ['ARIA_DATABASE']

    def insert_or_update(self, app_id, statuses):
        self.mongo.select_db_and_collection(self.db_name, collection_name=self.collection_name)

        now = datetime.datetime.now()

        # Find in DB if exists and was not modified today
        # Create or update if not exist
        status_in_db = self.mongo.find_one({
            "app_id": app_id,
            "updated_at": {"$lt": now.replace(hour=0, minute=0, second=0, microsecond=0)}
        }, {"_id": 1})

        if not status_in_db:
            self.mongo.insert_or_update(
                filter={"app_id": app_id},
                data={
                    "app_id": app_id,
                    "status": statuses,
                    "updated_at": now
                }
            )

    def get_statuses_by_app_id(self, app_id):
        self.mongo.select_db_and_collection(self.db_name, collection_name=self.collection_name)
        return self.mongo.find_one({"app_id": app_id})
