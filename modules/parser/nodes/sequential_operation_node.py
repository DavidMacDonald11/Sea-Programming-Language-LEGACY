from modules.lexer.position import Position
from .ast_node import ASTNode

class SequentialOperationNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        return f"({self.left}, THEN, {self.right})"

    def visit(self, visitor):
        left = self.left.visit(visitor)
        right = self.right.visit(visitor)

        return left if right == "" else f"{left}\n{right}"

    def interpret(self, interpreter):
        return self.visit(interpreter)

    def transpile(self, transpiler):
        return self.visit(transpiler)
