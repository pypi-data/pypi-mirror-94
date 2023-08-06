from __future__ import annotations
from typing import Any, List
from mjango.operators import BaseOperator
from mjango.expressions import BaseExpression

FILTER = 'filter'
GET = 'get'
CREATE = 'create'
DELETE = 'delete'
UPDATE = 'update'
BATCH_UPDATE = 'batch_update'
BATCH_DELETE = 'batch_delete'
COUNT = 'count'


class BaseDB:
    query_compiler: QueryCompiler

    def create(self, **kwargs: Any) -> dict:
        raise NotImplementedError('create() should be implement')

    def filter(self, query: BaseOperator) -> List[Any]:
        raise NotImplementedError('filter() should be implement')

    def update(self, query: BaseOperator, data: dict) -> dict:
        raise NotImplementedError('update() should be implement')

    def delete(self, query: BaseOperator) -> dict:
        raise NotImplementedError('delete() should be implement')

    def execute(self,
                query: BaseOperator,
                method_name: str,
                **kwargs: Any) -> Any:
        method = getattr(self, method_name)
        compiled = self.query_compiler.compile(query)
        result = method(compiled, **kwargs)
        return result


class QueryCompiler:
    expr_compiler: ExprCompiler

    def compile_expr(self, exprs: BaseExpression) -> Any:
        return [self.expr_compiler.compile(expr) for expr in exprs]

    def compile(self, query: BaseOperator) -> Any:
        methname = 'compile_' + query.__class__.__name__.lower()
        method = getattr(self, methname, None)
        if not method:
            raise NotImplementedError(f'{methname}() should be implemented')
        return method(query)


class ExprCompiler:
    def compile(self, expr: BaseExpression) -> Any:
        methname = 'compile_' + expr.__class__.__name__.lower()
        method = getattr(self, methname, None)
        if not method:
            raise NotImplementedError(f'{methname}() should be implemented')
        return method(expr)
