import requests
from mjango import db_settings, db
from mjango.manager import Manager
from mjango.operators import AND
from mjango.mongodb.backends import MongoDB
import copy


class ModelBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__

        meta = attrs.pop('Meta', None)
        parents = [b for b in bases if isinstance(b, ModelBase)]

        if not parents:
            attrs['_meta'] = meta
            return super_new(cls, name, bases, attrs)

        base_metas = [p._meta.__dict__.copy() for p in parents]
        for _meta in base_metas:
            for key, value in _meta.items():
                if not key.startswith('__') and not hasattr(meta, key):
                    setattr(meta, key, value)

        collection = meta.collection
        new_class = super_new(cls, name, bases, attrs)

        new_class.add_to_class('_meta', meta)
        new_class.add_to_class('_collection', meta.collection)
        new_class.add_to_class('db', meta.db_class(collection, meta.settings))
        new_class.add_to_class('pk', meta.default_pk)
        new_class.add_to_class('objects', Manager(new_class))

        return new_class

    def add_to_class(cls, name, attr):
        setattr(cls, name, attr)


class Model(metaclass=ModelBase):
    class Meta:
        db_class = MongoDB
        settings = db_settings
        default_pk = '_id'

    def __init__(self, data):
        self._data = data

    def __getattr__(self, key):
        try:
            return self._data[key]
        except KeyError as e:
            raise AttributeError(e)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return getattr(other, other.pk) == getattr(self, self.pk)
        raise TypeError('model compare should be same base class')

    def __setattr__(self, name, value):
        _setattr = super().__setattr__
        if name not in self.__dict__ and not name.startswith('_'):
            self._save(name, value)
        else:
            _setattr(name, value)

    def _save(self, key, value):
        self._data[key] = value

    def get_pk_value(self):
        return getattr(self, self.pk)

    def save(self):
        kwargs = {self.pk: getattr(self, self.pk)}
        query = AND(**kwargs)
        return self.db.execute(query, db.UPDATE, data=self._data)

    def delete(self):
        kwargs = {self.pk: getattr(self, self.pk)}
        query = AND(**kwargs)
        self.db.execute(query, db.DELETE)
        del self._data[self.pk]

    def to_json(self):
        return copy.deepcopy(self._data)
