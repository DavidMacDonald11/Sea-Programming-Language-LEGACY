from modules.lexer.tokens import TT
from modules.visitor.visitor import Visitor
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
