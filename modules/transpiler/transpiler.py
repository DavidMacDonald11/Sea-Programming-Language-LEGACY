from modules.lexer.tokens import TT
from modules.parser import nodes
from modules.visitor.visitor import Visitor
from modules.visitor.symbol_table import SymbolTable
from ..transpiler import errors

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
    TT.EQ: "==",
    TT.NE: "!=",
    TT.LT: "<",
    TT.GT: ">",
    TT.LTE: "<=",
    TT.GTE: ">="
}

def get_c_operator(node):
    try:
        operation = node.operation

        if operation.type is TT.KEYWORD:
            return C_KEYWORD_OPERATORS[operation.value]

        return C_OPERATORS[operation.type]
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

    def visit_eof_node(self, node):
        return ""

    def visit_number_node(self, node):
        return node.token.value

    def visit_variable_access_node(self, node):
        var = self.symbol_table.safe_get(node)

        if var.is_constant:
            return var.value

        return var.name

    def visit_variable_assign_node(self, node):
        var_type = node.type.value
        var_name = node.variable.value

        value = self.visit(node.value)

        if var_type == "bool":
            var_type = "int"

        self.symbol_table.safe_set(node, value, True)

        return f"{var_type} {var_name} = {value}"

    def visit_unary_operation_node(self, node):
        operator = get_c_operator(node)
        right = self.visit(node.right)

        return f"{operator}{right}"

    def visit_binary_operation_node(self, node):
        if node.operation is None:
            left = self.visit(node.left)
            right = self.visit(node.right)

            return f"{left}\n{right}"

        if node.operation.type is TT.POWER:
            left = node.left.token
            right = node.right.token

            return self.arithmetic_power(left, right)

        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = get_c_operator(node)

        return f"({left} {operator} {right})"

    def visit_ternary_operation_node(self, node):
        left = self.visit(node.left)
        left_operation = node.left_operation
        middle = self.visit(node.middle)
        right_operation = node.right_operation
        right = self.visit(node.right)

        operation_value = (left_operation.value, right_operation.value)
        operator = (left_operation.type, right_operation.type)

        if operator != (TT.KEYWORD, TT.KEYWORD) or operation_value != ("if", "else"):
            raise errors.UnimplementedOperationError(node)

        return f"{middle} ? {left} : {right}"

    def visit_line_node(self, node):
        is_if = node.is_if
        indent = "\t" * node.depth

        if isinstance(node.expression, nodes.IfNode):
            self.symbol_table = SymbolTable(type(self), self.symbol_table)
            expression = self.visit(node.expression)
            self.symbol_table = self.symbol_table.parent
        else:
            expression = self.visit(node.expression)

        return f"{indent}{expression}{'' if is_if else ';'}\n"

    def visit_sequential_operation_node(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        return f"{left}\n{right}"

    def visit_if_node(self, node):
        statement = ""
        first = True

        for condition, expression in node.cases:
            condition_value = self.visit(condition)

            if first:
                statement += f"if({condition_value})\n{{\n"
                first = False
            else:
                statement += f"else if({condition_value})\n{{\n"

            statement += f"{self.visit(expression)}"
            statement += "}\n"

        if node.else_case:
            statement += f"else\n{{\n{self.visit(node.else_case)}}}\n"

        return statement

    def arithmetic_power(self, left, right):
        self.headers.add("#include <math.h>")

        if left.type is TT.INT and right.type is TT.INT:
            return f"((int)powf({left.value}, {right.value}))"

        return f"powl({left.value}, {right.value})"
