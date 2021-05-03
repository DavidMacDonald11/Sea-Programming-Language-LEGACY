from tokens.symbol import Sym
from nodes.expressions.if_node import IfNode

def make_if_expression(parser, makes):
    cases = []
    else_case = None
    if_token = parser.take()
    get_if_case(parser, makes, cases)

    while parser.wanting(*parser.indent, "elif") is not None:
        get_if_case(parser, makes, cases)

    if parser.wanting(*parser.indent, "else") is not None:
        get_if_case(parser, makes)

    return IfNode(if_token, cases, else_case)

def get_if_case(parser, makes, cases = None):
    if cases is not None:
        condition = makes.expression(parser, makes)

    parser.expecting(Sym.COLON)
    expression = makes.block_or_expression(parser, makes)

    if cases is None:
        return expression

    cases += [(condition, expression)]
