from functools import cached_property
from modules.lexer.tokens import TT
from modules.visitor.visitor import Visitor
from ..interpreter import errors

class Interpreter(Visitor):
    vocab_base = "Interpret"

    @cached_property
    def unary_operator_func(self):
        return {
            TT.PLUS: self.pos_num,
            TT.MINUS: self.neg_num
        }

    @cached_property
    def binary_operator_func(self):
        return {
            TT.PLUS: self.add_nums,
            TT.MINUS: self.sub_nums,
            TT.STAR: self.mul_nums,
            TT.SLASH: self.div_nums
        }

    def visit_number_node(self, node):
        value = node.token.value
        return int(value) if node.token.type is TT.INT else float(value)

    def visit_binary_operation_node(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operator = node.operation_token.type

        try:
            return self.binary_operator_func[operator](left, right)
        except errors.DivideByZeroError as error:
            error.node = node.right_node
            raise error

    def visit_unary_operation_node(self, node):
        operator = node.operation_token.type
        right = self.visit(node.node)

        return self.unary_operator_func[operator](right)

    def neg_num(self, num):
        return -num

    def pos_num(self, num):
        return num

    def add_nums(self, left, right):
        return left + right

    def sub_nums(self, left, right):
        return left - right

    def mul_nums(self, left, right):
        return left * right

    def div_nums(self, left, right):
        if right == 0:
            raise errors.DivideByZeroError(None)

        return left / right
