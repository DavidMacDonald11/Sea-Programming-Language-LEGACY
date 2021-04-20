from modules.lexer.token_types import TT
from .not_expression import make_boolean_not_expression

def make_boolean_and_expression(parser, **make_funcs):
    make_funcs["boolean_and_expression"] = make_boolean_and_expression

    args = (parser, make_boolean_not_expression, ((TT.KEYWORD, "and"), ))
    return make_funcs["binary_operation"](*args, **make_funcs)
