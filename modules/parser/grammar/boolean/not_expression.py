from modules.lexer.token_types import TT
from ..comparison_expression import make_comparison_expression
from ...nodes.collection import NODES

def make_boolean_not_expression(parser, **make_funcs):
    make_funcs["boolean_not_expression"] = make_boolean_not_expression

    if not parser.token.matches(TT.KEYWORD, "not"):
        return make_comparison_expression(parser, **make_funcs)

    operation_token = parser.take_token()
    node = make_comparison_expression(parser, **make_funcs)

    return NODES.LeftUnaryOperationNode(operation_token, node)
