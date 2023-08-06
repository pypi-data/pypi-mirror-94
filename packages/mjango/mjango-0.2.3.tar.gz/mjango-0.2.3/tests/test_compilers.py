from mjango import operators
from mjango.mongodb import compilers


def test_compiler():
    compiler = compilers.QueryCompiler()
    query = operators.AND(a__b=1, b=2, c__gte=3)

    print(compiler.compile(query))
