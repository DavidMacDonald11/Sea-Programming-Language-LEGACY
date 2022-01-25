from types import SimpleNamespace
from ..node import Node

class UnaryExpressionNode(Node):
    @classmethod
    def construct(cls, parser):
        return parser.make.postfix_expression()

    def interpret(self):
        pass

    def transpile(self):
        pass

class PrefixIncrementOperatorNode(Node):
    @classmethod
    def construct(cls, parser):
        pass

class PrefixDecrementOperatorNode(Node):
    @classmethod
    def construct(cls, parser):
        pass

class UnaryCastNode(Node):
    @classmethod
    def construct(cls, parser):
        pass

class UnarySizeOfOperatorNode(Node):
    @classmethod
    def construct(cls, parser):
        pass

UNARY_MAKES = {
    "unary_expression": UnaryExpressionNode,
    "prefix_increment_operator": PrefixIncrementOperatorNode,
    "prefix_decrement_operator":  PrefixDecrementOperatorNode,
    "unary_cast": UnaryCastNode,
    "unary_size_of_operator": UnarySizeOfOperatorNode
}

#TODO Implment align of?
