from position.position import Position
from ..ast_node import ASTNode

class SequentialOperationNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        return f"({self.left}, THEN, {self.right})"

    def visit(self, mode, memory):
        left = self.left.visit(mode, memory)
        right = self.right.visit(mode, memory)

        return left if right == "" else f"{left}\n{right}"

    def interpret(self, memory):
        self.visit("i", memory)

    def transpile(self, memory):
        self.visit("t", memory)
