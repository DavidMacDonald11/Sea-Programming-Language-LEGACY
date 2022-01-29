from .binary_expression import BinaryExpressionNode

class LogicalOrExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.logical_and_expression,
                ("or",),
                parser.make.logical_and_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
