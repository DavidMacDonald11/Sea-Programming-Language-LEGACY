from modules.lexer.token_types import TT
from .atom import make_atom

def make_power(parser, **make_funcs):
    make_funcs["power"] = make_power

    args = (parser, make_atom, (TT.POWER, ), make_funcs["factor"])
    return make_funcs["binary_operation"](*args, **make_funcs)
