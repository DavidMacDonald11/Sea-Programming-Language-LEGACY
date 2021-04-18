from modules.lexer.token_types import TT
from .term import make_term

def make_arithmetic_expression(parser, **make_funcs):
    make_funcs["make_arithmetic_expression"] = make_arithmetic_expression

    args = (parser, make_term, (TT.PLUS, TT.MINUS))
    return make_funcs["binary_operation"](*args, **make_funcs)
