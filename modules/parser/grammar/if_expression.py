from modules.lexer.token_types import TT
from .expression import make_expression
from ..nodes.collection import NODES

def make_if_expression(parser, **make_funcs):
    cases = []
    else_case = None
    if_token = get_if_case(parser, cases, **make_funcs)

    while parser.token.matches(TT.KEYWORD, "elif"):
        get_if_case(parser, cases, **make_funcs)

    if parser.token.matches(TT.KEYWORD, "else"):
        else_case = get_if_case(parser, **make_funcs)

    return NODES.IfNode(if_token, cases, else_case)

def get_if_case(parser, cases = None, **make_funcs):
    token = parser.take_token()

    if cases is not None:
        condition = make_expression(parser)

    parser.expecting(TT.COLON)
    expression = make_funcs["block_or_expression"](parser)

    if cases is None:
        return expression

    cases += [(condition, expression)]
    return token
