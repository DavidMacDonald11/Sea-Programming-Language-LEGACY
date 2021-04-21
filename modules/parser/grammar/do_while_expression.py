from modules.lexer.token_types import TT
from .expression import make_expression
from ..nodes.collection import NODES

def make_do_while_expression(parser, **make_funcs):
    do_token = parser.take_token()
    parser.expecting(TT.COLON)

    expression = make_funcs["block_or_expression"](parser)
    else_case = None

    parser.expecting_ahead(*([TT.INDENT] * parser.depth))
    parser.expecting_keyword("while")
    condition = make_expression(parser, **make_funcs)

    parser.expecting(TT.NEWLINE, TT.EOF)
    parser.remove_newlines()

    if parser.take_tokens_if_ahead(*(*parser.indent, (TT.KEYWORD, "else"))):
        parser.expecting(TT.COLON)
        else_case = make_funcs["block_or_expression"](parser)

    return NODES.DoWhileNode(do_token, expression, condition, else_case)
