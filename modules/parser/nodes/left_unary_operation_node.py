from modules.lexer.position import Position
from modules.lexer.token_types import TT
from modules.visitor.transpiler.operators import get_c_operator
from .ast_node import ASTNode

class LeftUnaryOperationNode(ASTNode):
    def __init__(self, operation, right):
        self.operation = operation
        self.operator = operation.type
        self.right = right

        super().__init__(Position(operation.position.start, right.position.end))

    def __repr__(self):
        return f"({self.operation}, {self.right})"

    def interpret(self, interpreter):
        right = self.right.interpret(interpreter)

        if self.operator is TT.KEYWORD:
            return OPERATOR_KEYWORD_FUNC[self.operation.value](right)

        return OPERATOR_FUNC[self.operation.type](right)

    def transpile(self, transpiler):
        operator = get_c_operator(self)
        right = self.right.transpile(transpiler)

        return f"({operator}{right})"

OPERATOR_FUNC = {
    TT.PLUS: (lambda x: +x),
    TT.MINUS: (lambda x: -x),
    TT.NOT: (lambda x: ~x)
}

OPERATOR_KEYWORD_FUNC = {
    "not": (lambda x: not x)
}
