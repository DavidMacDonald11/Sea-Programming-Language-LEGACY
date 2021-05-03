from position.position import Position
from ..ast_node import ASTNode

class TernaryOperationNode(ASTNode):
    def __init__(self, operations, values):
        self.left, self.middle, self.right = values
        self.operations = operations

        self.operation_values = tuple(map(lambda x: x.value, self.operations))
        self.operators = tuple(map(lambda x: x.type, self.operations))

        super().__init__(Position(self.left.position.start, self.right.position.end))

    def __repr__(self):
        left = f"({self.left}, {self.operations[0]}, "
        return left + f"{self.middle}, {self.operations[1]}, {self.right})"