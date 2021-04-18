from modules.lexer.token_types import TT
from modules.parser.nodes.collection import NODES
from .power import make_power

def make_factor(parser, **make_funcs):
    if parser.token.type in (TT.PLUS, TT.MINUS):
        operation_token = parser.take_token()
        return NODES.LeftUnaryOperationNode(operation_token, make_factor(parser, **make_funcs))

    make_funcs["factor"] = make_factor
    return make_power(parser, **make_funcs)
