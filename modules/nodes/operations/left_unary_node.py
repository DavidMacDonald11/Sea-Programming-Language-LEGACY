from position.position import Position
from ..ast_node import ASTNode

class LeftUnaryOperationNode(ASTNode):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

        super().__init__(Position(operator.position.start, right.position.end))

    def __repr__(self):
        return f"({self.operator}, {self.right})"

    def interpret(self, memory):
        pass

    def transpile(self, memory):
        pass
