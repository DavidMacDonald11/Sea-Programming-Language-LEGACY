from position.position import Position
from ..ast_node import ASTNode

class SequentialOperationNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        return f"({self.left}, THEN, {self.right})"

    def interpret(self, memory):
        pass

    def transpile(self, memory):
        pass
