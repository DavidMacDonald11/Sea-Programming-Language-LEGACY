from modules.visitor.visitor import Visitor

class Transpiler(Visitor):
    vocab_base = "Transpil"

    def visit_number_node(self, node):
        return node.token.value

    def visit_binary_operation_node(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operator = node.operation_token.type.value

        return f"({left} {operator} {right})"

    def visit_unary_operation_node(self, node):
        operator = node.operation_token.type.value
        right = self.visit(node.node)

        return f"({operator}{right})"
