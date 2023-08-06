from mjango import expressions


def determine(key, value, cls):
    expr_class = expressions.build_expr_obj(key, value)
    return isinstance(expr_class, cls)


def test_expressions():
    assert determine('a', '1', expressions.Str)
    assert determine('a', 1, expressions.Num)
    assert determine('a', True, expressions.Bool)
    assert determine('a', {'b': 'c'}, expressions.Nested)
    assert determine('a__b__c', 'c', expressions.Nested)
    assert determine('a__gte', 'c', expressions.GTE)
    assert determine('a__lte', 'c', expressions.LTE)
    assert determine('a__gt', 'c', expressions.GT)
    assert determine('a__lt', 'c', expressions.LT)
    assert determine('a__in', 'c', expressions.IN)
    assert determine('a__ne', 'c', expressions.NE)


def test_nested():
    expr = expressions.build_expr_obj('a', {'b': 'c'})
    assert expr.key == 'a'
    assert isinstance(expr.value[0], expressions.Str)
    assert expr.value[0].key == 'b'
    assert expr.value[0].value == 'c'


def test_build_in_nested():
    expr = expressions.build_expr_obj('a__b', 'c')
    assert expr.key == 'a'
    assert isinstance(expr.value[0], expressions.Str)
    assert expr.value[0].key == 'b'
    assert expr.value[0].value == 'c'
