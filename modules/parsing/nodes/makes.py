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
        "expression": AdditiveExpressionNode,
        "assignment_expression": AdditiveExpressionNode
    })
)

# TODO replace expression
# TODO replace assignment expression
