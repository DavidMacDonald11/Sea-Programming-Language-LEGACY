from position.position import Position
from tokens.operator import Op
from tokens.keyword import Keyword
from nodes.operations.binary_node import BinaryOperationNode

def make_comparison_expression(parser, makes):
    operations = (Op.EQ, Op.NE, Op.LT, Op.GT, Op.LTE, Op.GTE)

    left = makes.bitwise_or_expression(parser, makes)
    right = None

    while parser.token.data in operations:
        operator = parser.take()
        new_right = makes.bitwise_or_expression(parser, makes)

        if right is None:
            left = BinaryOperationNode(left, operator, new_right)
        else:
            position = Position(right.position.stream, right.position.end, operator.position.start)
            and_token = Keyword("and", position)

            right = BinaryOperationNode(right, operator, new_right)
            left = BinaryOperationNode(left, and_token, right)

        right = new_right

    return left
