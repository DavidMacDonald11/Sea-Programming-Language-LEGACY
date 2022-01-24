from ..node import Node

class PostfixExpressionNode(Node):
    @classmethod
    def construct(cls, parser):
        return parser.make.primary_expression()

    def interpret(self):
        pass

    def transpile(self):
        pass

class IndexOperatorNode(PostfixExpressionNode):
    @classmethod
    def construct(cls, parser):
        pass

class CallOperatorNode(PostfixExpressionNode):
    @classmethod
    def construct(cls, parser):
        pass

class AccessOperatorNode(PostfixExpressionNode):
    @classmethod
    def construct(cls, parser):
        pass

class PointerAccessOperatorNode(PostfixExpressionNode):
    @classmethod
    def construct(cls, parser):
        pass

class PostfixIncrementOperatorNode(PostfixExpressionNode):
    @classmethod
    def construct(cls, parser):
        pass

class PostfixDecrementOperatorNode(PostfixExpressionNode):
    @classmethod
    def construct(cls, parser):
        pass

# TODO Implement initializer list
