from tokens.symbol import Sym
from nodes.expressions.do_while_node import DoWhileNode

def make_do_while_expression(parser, makes):
    do_token = parser.take()
    parser.expecting(Sym.COLON)

    block = makes.block_or_expression(parser, makes)
    else_case = None

    parser.expecting(*parser.indent, "while")
    condition = makes.expression(parser, makes)
    else_case = makes.else_case(parser, makes)

    if else_case is None:
        parser.expecting((Sym.NEWLINE, Sym.EOF))
        else_case = makes.else_case(parser, makes)

    return DoWhileNode(do_token, block, condition, else_case)
