from tokens.token import Token
from tokens.keyword import Keyword, TYPE_KEYWORDS
from tokens.operator import Op
from tokens.identifier import Identifier
from nodes.memory_assign_node import MemoryAssignNode
from nodes.memory_reassign_node import MemoryReassignNode
from nodes.operations.binary_node import BinaryOperationNode
from nodes.operations.ternary_node import TernaryOperationNode

def make_expression(parser, makes):
    if parser.token.matches(Keyword) and parser.token.data in TYPE_KEYWORDS:
        return make_memory_assign(parser, makes)

    if parser.token.matches(Identifier):
        parser.advance()

        if "EQUALS" in f"{parser.token.data}":
            parser.retreat()
            return make_memory_reassign(parser, makes)

        parser.retreat()

    return ternary_operation(parser, makes, "if", "else", makes.boolean_or_expression)

def make_memory_assign(parser, makes):
    keyword = parser.take()
    identifier = parser.expecting(Identifier, check_type = True)
    parser.expecting(Op.EQUALS)
    expression = makes.expression(parser, makes)

    return MemoryAssignNode(keyword, identifier, expression)

def make_memory_reassign(parser, makes):
    identifier = parser.take()
    operator = parser.take()
    expression = makes.expression(parser, makes)

    return MemoryReassignNode(identifier, operator, expression)

def ternary_operation(parser, makes, left_operations, right_operations, *funcs):
    left = funcs[0](parser, makes)

    if not isinstance(left_operations, (tuple, list)):
        left_operations = (left_operations,)

    if not parser.token.matches(Token, *left_operations):
        return left

    left_operation = parser.take()
    middle = funcs[-1](parser, makes)

    if not isinstance(right_operations, (tuple, list)):
        right_operations = (right_operations,)

    if not parser.token.matches(Token, *right_operations):
        return BinaryOperationNode(left, left_operation, middle)

    right_operation = parser.take()
    right = funcs[-2](parser, makes) if len(funcs) > 2 else funcs[-1](parser, makes)

    operations = (left_operation, right_operation)
    values = (left, middle, right)

    return TernaryOperationNode(operations, values)

def binary_operation(parser, makes, operations, *funcs):
    left = funcs[0](parser, makes)

    if not isinstance(operations, (tuple, list)):
        operations = (operations,)

    while parser.token.matches(Token, *operations):
        operator = parser.take()
        right = funcs[-1](parser, makes)
        left = BinaryOperationNode(left, operator, right)

    return left
