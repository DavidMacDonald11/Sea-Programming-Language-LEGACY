from modules.lexer.token_types import TT
from ..arithmetic_expression import make_arithmetic_expression

def make_bitwise_shift_expression(parser, **make_funcs):
    make_funcs["bitwise_shift_expression"] = make_bitwise_shift_expression

    args = (parser, make_arithmetic_expression, (TT.LSHIFT, TT.RSHIFT))
    return make_funcs["binary_operation"](*args, **make_funcs)
