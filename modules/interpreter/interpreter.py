from modules.lexer.tokens import TT
from modules.visitor.visitor import Visitor
from ..interpreter import arithmetic
from ..interpreter import errors

unary_operator_func = {
    TT.PLUS: (lambda x: +x),
    TT.MINUS: (lambda x: -x)
}

unary_operator_keyword_func = {
    "not": (lambda x: not x)
}

binary_operator_func = {
    TT.PLUS: (lambda x, y: x + y),
    TT.MINUS: (lambda x, y: x - y),
    TT.MULTIPLY: (lambda x, y: x * y),
    TT.POWER: arithmetic.pow_nums,
    TT.DIVIDE: arithmetic.div_nums,
    TT.EQ: (lambda x, y: x == y),
    TT.NE: (lambda x, y: x != y),
    TT.LT: (lambda x, y: x < y),
    TT.GT: (lambda x, y: x > y),
    TT.LTE: (lambda x, y: x <= y),
    TT.GTE: (lambda x, y: x >= y)
}

binary_operator_keyword_func = {
    "and": (lambda x, y: x and y),
    "or": (lambda x, y: x or y)
}

class Interpreter(Visitor):
    vocab_base = "Interpret"

    def __init__(self, output_stream):
        super().__init__(output_stream)
        self.symbol_table.interpret = True

    def visit_number_node(self, node):
        value = node.token.value
        return int(value) if node.token.type is TT.INT else float(value)

    def visit_variable_access_node(self, node):
        var = self.symbol_table.safe_get(node)
        return var.casted_value

    def visit_variable_assign_node(self, node):
        value = self.visit(node.value_node)
        self.symbol_table.safe_set(node, value, True)

        return value

    def visit_binary_operation_node(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operation_token = node.operation_token
        operator = operation_token.type

        try:
            if operator is TT.KEYWORD:
                return binary_operator_keyword_func[operation_token.value](left, right)

            return binary_operator_func[operator](left, right)
        except errors.NumericalError as error:
            error.node = node.right_node
            raise error

    def visit_unary_operation_node(self, node):
        operation_token = node.operation_token
        operator = operation_token.type
        right = self.visit(node.node)

        if operator is TT.KEYWORD:
            return unary_operator_keyword_func[operation_token.value](right)

        return unary_operator_func[operator](right)
