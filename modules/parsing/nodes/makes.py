from functools import wraps
from types import SimpleNamespace
from .expressions.primary_expression import PRIMARY_MAKES
from .expressions.postfix_expression import PostfixExpressionNode
from .expressions.argument_expression_list import ArgumentExpressionListNode
from .expressions.prefix_deviation_expression import PrefixDeviationExpressionNode
from .expressions.exponential_expression import ExponentialExpressionNode
from .expressions.unary_expression import UnaryExpressionNode
from .expressions.cast_expression import CastExpressionNode
from .expressions.multiplicative_expression import MultiplicativeExpressionNode
from .expressions.additive_expression import AdditiveExpressionNode
from .expressions.shift_expression import ShiftExpressionNode
from .expressions.bitwise_and_expression import BitwiseAndExpressionNode
from .expressions.bitwise_xor_expression import BitwiseXorExpressionNode
from .expressions.bitwise_or_expression import BitwiseOrExpressionNode
from .expressions.comparison_expression import ComparisonExpressionNode
from .expressions.logical_not_expression import LogicalNotExpressionNode
from .expressions.logical_and_expression import LogicalAndExpressionNode
from .expressions.logical_or_expression import LogicalOrExpressionNode
from .expressions.conditional_expression import ConditionalExpressionNode
from .expressions.assignment_expression import AssignmentExpressionNode
from .expressions.expression import ExpressionNode

PARSER = []

def set_parser(parser):
    PARSER.clear()
    PARSER.append(parser)

def make(makes):
    def wrap(node):
        @wraps(node.construct)
        def decorator():
            return node.construct(PARSER[0])

        return decorator

    return {k:wrap(v) for k,v in makes.items()}

MAKES = SimpleNamespace(
    **make(PRIMARY_MAKES),
    **make({
        "postfix_expression": PostfixExpressionNode,
        "argument_expression_list": ArgumentExpressionListNode,
        "prefix_deviation_expression": PrefixDeviationExpressionNode,
        "exponential_expression": ExponentialExpressionNode,
        "unary_expression": UnaryExpressionNode,
        "cast_expression": CastExpressionNode,
        "multiplicative_expression": MultiplicativeExpressionNode,
        "additive_expression": AdditiveExpressionNode,
        "shift_expression": ShiftExpressionNode,
        "bitwise_and_expression": BitwiseAndExpressionNode,
        "bitwise_xor_expression": BitwiseXorExpressionNode,
        "bitwise_or_expression": BitwiseOrExpressionNode,
        "comparison_expression": ComparisonExpressionNode,
        "logical_not_expression": LogicalNotExpressionNode,
        "logical_and_expression": LogicalAndExpressionNode,
        "logical_or_expression": LogicalOrExpressionNode,
        "conditional_expression": ConditionalExpressionNode,
        "constant_expression": ConditionalExpressionNode,
        "assignment_expression": AssignmentExpressionNode,
        "expression": ExpressionNode
    })
)
