from position.position import Position
from ..ast_node import ASTNode

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        return f"({self.left}, {self.operator}, {self.right})"

    def interpret(self, memory):
        pass

    def transpile(self, memory):
        pass
