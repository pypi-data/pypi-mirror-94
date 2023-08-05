import inspect
from mjango.query import QuerySet
from mjango.settings import Settings


class BaseManager:
    def __init__(self, model, db=None):
        self.model = model
        self.db = db or model.db
        self._query = None

    @classmethod
    def _get_queryset_methods(cls, queryset_class):
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
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            **cls._get_queryset_methods(queryset_class),
        })

    def get_queryset(self):
        return self._queryset_class(model=self.model)


class Manager(BaseManager.from_queryset(QuerySet)):
    def __call__(self, db_host=None, db_name=None):
        settings = Settings()
        settings.db_host = db_host or self.model._meta.settings.db_host
        settings.db_name = db_name or self.model._meta.settings.db_name
        db_instance = self.model._meta.db_class(settings)
        return Manager(self.model, db_instance)
