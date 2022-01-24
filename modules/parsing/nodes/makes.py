from functools import wraps
from types import SimpleNamespace
from .expressions.primary_expression import PrimaryExpressionNode
from .expressions.primary_expression import IdentifierNode
from .expressions.primary_expression import ConstantNode
from .expressions.primary_expression import ParentheticalExpressionNode

PARSER = []

def set_parser(parser):
    PARSER.clear()
    PARSER.append(parser)

def make(node):
    @wraps(node.construct)
    def decorator():
        return node.construct(PARSER[0])

    return decorator

MAKES = SimpleNamespace(
    identifier = make(IdentifierNode),
    constant = make(ConstantNode),
    parenthetical_expression = make(ParentheticalExpressionNode),
    primary_expression = make(PrimaryExpressionNode)
)
