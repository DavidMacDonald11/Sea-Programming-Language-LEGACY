from functools import wraps
from types import SimpleNamespace
from .expressions.primary_expression import PRIMARY_MAKES
from .expressions.postfix_expression import PostfixExpressionNode
from .expressions.argument_expression_list import ArgumentExpressionListNode
from .expressions.exponential_expression import ExponentialExpressionNode
from .expressions.unary_expression import UnaryExpressionNode
from .expressions.cast_expression import CastExpressionNode
from .expressions.multiplicative_expression import MultiplicativeExpressionNode
from .expressions.additive_expression import AdditiveExpressionNode
from .expressions.shift_expression import ShiftExpressionNode
from .expressions.bitwise_and_expression import BitwiseAndExpressionNode
from .expressions.bitwise_xor_expression import BitwiseXorExpressionNode
from .expressions.bitwise_or_expression import BitwiseOrExpressionNode

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
        "exponential_expression": ExponentialExpressionNode,
        "unary_expression": UnaryExpressionNode,
        "cast_expression": CastExpressionNode,
        "multiplicative_expression": MultiplicativeExpressionNode,
        "additive_expression": AdditiveExpressionNode,
        "shift_expression": ShiftExpressionNode,
        "bitwise_and_expression": BitwiseAndExpressionNode,
        "bitwise_xor_expression": BitwiseXorExpressionNode,
        "bitwise_or_expression": BitwiseOrExpressionNode,
        "expression": BitwiseOrExpressionNode,
        "assignment_expression": BitwiseOrExpressionNode
    })
)

# TODO replace expression
# TODO replace assignment expression
