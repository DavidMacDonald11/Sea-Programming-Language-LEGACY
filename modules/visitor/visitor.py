from .symbol_table import SymbolTable
from ..visitor import symbols

class Visitor:
    vocab_bases = {
        "Compiler": "Compil",
        "Interpreter": "Interpret",
        "Transpiler": "Transpil"
    }

    def __init__(self, visitor_type, output_stream):
        self.type = visitor_type
        self.vocab_base = type(self).vocab_bases[visitor_type]
        self.output_stream = output_stream

        self.symbol_table = SymbolTable()
        self.symbol_table.interpret = visitor_type == "Interpreter"
        self.add_global_vars()

    def add_global_vars(self):
        self.symbol_table["null"] = symbols.Constant("null", 0)
        self.symbol_table["true"] = symbols.Constant("true", 1)
        self.symbol_table["false"] = symbols.Constant("false", 0)

    def traverse(self, root):
        self.output_stream.write(f"{root.visit(self)}\n")

    @classmethod
    def get_vocab_base(cls, visitor_type):
        return cls.vocab_bases[visitor_type]
