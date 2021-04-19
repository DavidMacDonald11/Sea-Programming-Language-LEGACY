from modules.lexer.token_types import TT
from .factor import  make_factor

def make_term(parser, **make_funcs):
    make_funcs["term"] = make_term

    args = (parser, make_factor, (TT.MULTIPLY, TT.DIVIDE, TT.MODULO))
    return make_funcs["binary_operation"](*args, **make_funcs)
