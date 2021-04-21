from modules.lexer.keywords import cast_value_to_type
from modules.lexer.position import Position
from modules.lexer.token import Token
from modules.lexer.token_types import TT
from modules.visitor import errors as v_errors
from modules.visitor.transpiler.operators import get_c_operator
from .ast_node import ASTNode
from .number_node import NumberNode
from .binary_operation_node import BinaryOperationNode
from .symbol_access_node import SymbolAccessNode

class VariableReassignNode(ASTNode):
    def __init__(self, variable, operation, value = None, left = False):
        self.variable = variable
        self.var_name = variable.value
        self.operation = operation
        self.operator = operation.type
        self.value = value
        self.left = left

        super().__init__(variable.position)

    def __repr__(self):
        value = "" if self.value is None else f", {self.value}"

        if self.left:
            return f"({self.operation}, {self.variable}{value})"

        return f"({self.variable}, {self.operation}{value})"

    def visit(self, visitor):
        if self.operator is TT.EQUALS:
            return super().visit(visitor)

        if self.operator in (TT.INCREMENT, TT.DECREMENT):
            return self.visit_unary(visitor)

        position = Position(self.operation.position.start)
        operation = Token(OPERATOR_FUNC[self.operator], None, position)
        assign = Token(TT.EQUALS, None, position)

        node = SymbolAccessNode(self.variable)
        node = BinaryOperationNode(node, operation, self.value)
        node = VariableReassignNode(self.variable, assign, node)

        return node.visit(visitor)

    def visit_unary(self, visitor):
        if visitor.type == "Transpiler":
            return self.transpile_unary(visitor)

        return self.interpret_unary(visitor)

    def interpret(self, interpreter):
        if self.operator is not TT.EQUALS:
            return self.visit(interpreter)

        return self.save_in_symbol_table(interpreter, True)

    def interpret_unary(self, interpreter):
        position = Position(self.operation.position)
        token_type = TT.PLUS_EQUALS if self.operator is TT.INCREMENT else TT.MINUS_EQUALS
        operation = Token(token_type, None, position)
        one = NumberNode(Token(TT.INT, 1, position))

        node = VariableReassignNode(self.variable, operation, one)

        if self.left:
            return node.visit(interpreter)

        value = SymbolAccessNode(self.variable).interpret(interpreter)
        node.visit(interpreter)

        return value

    def transpile(self, transpiler):
        if self.operator is not TT.EQUALS:
            return self.visit(transpiler)

        value = self.save_in_symbol_table(transpiler)
        return f"({self.var_name} = {value})"

    def transpile_unary(self, _):
        operator = get_c_operator(self)

        if self.left:
            return f"({operator}{self.var_name})"

        return f"({self.var_name}{operator})"

    def save_in_symbol_table(self, visitor, cast = False):
        value = self.value.visit(visitor)
        found = visitor.symbol_table[self.var_name]

        if found is None:
            raise v_errors.UndefinedSymbolError(self, self.var_name)

        if cast:
            value = cast_value_to_type(found.type, value)

        found.modify(value, self)

        return value

OPERATOR_FUNC = {
    TT.PLUS_EQUALS: TT.PLUS,
    TT.MINUS_EQUALS: TT.MINUS,
    TT.MULTIPLY_EQUALS: TT.MULTIPLY,
    TT.POWER_EQUALS: TT.POWER,
    TT.DIVIDE_EQUALS: TT.DIVIDE,
    TT.MODULO_EQUALS: TT.MODULO,
    TT.LSHIFT_EQUALS: TT.LSHIFT,
    TT.RSHIFT_EQUALS: TT.RSHIFT,
    TT.AND_EQUALS: TT.AND,
    TT.XOR_EQUALS: TT.XOR,
    TT.OR_EQUALS: TT.OR
}
