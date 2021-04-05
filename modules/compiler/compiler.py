from modules.visitor.visitor import Visitor

class Compiler(Visitor):
    vocab_base = "Compil"

    def visit_number_node(self, node):
        pass

    def visit_binary_operation_node(self, node):
        pass

    def visit_unary_operation_node(self, node):
        pass
