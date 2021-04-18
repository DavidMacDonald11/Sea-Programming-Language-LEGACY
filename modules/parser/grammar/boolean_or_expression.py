from modules.lexer.token_types import TT
from .boolean_and_expression import make_boolean_and_expression

def make_boolean_or_expression(parser, **make_funcs):
    make_funcs["boolean_or_expression"] = make_boolean_or_expression

    args = (parser, make_boolean_and_expression, ((TT.KEYWORD, "or"), ))
    return make_funcs["binary_operation"](*args, **make_funcs)
