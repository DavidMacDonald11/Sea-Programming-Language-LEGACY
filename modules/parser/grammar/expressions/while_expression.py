from tokens.symbol import Sym
from nodes.expressions.while_node import WhileNode

def make_while_expression(parser, makes):
    while_token = parser.take()
    condition = makes.expression(parser, makes)
    parser.expecting(Sym.COLON)

    block = makes.block_or_expression(parser, makes)
    else_case = None

    if parser.wanting(*parser.indent, "else") is not None:
        parser.expecting(Sym.COLON)
        else_case = makes.block_or_expression(parser, makes)

    return WhileNode(while_token, condition, block, else_case)
