from modules.lexer.position import Position
from modules.visitor import symbols
from .ast_node import ASTNode

class ConstantDefineNode(ASTNode):
    def __init__(self, define_token, name, value):
        self.name = name.value
        self.value = value

        super().__init__(Position(define_token.position.start, value.position.end))

    def __repr__(self):
        return f"(DEFINE, {self.name}, AS, {self.value})"

    def interpret(self, interpreter):
        return self.save_in_symbol_table(interpreter)

    def transpile(self, transpiler):
        value = self.save_in_symbol_table(transpiler)
        return f"#define {self.name} {value}"

    def save_in_symbol_table(self, visitor):
        value = self.value.visit(visitor)
        found = visitor.symbol_table[self.name]

        if found is not None:
            found.modify(value, self)

        visitor.symbol_table[self.name] = symbols.Constant(self.name, value)

        return value
