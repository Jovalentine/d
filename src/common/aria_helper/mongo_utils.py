import pymongo

class Mongo:
    def __init__(self, mongo_uri):
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.col = ''

    def select_db_and_collection(self, db_name, collection_name):
        self.db = self.client[db_name]
        self.col = self.db.get_collection(collection_name)

    def insert_one(self, data):
        self.col.insert_one(data)
        
    def insert_many(self, data):
        self.col.insert_many(data)
        
    def update_one(self, filter, data, *args, **kwargs):
        self.col.update_one(filter, data, *args, **kwargs)
        
    def update_many(self, filter, data, *args, **kwargs):
        self.col.update_many(filter, data, *args, **kwargs)
        
    def find_one(self, filter, *args, **kwargs):
        return self.col.find_one(filter, *args, **kwargs)
    
    def insert_or_update(self, filter, data):
        x = self.find_one(filter)
        if x:
            self.update_one(filter, {'$set': data})
        else:
            self.insert_one(data)

    def close_connection(self):
        self.client.close()
