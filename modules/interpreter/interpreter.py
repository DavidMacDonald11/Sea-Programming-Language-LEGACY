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

ternary_operator_func = {

}

ternary_operator_keyword_func = {
    ("if", "else"): (lambda x, c, y: x if c else y)
}

class Interpreter(Visitor):
    vocab_base = "Interpret"

    def __init__(self, output_stream):
        super().__init__(output_stream)
        self.symbol_table.interpret = True

    def visit_eof_node(self, node):
        return ""

    def visit_number_node(self, node):
        value = node.token.value
        return int(value) if node.token.type is TT.INT else float(value)

    def visit_variable_access_node(self, node):
        var = self.symbol_table.safe_get(node)
        return var.casted_value

    def visit_variable_assign_node(self, node):
        value = self.visit(node.value)
        self.symbol_table.safe_set(node, value, True)

        return value

    def visit_unary_operation_node(self, node):
        operation = node.operation
        operator = operation.type
        right = self.visit(node.right)

        if operator is TT.KEYWORD:
            return unary_operator_keyword_func[operation.value](right)

        return unary_operator_func[operator](right)

    def visit_binary_operation_node(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        operation = node.operation
        operator = operation.type

        try:
            if operator is TT.KEYWORD:
                return binary_operator_keyword_func[operation.value](left, right)

            return binary_operator_func[operator](left, right)
        except errors.NumericalError as error:
            error.node = node.right_node
            raise error

    def visit_ternary_operation_node(self, node):
        left = self.visit(node.left)
        left_operation = node.left_operation
        middle = self.visit(node.middle)
        right_operation = node.right_operation
        right = self.visit(node.right)

        inputs = (left, middle, right)
        operation_value = (left_operation.value, right_operation.value)
        operator = (left_operation.type, right_operation.type)

        if operator == (TT.KEYWORD, TT.KEYWORD):
            return ternary_operator_keyword_func[operation_value](*inputs)

        return ternary_operator_func[(left_operation, right_operation)](*inputs)

    def visit_line_node(self, node):
        return self.visit(node.expression)

    def visit_sequential_operation_node(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if right == "":
            return left

        return f"{left}\n{right}"

    def visit_if_node(self, node):
        for condition, expression in node.cases:
            condition_value = self.visit(condition)

            if condition_value:
                return self.visit(expression)

        if node.else_case:
            return self.visit(node.else_case)

        return ""
