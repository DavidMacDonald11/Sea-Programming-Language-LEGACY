from modules.lexer.position import Position
from modules.visitor import errors as v_errors
from .ast_node import ASTNode

class ConstantUndefineNode(ASTNode):
    def __init__(self, undefine_token, name):
        self.name = name.value
        super().__init__(Position(undefine_token.position.start, name.position.end))

    def __repr__(self):
        return f"(UNDEFINE, {self.name})"

    def interpret(self, interpreter):
        self.remove_from_symbol_table(interpreter)
        return f"Success: Undefined {self.name}"

    def transpile(self, transpiler):
        self.remove_from_symbol_table(transpiler)
        return f"#undef {self.name}"

    def remove_from_symbol_table(self, visitor):
        found = visitor.symbol_table[self.name]

        if found is None:
            raise v_errors.UndefiningUndefinedSymbolError(self, self.name)

        del visitor.symbol_table[self.name]
