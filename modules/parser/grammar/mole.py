from modules.lexer.token_types import TT
from modules.parser.nodes.collection import NODES
from .atom import make_atom

def make_mole(parser, **make_funcs):
    make_funcs["mole"] = make_mole

    token_is_identifier = parser.token.type is TT.IDENTIFIER
    next_token_is_reassign = parser.token_ahead().type in (TT.INCREMENT, TT.DECREMENT)

    if token_is_identifier and next_token_is_reassign:
        variable = parser.take_token()
        operation = parser.take_token()
        return NODES.VariableReassignNode(variable, operation)

    return make_atom(parser, **make_funcs)
