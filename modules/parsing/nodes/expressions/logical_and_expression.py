from .binary_expression import BinaryExpressionNode

class LogicalAndExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.logical_not_expression,
                ("and",),
                parser.make.logical_not_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
