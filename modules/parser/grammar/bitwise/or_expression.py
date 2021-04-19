from modules.lexer.token_types import TT
from .xor_expression import make_bitwise_xor_expression

def make_bitwise_or_expression(parser, **make_funcs):
    make_funcs["bitwise_or_expression"] = make_bitwise_or_expression

    args = (parser, make_bitwise_xor_expression, (TT.OR,))
    return make_funcs["binary_operation"](*args, **make_funcs)
