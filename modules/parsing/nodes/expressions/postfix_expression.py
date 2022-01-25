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

POSTFIX_MAKES = {
    "postfix_expression": PostfixExpressionNode,
    "index_operator": IndexOperatorNode,
    "call_operator": CallOperatorNode,
    "access_operator": AccessOperatorNode,
    "pointer_access_operator": PointerAccessOperatorNode,
    "postfix_increment_operator": PostfixIncrementOperatorNode,
    "postfix_decrement_operator": PostfixDecrementOperatorNode
}
