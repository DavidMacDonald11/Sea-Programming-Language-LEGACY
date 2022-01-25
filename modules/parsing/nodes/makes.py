from functools import wraps
from types import SimpleNamespace
from .expressions.primary_expression import PrimaryExpressionNode
from .expressions.primary_expression import IdentifierNode
from .expressions.primary_expression import ConstantNode
from .expressions.primary_expression import StringLiteralNode
from .expressions.primary_expression import ParentheticalExpressionNode
from .expressions.postfix_expression import IndexOperatorNode
from .expressions.postfix_expression import CallOperatorNode
from .expressions.postfix_expression import AccessOperatorNode
from .expressions.postfix_expression import PointerAccessOperatorNode
from .expressions.postfix_expression import PostfixIncrementOperatorNode
from .expressions.postfix_expression import PostfixDecrementOperatorNode

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
    string_literal = make(StringLiteralNode),
    parenthetical_expression = make(ParentheticalExpressionNode),
    primary_expression = make(PrimaryExpressionNode),
    index_operator = make(IndexOperatorNode),
    call_operator = make(CallOperatorNode),
    access_operator = make(AccessOperatorNode),
    pointer_access_operator = make(PointerAccessOperatorNode),
    postfix_increment_operator = make(PostfixIncrementOperatorNode),
    postfix_decrement_operator = make(PostfixDecrementOperatorNode)
)
