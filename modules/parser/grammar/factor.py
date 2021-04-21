from modules.lexer.token_types import TT
from .part import make_part

def make_factor(parser, **make_funcs):
    make_funcs["factor"] = make_factor

    args = (parser, make_part, (TT.POWER, ), make_funcs["factor"])
    return make_funcs["binary_operation"](*args, **make_funcs)
