from __future__ import annotations
from typing import TypeVar, Generic, Any
import copy
from mjango.expressions import build_expr_obj


class BaseOperator:
    def __init__(self, *args: BaseOperator, **kwargs: Any) -> None:
        self.sub_queries = args
        self.expr = []

        if not all([isinstance(query, BaseOperator) for query in self.sub_queries]):
            raise TypeError('args should be instanceof BaseOperator')

        for key, value in kwargs.items():
            expr_class = build_expr_obj(key, value)
            self.expr.append(expr_class)

    def __and__(self, other: BaseOperator) -> BaseOperator:
        return AND(self, other)

    def __or__(self, other: BaseOperator) -> BaseOperator:
        return OR(self, other)

    def copy(self) -> BaseOperator:
        return copy.deepcopy(self)


class EMPTY(BaseOperator):
    def __init__(self):
        pass

    def __bool__(self):
        return False


class AND(BaseOperator):
    pass


class OR(BaseOperator):
    pass


class NOR(BaseOperator):
    pass


class NOT(BaseOperator):
    pass
