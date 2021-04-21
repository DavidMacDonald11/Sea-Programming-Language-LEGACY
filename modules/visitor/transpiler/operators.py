from modules.lexer.token_types import TT
from ...visitor import errors

def get_c_operator(node):
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
    TT.INCREMENT: "++",
    TT.DECREMENT: "--",
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
