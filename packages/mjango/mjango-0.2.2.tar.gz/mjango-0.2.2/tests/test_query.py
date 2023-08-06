from mjango import operators, db_settings
from mjango.query import QuerySet
from mjango.models import Model
from mjango.db import MongoDB
import random
import json

AND = operators.AND
OR = operators.OR


def gen_expres():
    length = random.randint(1, 50)
    exprs = {}
    for i in range(length):
        exprs[str(i)] = random.random()

    return exprs


def test_and():
    expres = gen_expres()
    query = AND(**expres)
    db = MongoDB('test')
    compiler = query.get_compiler(db, 'test')
    ans = {'$and': [expres]}
    assert json.dumps(compiler.compile()) == json.dumps(ans)

    expres = gen_expres()
    query = AND(query, **expres)
    compiler = query.get_compiler(db, 'test')
    assert json.dumps(compiler.compile()) == json.dumps(
        {'$and': [expres, ans]})
