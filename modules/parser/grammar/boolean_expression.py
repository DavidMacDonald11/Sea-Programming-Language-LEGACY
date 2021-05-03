from tokens.keyword import Keyword
from nodes.operations.left_unary_node import LeftUnaryOperationNode

def make_boolean_not_expression(parser, makes):
    if not parser.token.matches(Keyword, "not"):
        return makes.comparison_expression(parser, makes)

    operator = parser.take()
    node = make_boolean_not_expression(parser, makes)

    return LeftUnaryOperationNode(operator, node)

def make_boolean_and_expression(parser, makes):
    return makes.binary_operation(parser, makes, "and", make_boolean_not_expression)

def make_boolean_or_expression(parser, makes):
    return makes.binary_operation(parser, makes, "or", make_boolean_and_expression)
