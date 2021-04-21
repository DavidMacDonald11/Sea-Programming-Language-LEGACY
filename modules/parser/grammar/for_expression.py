from modules.lexer.token_types import TT
from .expression import make_expression
from ..nodes.collection import NODES

def make_for_expression(parser, **make_funcs):
    for_token = parser.take_token()
    assignment = make_expression(parser, **make_funcs)
    parser.expecting(TT.SEMICOLON)

    condition = make_expression(parser, **make_funcs)
    parser.expecting(TT.SEMICOLON)

    reassignment = make_expression(parser, **make_funcs)
    parser.expecting(TT.COLON)

    expression = make_funcs["block_or_expression"](parser)
    else_case = None

    parser.remove_newlines()

    if parser.take_tokens_if_ahead(*(*parser.indent, (TT.KEYWORD, "else"))):
        parser.expecting(TT.COLON)
        else_case = make_funcs["block_or_expression"](parser)

    triple = (assignment, condition, reassignment)

    return NODES.ForNode(for_token, triple, expression, else_case)
