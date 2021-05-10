from position.position import Position
from interpreting import errors
from interpreting import arithmetic as iarithmetic
from interpreting import bitwise
from transpiling import arithmetic as tarithmetic
from transpiling.operators import get_c_operator
from tokens.operator import Op
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
        left = self.left.interpret(memory)
        right = self.right.interpret(memory)

        try:
            return OPERATOR_FUNC[self.operator.data](left, right)
        except errors.InterpreterError as error:
            error.node = self
            raise error

    def transpile(self, memory):
        self.interpret(memory.memory)

        left = self.left.transpile(memory)
        right = self.right.transpile(memory)

        if self.operator is Op.POWER:
            return tarithmetic.pow_nums(right, left, memory)

        operator = get_c_operator(self)

        return f"({left} {operator} {right})"

OPERATOR_FUNC = {
    Op.PLUS: (lambda x, y: x + y),
    Op.MINUS: (lambda x, y: x - y),
    Op.MULTIPLY: (lambda x, y: x * y),
    Op.POWER: iarithmetic.pow_nums,
    Op.DIVIDE: iarithmetic.div_nums,
    Op.MODULO: iarithmetic.mod_nums,
    Op.EQ: (lambda x, y: x == y),
    Op.NE: (lambda x, y: x != y),
    Op.LT: (lambda x, y: x < y),
    Op.GT: (lambda x, y: x > y),
    Op.LTE: (lambda x, y: x <= y),
    Op.GTE: (lambda x, y: x >= y),
    Op.LSHIFT: bitwise.lshift_nums,
    Op.RSHIFT: bitwise.rshift_nums,
    Op.AND: bitwise.and_nums,
    Op.XOR: bitwise.xor_nums,
    Op.OR: bitwise.or_nums,
    "and": (lambda x, y: x and y),
    "or": (lambda x, y: x or y)
}
