from tokens.operator import Operator
from visiting import errors

def get_c_operator(node):
    try:
        if isinstance(node.operation, Operator):
            return node.operation.data.value

        return C_OPERATORS[node.operation.data]
    except KeyError as e:
        raise errors.UnimplementedOperationError(node) from e

C_OPERATORS = {
    "not": "!",
    "and": "&&",
    "or": "||"
}
