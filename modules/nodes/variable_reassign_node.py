from position.position import Position
from tokens.operator import Operator, Op
from tokens.literal import Literal
from visiting import errors
from transpiling.operators import get_c_operator
from .ast_node import ASTNode
from .number_node import NumberNode
from .variable_access_node import VariableAccessNode
from .operations.binary_node import BinaryOperationNode

class VariableReassignNode(ASTNode):
    def __init__(self, identifier, operator, value = None, left = False):
        self.identifier = identifier
        self.operator = operator
        self.value = value
        self.left = left

        position_start = (operator if left else identifier).position.start

        right = identifier if left else identifier
        position_end = (value if value is not None else right).position.end
        stream = operator.position.stream

        super().__init__(Position(stream, position_start, position_end))

    def __repr__(self):
        value = "" if self.value is None else f", {self.value}"

        if self.left:
            return f"({self.operator}, {self.identifier}{value})"

        return f"({self.identifier}, {self.operator}{value})"

    def visit(self, mode, memory):
        if self.operator.operator is Op.EQUALS:
            return super().visit(mode, memory)

        if self.operator.operator in (Op.INCREMENT, Op.DECREMENT):
            return self.visit_unary(mode, memory)

        position = Position(self.operator.position.stream, self.operator.position.start)
        operation = Operator(OPERATOR_FUNC[self.operator.data], position)
        assign = Operator(Op.EQUALS, position)

        node = VariableAccessNode(self.identifier)
        node = BinaryOperationNode(node, operation, self.value)
        node = VariableReassignNode(self.identifier, assign, node)

        return node.visit(mode, memory)

    def visit_unary(self, mode, memory):
        if mode == "t":
            return self.transpile_unary(memory)

        return self.interpret_unary(memory)

    def interpret(self, memory):
        if self.operator.operator is not Op.EQUALS:
            return self.visit("i", memory)

        identifier = self.identifier.data

        if not memory.contains(identifier):
            raise errors.UndefinedIdentifierError(self, identifier)

        value = self.value.interpret(memory)
        memory.modify(identifier, value)

        return value

    def interpret_unary(self, memory):
        position = Position(self.operator.position.stream, self.operator.position.start)
        token_type = Op.PLUS_EQUALS if self.operator.operator is Op.INCREMENT else Op.MINUS_EQUALS
        operation = Operator(token_type, position)
        one = NumberNode(Literal("int", 1, position))

        node = VariableReassignNode(self.identifier, operation, one)

        if self.left:
            return node.visit("i", memory)

        value = VariableAccessNode(self.identifier).interpret(memory)
        node.visit("i", memory)

        return value

    def transpile(self, memory):
        if self.operator.operator is not Op.EQUALS:
            return self.visit("t", memory)

        value = self.value.transpile(memory)
        return f"({self.identifier} = {value})"

    def transpile_unary(self, _):
        operator = get_c_operator(self)

        if self.left:
            return f"({operator}{self.identifier})"

        return f"({self.identifier}{operator})"

OPERATOR_FUNC = {
    Op.PLUS_EQUALS: Op.PLUS,
    Op.MINUS_EQUALS: Op.MINUS,
    Op.MULTIPLY_EQUALS: Op.MULTIPLY,
    Op.POWER_EQUALS: Op.POWER,
    Op.DIVIDE_EQUALS: Op.DIVIDE,
    Op.MODULO_EQUALS: Op.MODULO,
    Op.LSHIFT_EQUALS: Op.LSHIFT,
    Op.RSHIFT_EQUALS: Op.RSHIFT,
    Op.AND_EQUALS: Op.AND,
    Op.XOR_EQUALS: Op.XOR,
    Op.OR_EQUALS: Op.OR
}
