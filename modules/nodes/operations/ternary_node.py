from position.position import Position
from ..ast_node import ASTNode

class TernaryOperationNode(ASTNode):
    def __init__(self, operations, values):
        self.left, self.middle, self.right = values
        self.operations = operations

        stream = self.left.position.stream
        super().__init__(Position(stream, self.left.position.start, self.right.position.end))

    def __repr__(self):
        left = f"({self.left}, {self.operations[0]}, "
        return left + f"{self.middle}, {self.operations[1]}, {self.right})"

    def interpret(self, memory):
        left = self.left.interpret(memory)
        middle = self.middle.interpret(memory)
        right = self.right.interpret(memory)

        key = (self.operations[0].data, self.operations[1].data)
        inputs = (left, middle, right)

        return OPERATOR_FUNC[key](*inputs)

    def transpile(self, memory):
        left = self.left.transpile(memory)
        middle = self.middle.transpile(memory)
        right = self.right.transpile(memory)

        return f"({middle} ? {left} : {right})"

OPERATOR_FUNC = {
    ("if", "else"): (lambda x, y, z: x if y else z)
}
