from modules.lexer.token_types import TT
from .symbol_table import SymbolTable
from ..visitor import symbols
from ..visitor import errors

class Visitor:
    vocab_bases = {
        "Compiler": "Compil",
        "Interpreter": "Interpret",
        "Transpiler": "Transpil"
    }

    def __init__(self, visitor_type, output_stream):
        self.type = visitor_type
        self.headers = set()
        self.output_stream = output_stream

        self.symbol_table = SymbolTable()
        self.symbol_table.interpret = visitor_type == "Interpreter"
        self.add_global_vars()

    def add_global_vars(self):
        self.symbol_table["null"] = symbols.Constant("null", 0)
        self.symbol_table["true"] = symbols.Constant("true", 1)
        self.symbol_table["false"] = symbols.Constant("false", 0)

    def traverse(self, root):
        result = root.visit(self)

        for header in self.headers:
            self.output_stream.write(f"{header}\n")

        self.output_stream.write(f"{result}\n")

    @classmethod
    def get_vocab_base(cls, visitor_type):
        return cls.vocab_bases[visitor_type]

    @classmethod
    def get_operator(cls, node):
        try:
            operation = node.operation

            if operation.type is TT.KEYWORD:
                return C_KEYWORD_OPERATORS[operation.value]

            return C_OPERATORS[operation.type]
        except KeyError as e:
            raise errors.UnimplementedOperationError(node) from e

C_KEYWORD_OPERATORS = {
    "not": "!",
    "and": "&&",
    "or": "||"
}

C_OPERATORS = {
    TT.PLUS: "+",
    TT.MINUS: "-",
    TT.MULTIPLY: "*",
    TT.DIVIDE: "/",
    TT.MODULO: "%",
    TT.EQ: "==",
    TT.NE: "!=",
    TT.LT: "<",
    TT.GT: ">",
    TT.LTE: "<=",
    TT.GTE: ">=",
    TT.NOT: "~",
    TT.LSHIFT: "<<",
    TT.RSHIFT: ">>",
    TT.AND: "&",
    TT.XOR: "^",
    TT.OR: "|"
}
