from functools import wraps
from types import SimpleNamespace
from .expressions.primary_expression import PRIMARY_MAKES
from .expressions.postfix_expression import PostfixExpressionNode
from .expressions.unary_expression import UnaryExpressionNode
from .expressions.cast_expression import CastExpressionNode
from .expressions.multiplicative_expression import MultiplicativeExpressionNode

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
        "unary_expression": UnaryExpressionNode,
        "cast_expression": CastExpressionNode,
        "multiplicative_expression": MultiplicativeExpressionNode,
        "expression": MultiplicativeExpressionNode
    })
)

# TODO replace expression
