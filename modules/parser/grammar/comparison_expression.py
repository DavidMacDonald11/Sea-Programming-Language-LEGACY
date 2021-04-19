from modules.lexer.token_types import TT
from .bitwise.or_expression import make_bitwise_or_expression
from ..nodes.collection import NODES

def make_comparison_expression(parser, **make_funcs):
    make_funcs["make_comparison_expression"] = make_comparison_expression

    if parser.token.matches(TT.KEYWORD, "not"):
        operation_token = parser.take_token()
        node = make_comparison_expression(parser, **make_funcs)

        return NODES.LeftUnaryOperationNode(operation_token, node)

    operations = (TT.EQ, TT.NE, TT.LT, TT.GT, TT.LTE, TT.GTE)
    args = (parser, make_bitwise_or_expression, operations)

    return make_funcs["binary_operation"](*args, **make_funcs)
