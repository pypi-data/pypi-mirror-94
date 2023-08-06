from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import inspect
from mjango.query import QuerySet
from mjango.settings import Settings, db_settings

if TYPE_CHECKING:
    from mjango.models import Model
    from mjango.db import BaseDB


class BaseManager:
    def __init__(self, model: Model, db: Optional[BaseDB] = None) -> None:
        self.model = model
        self.db = db or model.db
        self._query = None

    @classmethod
    def _get_queryset_methods(cls, queryset_class: QuerySet) -> dict:
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)

            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        new_methods = {}
        for name, method in inspect.getmembers(queryset_class, predicate=inspect.isfunction):
            # Only copy missing methods.
            if hasattr(cls, name):
                continue
            # Only copy public methods or methods with the attribute `queryset_only=False`.
            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None and name.startswith('_')):
                continue
            # Copy the method onto the manager.
            new_methods[name] = create_method(name, method)
        return new_methods

    @classmethod
    def from_queryset(cls,
                      queryset_class: QuerySet,
                      class_name: Optional[str] = None) -> BaseManager:
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            **cls._get_queryset_methods(queryset_class),
        })

    def get_queryset(self) -> QuerySet:
        return self._queryset_class(model=self.model, db=self.db)


class Manager(BaseManager.from_queryset(QuerySet)):
    def __call__(self,
                 db_host: Optional[str] = None,
                 db_name: Optional[str] = None) -> BaseManager:
        db_host = db_host or db_settings.db_host
        db_name = db_name or db_settings.db_name
        settings = Settings(db_host, db_name)
        db_instance = self.model._meta.db_class(
            self.model._meta.collection, settings)
        return Manager(self.model, db_instance)
