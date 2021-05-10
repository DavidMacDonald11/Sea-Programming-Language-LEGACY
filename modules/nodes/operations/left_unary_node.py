from position.position import Position
from transpiling.operators import get_c_operator
from tokens.operator import Op
from ..ast_node import ASTNode

class LeftUnaryOperationNode(ASTNode):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

        super().__init__(Position(operator.position.start, right.position.end))

    def __repr__(self):
        return f"({self.operator}, {self.right})"

    def interpret(self, memory):
        right = self.right.interpret(memory)
        return OPERATOR_FUNC[self.operator.data](right)

    def transpile(self, memory):
        operator = get_c_operator(self)
        right = self.right.transpile(memory)

        return f"({operator}{right})"

OPERATOR_FUNC = {
    Op.PLUS: (lambda x: +x),
    Op.MINUS: (lambda x: -x),
    Op.NOT: (lambda x: ~x),
    "not": (lambda x: not x)
}
