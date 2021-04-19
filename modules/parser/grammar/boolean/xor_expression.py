from modules.lexer.token_types import TT
from .and_expression import make_boolean_and_expression

def make_boolean_xor_expression(parser, **make_funcs):
    make_funcs["boolean_xor_expression"] = make_boolean_xor_expression

    args = (parser, make_boolean_and_expression, ((TT.KEYWORD, "xor"), ))
    return make_funcs["binary_operation"](*args, **make_funcs)
