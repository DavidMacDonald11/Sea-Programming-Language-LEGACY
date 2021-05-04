from tokens.operator import Operator, Op
from tokens.identifier import Identifier
from nodes.variable_reassign_node import VariableReassignNode

def make_mole(parser, makes):
    if isinstance(parser.token, Identifier):
        parser.advance()

        if parser.token.matches(Operator, Op.INCREMENT, Op.DECREMENT):
            parser.retreat()
            identifier = parser.take()
            operator = parser.take()

            return VariableReassignNode(identifier, operator)

        parser.retreat()

    return makes.atom(parser, makes)
