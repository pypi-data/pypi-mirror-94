from __future__ import annotations
from typing import Optional, Union, List, Iterable, Any, TypeVar, Generic, TYPE_CHECKING
from mjango.operators import AND, OR, BaseOperator, EMPTY
from mjango.db import BaseDB, FILTER, GET, BATCH_UPDATE, BATCH_DELETE, COUNT
from mjango.exceptions import QueryError
from functools import reduce

if TYPE_CHECKING:
    from mjango.models import Model


class BaseIterable:
    def __init__(self, queryset: QuerySet) -> None:
        self.queryset = queryset


class ModelIterable(BaseIterable):
    def __iter__(self) -> None:
        db = self.queryset.db
        query = self.queryset.query
        method = self.queryset.method
        slicing = self.queryset.slicing
        kwargs = {}
        if slicing:
            kwargs['skip'] = slicing.start
            kwargs['limit'] = slicing.stop
        result = db.execute(query, method, **kwargs)
        for item in result:
            yield (self.queryset.model(item))


class ValuesIterable(BaseIterable):
    def __iter__(self) -> None:
        db = self.queryset.db
        query = self.queryset.query
        method = self.queryset.method
        slicing = self.queryset.slicing
        projection = self.queryset.projection
        kwargs = {'projection': projection}
        if slicing:
            kwargs['skip'] = slicing.start
            kwargs['limit'] = slicing.stop
        result = db.execute(query, method, **kwargs)
        return iter(result)


class QuerySet:
    def __init__(self,
                 model: Model,
                 db: Optional[BaseDB] = None,
                 method: Optional[str] = None,
                 query: Optional[BaseOperator] = None,
                 slicing: Union[slice, int, None] = None,
                 iter_class: BaseIterable = ModelIterable,
                 projection: Optional[List[str]] = None) -> None:

        self.model = model
        self.db = db or model.db
        self.method = method
        self.slicing = slicing
        self.projection = projection
        self._query = query or EMPTY()
        self._cached_result = None
        self._iter_class = iter_class or ModelIterable

    @property
    def query(self) -> BaseOperator:
        return self._query

    def _fetch_all(self) -> None:
        if self._cached_result is None:
            self._cached_result = list(self._iter_class(self))

    def __iter__(self) -> Iterable[Model]:
        self._fetch_all()
        return iter(self._cached_result)

    def __getitem__(self,
                    slicing: Union[slice, int, None]) -> Union[QuerySet,
                                                               Model]:
        if isinstance(slicing, int):
            self._fetch_all()
            return self._cached_result[slicing]
        query = self.query.copy()
        return self._clone(query,
                           method=self.method,
                           iter_class=self._iter_class,
                           slicing=slicing)

    def __len__(self) -> int:
        return self.count()

    def __bool__(self) -> bool:
        self._fetch_all()
        return bool(self._cached_result)

    def _make_query(self,
                    *query: BaseOperator,
                    **kwargs: Any) -> BaseOperator:
        kwargs_q = AND(**kwargs)
        query_queue = [*query, kwargs_q]
        if self._query:
            query_queue.append(self._query)
        query = reduce(lambda x, y: x & y, query_queue)
        return query.copy()

    def _clone(self,
               query: BaseOperator,
               method: Optional[str] = None,
               iter_class: Optional[BaseOperator] = None,
               slicing: Union[slice, int, None] = None,
               projection: List[str] = None) -> QuerySet:
        if not method:
            method = self.method
        queryset = self.__class__(
            self.model,
            db=self.db,
            method=method,
            query=query,
            iter_class=iter_class,
            slicing=slicing,
            projection=projection)
        return queryset

    def filter(self, *query: BaseOperator, **kwargs: Any) -> QuerySet:
        if self.slicing:
            raise QueryError(
                'not able to filter with sliced queryset')
        query = self._make_query(*query, **kwargs)
        return self._clone(query, method=FILTER)

    def values(self, *args: str) -> QuerySet:
        return self._clone(self._query,
                           iter_class=ValuesIterable,
                           projection=args)

    def get(self, *query: BaseOperator, **kwargs: Any) -> Model:
        query = self._make_query(*query, **kwargs)
        result = self.db.execute(query, GET)
        return self.model(result)

    def create(self, **kwargs: Any) -> Model:
        if self.query:
            raise QueryError(
                'queryset does not support create() after first query')
        result = self.db.create(**kwargs)
        return self.model(result)

    def update(self, **kwargs: Any) -> dict:
        if not self.query:
            raise QueryError(
                'queryset does not support update() before first query')
        result = self.db.execute(
            self.query, BATCH_UPDATE, data=kwargs)
        return result

    def count(self) -> int:
        return self.db.execute(self.query, COUNT)

    def all(self) -> QuerySet:
        if self.query:
            raise QueryError(
                'queryset does not support all() after first query')
        return self._clone(EMPTY(), FILTER)

    def delete(self) -> dict:
        if self.query:
            raise QueryError(
                'queryset does not support delete() before first query')

        return self.db.execute(self.query, BATCH_DELETE)
