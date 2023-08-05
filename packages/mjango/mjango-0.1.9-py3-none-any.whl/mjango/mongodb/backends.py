from pymongo import MongoClient, ReturnDocument
from mjango import db, exceptions, db_settings
from mjango.mongodb.compilers import QueryCompiler

mongo_clients = {}


def connect(db_host):
    try:
        return mongo_clients[db_host]
    except KeyError as e:
        mongo_clients[db_host] = MongoClient(db_host)
        return mongo_clients[db_host]


class MongoBase:
    def __init__(self, collection, settings=None):
        self.collection = collection
        self.settings = settings or db_settings

    @property
    def db_host(self):
        if not self.settings.db_host:
            raise exceptions.SettingsError
        return self.settings.db_host

    @property
    def db_name(self):
        return self.settings.db_name

    @property
    def client(self):
        client = connect(self.db_host)
        return client[self.db_name][self.collection]

    def filter(self, query, skip, limit, projection):
        return self.client.find(query, skip=skip, limit=limit, projection=projection)

    def get(self, query):
        return self.client.find_one(query)

    def create(self, **kwargs):
        self.client.insert_one(kwargs)
        return kwargs

    def delete(self, query):
        self.client.find_one_and_delete(query)

    def update(self, query, data):
        return self.client.find_one_and_update(query, {'$set': data}, return_document=ReturnDocument.AFTER)

    def count(self, query):
        return self.client.count_documents(query)

    def batch_update(self, query, data):
        return self.client.update_many(query, {'$set': data})

    def batch_delete(self, query):
        return self.client.delete_many(query)


class MongoDB(db.BaseDB):
    query_compiler = QueryCompiler()

    def __init__(self, collection, settings=None):
        self.db_base = MongoBase(collection, settings)

    def create(self, **kwargs):
        return self.db_base.create(**kwargs)

    def filter(self, query, skip=0, limit=0, projection=None):
        skip = skip or 0
        limit = limit or 0
        if not projection:
            real_proj = None
        elif isinstance(projection, list):
            real_proj = {}
            for key in projection:
                real_proj[key] = 1
        else:
            real_proj = projection

        return self.db_base.filter(query, skip, limit, real_proj)

    def count(self, query):
        return self.db_base.count(query)

    def update(self, query, data):
        return self.db_base.update(query, data=data)

    def delete(self, query):
        return self.db_base.delete(query)

    def all(self):
        return self.db_base.filter({})

    def get(self, query):
        result = self.db_base.get(query)
        if not result:
            raise exceptions.InstanceNotFound
        return result

    def batch_update(self, query, data):
        result = self.db_base.batch_update(query, data=data)
        return {'count': result.matched_count, 'data': data}

    def batch_delete(self, query):
        result = self.db_base.batch_delete(query)
        return {'count': result.deleted_count}
