from modules.lexer.token_types import TT
from modules.visitor.visitor import Visitor
from ..transpiler import errors

class Transpiler(Visitor):
    vocab_base = "Transpil"

    def __init__(self, output_stream):
        self.headers = set()
        super().__init__(output_stream)

    def traverse(self, root):
        result = root.transpile(self)

        for header in self.headers:
            self.output_stream.write(f"{header}\n")

        self.output_stream.write(result)

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
