from modules.lexer.position import Position
from modules.lexer.token_types import TT
from modules.lexer.token import Token
from .bitwise.or_expression import make_bitwise_or_expression
from ..nodes.collection import NODES

def make_comparison_expression(parser, **make_funcs):
    make_funcs["make_comparison_expression"] = make_comparison_expression

    if parser.token.matches(TT.KEYWORD, "not"):
        operation_token = parser.take_token()
        node = make_comparison_expression(parser, **make_funcs)

        return NODES.LeftUnaryOperationNode(operation_token, node)

    operations = (TT.EQ, TT.NE, TT.LT, TT.GT, TT.LTE, TT.GTE)

    left = make_bitwise_or_expression(parser, **make_funcs)
    right = None

    while parser.token.type in operations:
        operation = parser.take_token()
        new_right = make_bitwise_or_expression(parser, **make_funcs)

        if right is None:
            left = NODES.BinaryOperationNode(left, operation, new_right)
        else:
            position = Position(right.position.end, operation.position.start)
            and_token = Token(TT.KEYWORD, "and", position)

            right = NODES.BinaryOperationNode(right, operation, new_right)
            left = NODES.BinaryOperationNode(left, and_token, right)

        right = new_right

    return left
