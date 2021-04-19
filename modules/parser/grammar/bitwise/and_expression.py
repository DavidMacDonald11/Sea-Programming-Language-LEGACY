from modules.lexer.token_types import TT
from .shift_expression import make_bitwise_shift_expression

def make_bitwise_and_expression(parser, **make_funcs):
    make_funcs["bitwise_and_expression"] = make_bitwise_and_expression

    args = (parser, make_bitwise_shift_expression, (TT.AND, ))
    return make_funcs["binary_operation"](*args, **make_funcs)
