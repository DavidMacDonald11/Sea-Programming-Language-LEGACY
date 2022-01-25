from functools import wraps
from types import SimpleNamespace
from .expressions.primary_expression import PRIMARY_MAKES
from .expressions.postfix_expression import POSTFIX_MAKES
from .expressions.unary_expression import UNARY_MAKES

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
    **make(POSTFIX_MAKES),
    **make(UNARY_MAKES)
)
