from modules.lexer.tokens import TT
from modules.visitor.visitor import Visitor
from modules.lexer.keywords import cast_value_to_type
from ..transpiler import errors

C_OPERATORS = {
    TT.PLUS: "+",
    TT.MINUS: "-",
    TT.MULTIPLY: "*",
    TT.DIVIDE: "/"
}

def get_c_operator(node):
    try:
        return C_OPERATORS[node.operation_token.type]
    except KeyError as e:
        raise errors.UnimplementedOperationError(node) from e

class Transpiler(Visitor):
    vocab_base = "Transpil"

    def __init__(self, output_stream):
        self.headers = set()
        super().__init__(output_stream)

    def traverse(self, root):
        result = self.visit(root)

        for header in self.headers:
            self.output_stream.write(f"{header}\n")

        self.output_stream.write(result)

    def visit_number_node(self, node):
        return node.token.value

    def visit_variable_access_node(self, node):
        return node.variable_token.value

    def visit_variable_assign_node(self, node):
        var_type = node.keyword_token.value
        var_name = node.variable_token.value
        value = self.visit(node.value_node)

        cast_value_to_type(var_type, value)

        return f"{var_type} {var_name} = {value}"

    def visit_binary_operation_node(self, node):
        if node.operation_token.type is TT.POWER:
            left = node.left_node.token
            right = node.right_node.token

            return self.arithmetic_power(left, right)

        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operator = get_c_operator(node)

        parens = operator in "+-"

        return f"{'(' if parens else ''}{left} {operator} {right}{')' if parens else ''}"

    def visit_unary_operation_node(self, node):
        operator = get_c_operator(node)
        right = self.visit(node.node)

        return f"{operator}{right}"

    def arithmetic_power(self, left, right):
        self.headers.add("#include <math.h>")

        if left.type is TT.INT and right.type is TT.INT:
            return f"((int)powf({left.value}, {right.value}))"

        return f"powl({left.value}, {right.value})"
