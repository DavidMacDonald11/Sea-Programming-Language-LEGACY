from tokens.symbol import Sym
from nodes.expressions.for_node import ForNode

def make_for_expression(parser, makes):
    for_token = parser.take()
    assignment = makes.expression(parser, makes)
    parser.expecting(Sym.SEMICOLON)

    condition = makes.expression(parser, makes)
    parser.expecting(Sym.SEMICOLON)

    reassignment = makes.expression(parser, makes)
    parser.expecting(Sym.COLON)

    block = makes.block_or_expression(parser, makes)
    else_case = None

    if parser.wanting(parser.indent, "else") is not None:
        parser.expecting(Sym.COLON)
        else_case = makes.block_or_expression(parser, makes)

    triple = (assignment, condition, reassignment)
    return ForNode(for_token, triple, block, else_case)
