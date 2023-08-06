from mjango import db, query


class ExprCompiler(db.ExprCompiler):
    def compile(self, expr):
        try:
            return super().compile(expr)
        except NotImplementedError:
            return self.compile_generic(expr)

    def compile_generic(self, expr):
        return {expr.key: expr.value}

    def compile_nested(self, expr):
        result = {expr.key: {}}
        for value in expr.value:
            result[expr.key] = {**result[expr.key], **self.compile(value)}

        return result

    def compile_gte(self, expr):
        return {expr.key: {'$gte': expr.value}}

    def compile_lte(self, expr):
        return {expr.key: {'$lte': expr.value}}

    def compile_lt(self, expr):
        return {expr.key: {'$lt': expr.value}}

    def compile_gt(self, expr):
        return {expr.key: {'$gt': expr.value}}

    def compile_in(self, expr):
        if isinstance(expr.value, query.QuerySet):
            value = [model.get_pk_value() for model in expr.value]
        else:
            value = expr.value
        return {expr.key: {'$in': value}}

    def compile_ne(self, expr):
        return {expr.key: {'$ne': expr.value}}


class QueryCompiler(db.QueryCompiler):
    expr_compiler = ExprCompiler()

    def compile_and(self, query):
        result = self.compile_expr(query.expr)
        if query.sub_queries:
            for sub_query in query.sub_queries:
                result.append(self.compile(sub_query))
        return {
            '$and': result
        }

    def compile_or(self, query):
        result = []
        for key, value in self.compile_expr(query.expr).items():
            result.append({key: value})
        if query.sub_queries:
            for sub_query in query.sub_queries:
                result.append(self.compile(sub_query))

        return {
            '$or': result
        }

    def compile_empty(self, query):
        return {}
