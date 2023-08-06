from typing import Optional, Any, Union, List
from pymongo import MongoClient, ReturnDocument
from pymongo.cursor import Cursor
from pymongo.results import UpdateResult, DeleteResult
from mjango import db_settings
from mjango.exceptions import InstanceNotFound, SettingsError
from mjango.db import BaseDB
from mjango.settings import Settings
from mjango.mongodb.compilers import QueryCompiler

mongo_clients = {}


def connect(db_host: str) -> MongoClient:
    try:
        return mongo_clients[db_host]
    except KeyError:
        mongo_clients[db_host] = MongoClient(db_host)
        return mongo_clients[db_host]


class MongoBase:
    def __init__(self,
                 collection: str,
                 settings: Optional[Settings] = None) -> None:
        self.collection = collection
        self.settings = settings or db_settings

    @property
    def db_host(self) -> str:
        if not self.settings.db_host:
            raise SettingsError
        return self.settings.db_host

    @property
    def db_name(self) -> str:
        return self.settings.db_name

    @property
    def client(self) -> MongoClient:
        client = connect(self.db_host)
        return client[self.db_name][self.collection]

    def filter(self,
               query: dict,
               skip: int = 0,
               limit: int = 0,
               projection: Optional[dict] = None) -> Cursor:
        return self.client.find(query,
                                skip=skip,
                                limit=limit,
                                projection=projection)

    def get(self, query: dict) -> dict:
        return self.client.find_one(query)

    def create(self, **kwargs: Any) -> dict:
        self.client.insert_one(kwargs)
        return kwargs

    def delete(self, query: dict) -> None:
        self.client.find_one_and_delete(query)

    def update(self, query: dict, data: dict) -> dict:
        return self.client.find_one_and_update(query, {'$set': data}, return_document=ReturnDocument.AFTER)

    def count(self, query: dict) -> int:
        return self.client.count_documents(query)

    def batch_update(self, query: dict, data: dict) -> UpdateResult:
        return self.client.update_many(query, {'$set': data})

    def batch_delete(self, query: dict) -> DeleteResult:
        return self.client.delete_many(query)


class MongoDB(BaseDB):
    query_compiler = QueryCompiler()

    def __init__(self,
                 collection: str,
                 settings: Optional[Settings] = None) -> None:
        self.db_base = MongoBase(collection, settings)

    def create(self, **kwargs: Any) -> dict:
        return self.db_base.create(**kwargs)

    def filter(self,
               query: dict,
               skip: int = 0,
               limit: int = 0,
               projection: Union[List[str], dict, None] = None) -> Cursor:
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

    def count(self, query: dict) -> int:
        return self.db_base.count(query)

    def update(self, query: dict, data: dict) -> dict:
        return self.db_base.update(query, data=data)

    def delete(self, query: dict) -> None:
        return self.db_base.delete(query)

    def all(self) -> Cursor:
        return self.db_base.filter({})

    def get(self, query: dict) -> dict:
        result = self.db_base.get(query)
        if not result:
            raise InstanceNotFound
        return result

    def batch_update(self, query: dict, data: dict) -> dict:
        result = self.db_base.batch_update(query, data=data)
        return {'count': result.matched_count, 'data': data}

    def batch_delete(self, query: dict) -> dict:
        result = self.db_base.batch_delete(query)
        return {'count': result.deleted_count}
