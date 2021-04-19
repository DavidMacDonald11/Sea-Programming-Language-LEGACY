from modules.lexer.position import Position
from modules.lexer.token_types import TT
from modules.interpreter import arithmetic
from modules.interpreter import errors as i_errors
from .ast_node import ASTNode

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.operator = operation.type
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        return f"({self.left}, {self.operation}, {self.right})"

    def interpret(self, interpreter):
        left = self.left.interpret(interpreter)
        right = self.right.interpret(interpreter)

        try:
            if self.operator is TT.KEYWORD:
                return OPERATOR_KEYWORD_FUNC[self.operation.value](left, right)

            return OPERATOR_FUNC[self.operator](left, right)
        except i_errors.NumericalError as error:
            error.node = self.right
            raise error

    def transpile(self, transpiler):
        left = self.left.transpile(transpiler)
        right = self.right.transpile(transpiler)

        if self.operation.type is TT.POWER:
            return self.transpile_power(transpiler, left, right)

        if self.operation.matches(TT.KEYWORD, "xor"):
            return f"(({left} || {right}) && !({left} && {right}))"

        operator = transpiler.get_operator(self)

        return f"({left} {operator} {right})"

    def transpile_power(self, transpiler, left, right):
        left_token = self.left.token
        right_token = self.right.token

        transpiler.headers.add("#include <math.h>")

        if left_token.type is TT.INT and right_token.type is TT.INT:
            return f"((int)powf({left}, {right}))"

        return f"powl({left}, {right})"

def arithmetic_power(transpiler, left, right):
    transpiler.headers.add("#include <math.h>")

    if left.type is TT.INT and right.type is TT.INT:
        return f"((int)powf({left.value}, {right.value}))"

    return f"powl({left.value}, {right.value})"

OPERATOR_FUNC = {
    TT.PLUS: (lambda x, y: x + y),
    TT.MINUS: (lambda x, y: x - y),
    TT.MULTIPLY: (lambda x, y: x * y),
    TT.POWER: arithmetic.pow_nums,
    TT.DIVIDE: arithmetic.div_nums,
    TT.MODULO: arithmetic.mod_nums,
    TT.EQ: (lambda x, y: x == y),
    TT.NE: (lambda x, y: x != y),
    TT.LT: (lambda x, y: x < y),
    TT.GT: (lambda x, y: x > y),
    TT.LTE: (lambda x, y: x <= y),
    TT.GTE: (lambda x, y: x >= y),
    TT.LSHIFT: (lambda x, y: x << y),
    TT.RSHIFT: (lambda x, y: x >> y),
    TT.AND: (lambda x, y: x & y),
    TT.XOR: (lambda x, y: x ^ y),
    TT.OR: (lambda x, y: x | y)
}

OPERATOR_KEYWORD_FUNC = {
    "and": (lambda x, y: x and y),
    "xor": (lambda x, y: (x or y) and not (x and y)),
    "or": (lambda x, y: x or y)
}
