from parser import errors
from tokens.symbol import Sym
from tokens.literal import Literal
from tokens.identifier import Identifier
from nodes.number_node import NumberNode
from nodes.memory_access_node import MemoryAccessNode

def make_atom(parser, makes):
    if parser.token.matches(Literal) and parser.token.matches_type("int", "float"):
        return NumberNode(parser.take())

    if parser.token.matches(Identifier):
        return MemoryAccessNode(parser.take())

    try:
        parser.expecting(Sym.LPAREN)
    except errors.ExpectedTokenError as e:
        raise errors.AtomError(e.position, e.message) from e

    node = makes.expression(parser, makes)
    parser.expecting(Sym.RPAREN)

    return node
