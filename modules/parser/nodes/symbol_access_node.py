from modules.visitor import symbols
from modules.visitor import errors as v_errors
from .ast_node import ASTNode

class SymbolAccessNode(ASTNode):
    def __init__(self, symbol):
        self.symbol = symbol
        self.name = symbol.value
        super().__init__(symbol.position)

    def __repr__(self):
        return f"{self.symbol}"

    def interpret(self, interpreter):
        symbol = self.get_from_symbol_table(interpreter)
        return symbol.value

    def transpile(self, transpiler):
        symbol = self.get_from_symbol_table(transpiler)

        if isinstance(symbol, symbols.ConstantVariable):
            return symbol.value

        return symbol.name

    def get_from_symbol_table(self, visitor):
        symbol = visitor.symbol_table[self.name]

        if symbol is None:
            raise v_errors.UndefinedSymbolError(self, self.name)

        return symbol
