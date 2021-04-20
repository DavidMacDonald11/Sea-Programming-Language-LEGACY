from modules.lexer.position import Position
from modules.lexer.token_types import TT
from modules.visitor import errors as v_errors
from .ast_node import ASTNode

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

    def interpret(self, interpreter):
        left = self.left.interpret(interpreter)
        middle = self.middle.interpret(interpreter)
        right = self.right.interpret(interpreter)

        inputs = (left, middle, right)

        if self.operators == (TT.KEYWORD, TT.KEYWORD):
            return OPERATOR_KEYWORD_FUNC[self.operation_values](*inputs)

        return OPERATOR_FUNC[self.operations](*inputs)

    def transpile(self, transpiler):
        left = self.left.transpile(transpiler)
        middle = self.middle.transpile(transpiler)
        right = self.right.transpile(transpiler)

        if self.operators != (TT.KEYWORD, TT.KEYWORD) or self.operation_values != ("if", "else"):
            raise v_errors.UnimplementedOperationError(self)

        return f"({middle} ? {left} : {right})"

OPERATOR_FUNC = {

}

OPERATOR_KEYWORD_FUNC = {
    ("if", "else"): (lambda x, y, z: x if y else z)
}
