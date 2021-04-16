from .symbol_table import SymbolTable
from ..visitor import symbols

class Visitor:
    vocab_base = None

    def __init__(self, output_stream):
        self.output_stream = output_stream
        self.symbol_table = SymbolTable()
        self.add_global_vars()

    def add_global_vars(self):
        self.symbol_table["null"] = symbols.Constant("null", 0)
        self.symbol_table["true"] = symbols.Constant("true", 1)
        self.symbol_table["false"] = symbols.Constant("false", 0)

    def traverse(self, root):
        self.output_stream.write(f"{root.visit(self)}\n")
