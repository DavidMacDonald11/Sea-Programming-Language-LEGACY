from modules.lexer.tokens import TT
from modules.visitor.visitor import Visitor
from modules.lexer.keywords import cast_value_to_type
from ..interpreter import arithmetic
from ..interpreter import errors

unary_operator_func = {
    TT.PLUS: arithmetic.pos_num,
    TT.MINUS: arithmetic.neg_num
}

binary_operator_func = {
    TT.PLUS: arithmetic.add_nums,
    TT.MINUS: arithmetic.sub_nums,
    TT.MULTIPLY: arithmetic.mul_nums,
    TT.POWER: arithmetic.pow_nums,
    TT.DIVIDE: arithmetic.div_nums
}

class Interpreter(Visitor):
    vocab_base = "Interpret"

    def visit_number_node(self, node):
        value = node.token.value
        return int(value) if node.token.type is TT.INT else float(value)

    def visit_variable_access_node(self, node):
        var_name = node.variable_token.value
        value = self.symbol_table.get(var_name)

        if value is None:
            raise errors.UndefinedVariableError(node)

        return value

    def visit_variable_assign_node(self, node):
        var_type = node.keyword_token.value
        var_name = node.variable_token.value

        value = self.visit(node.value_node)
        value = cast_value_to_type(var_type, value)

        self.symbol_table.set(var_type, var_name, value)

        return value

    def visit_binary_operation_node(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operator = node.operation_token.type

        try:
            return binary_operator_func[operator](left, right)
        except errors.NumericalError as error:
            error.node = node.right_node
            raise error

    def visit_unary_operation_node(self, node):
        operator = node.operation_token.type
        right = self.visit(node.node)

        return unary_operator_func[operator](right)
