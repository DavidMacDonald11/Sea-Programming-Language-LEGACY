from tokens.operator import Operator, Op
from tokens.identifier import Identifier
from nodes.memory_reassign_node import MemoryReassignNode
from nodes.operations.left_unary_node import LeftUnaryOperationNode

def make_part(parser, makes):
    if parser.token.matches(Operator, Op.INCREMENT, Op.DECREMENT):
        operator = parser.take()
        identifier = parser.expecting(Identifier, check_type = True)

        return MemoryReassignNode(identifier, operator, None, True)

    if parser.token.matches(Operator, Op.PLUS, Op.MINUS, Op.NOT):
        operator = parser.take()
        return LeftUnaryOperationNode(operator, makes.mole(parser, makes))

    return makes.mole(parser, makes)
