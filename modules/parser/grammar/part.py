from modules.lexer.token_types import TT
from modules.parser.nodes.collection import NODES
from .mole import make_mole

def make_part(parser, **make_funcs):
    make_funcs["part"] = make_part

    if parser.token.type in (TT.INCREMENT, TT.DECREMENT):
        operation = parser.take_token()
        variable = parser.expecting(TT.IDENTIFIER)

        return NODES.VariableReassignNode(variable, operation, None, True)

    if parser.token.type in (TT.PLUS, TT.MINUS, TT.NOT):
        operation = parser.take_token()
        return NODES.LeftUnaryOperationNode(operation, make_mole(parser, **make_funcs))

    return make_mole(parser, **make_funcs)
