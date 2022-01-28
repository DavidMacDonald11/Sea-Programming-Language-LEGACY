from ..node import Node

class PostfixExpressionNode(Node):
    @classmethod
    def construct(cls, parser):
        return parser.make.primary_expression()

    def interpret(self):
        pass

    def transpile(self):
        pass
