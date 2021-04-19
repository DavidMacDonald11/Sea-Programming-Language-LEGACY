from modules.lexer.token_types import TT
from .and_expression import make_bitwise_and_expression

def make_bitwise_xor_expression(parser, **make_funcs):
    make_funcs["bitwise_xor_expression"] = make_bitwise_xor_expression

    args = (parser, make_bitwise_and_expression, (TT.XOR, ))
    return make_funcs["binary_operation"](*args, **make_funcs)
