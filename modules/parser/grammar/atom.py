from modules.lexer.token_types import TT
from ..nodes.collection import NODES
from ...parser import errors

def make_atom(parser, **make_funcs):
    make_funcs["atom"] = make_atom

    if parser.token.type in (TT.INT, TT.FLOAT):
        return NODES.NumberNode(parser.take_token())

    if parser.token.type is TT.IDENTIFIER:
        return NODES.SymbolAccessNode(parser.take_token())

    try:
        parser.expecting(TT.LPAREN)
    except errors.ExpectedTokenError as e:
        raise errors.AtomError(e.token, e.expected, e.message) from e

    node = make_funcs["expression"](parser, **make_funcs)
    parser.expecting(TT.RPAREN)

    return node
