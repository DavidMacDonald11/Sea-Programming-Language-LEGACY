from modules.lexer.keywords import cast_value_to_type
from modules.lexer.position import Position
from modules.lexer.token import Token
from modules.lexer.token_types import TT
from modules.visitor import errors as v_errors
from .ast_node import ASTNode
from .binary_operation_node import BinaryOperationNode
from .symbol_access_node import SymbolAccessNode

class VariableReassignNode(ASTNode):
    def __init__(self, variable, operation, value):
        self.variable = variable
        self.var_name = variable.value
        self.operation = operation
        self.operator = operation.type
        self.value = value

        super().__init__(variable.position)

    def __repr__(self):
        return f"({self.variable}, {self.operation}, {self.value})"

    def visit(self, visitor):
        if self.operator is TT.EQUALS:
            return super().visit(visitor)

        position = Position(self.operation.position.start)
        operation = Token(OPERATOR_FUNC[self.operator], None, position)
        assign = Token(TT.EQUALS, None, position)

        node = SymbolAccessNode(self.variable)
        node = BinaryOperationNode(node, operation, self.value)
        node = VariableReassignNode(self.variable, assign, node)

        return node.visit(visitor)

    def interpret(self, interpreter):
        return self.save_in_symbol_table(interpreter, True)

    def transpile(self, transpiler):
        value = self.save_in_symbol_table(transpiler)
        return f"({self.var_name} = {value})"

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
