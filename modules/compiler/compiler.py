from functools import cached_property
from ..compiler import errors

class Compiler:
    @cached_property
    def operators(self):
        return {
            "PLUS": "+",
            "MINUS": "-",
            "MUL": "*",
            "DIV": "/"
        }

    def __init__(self, cfile):
        self.cfile = cfile

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)

        return method(node)

    def no_visit_method(self, node):
        raise errors.UndefinedVisitMethod(node)

    def visit_NumberNode(self, node):
        return node.token.value

    def visit_BinaryOperationNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operator = self.operators[node.operation_token.type]

        return f"({left} {operator} {right})"

    def visit_UnaryOperationNode(self, node):
        operator = self.operators[node.operation_token.type]
        right = self.visit(node.node)

        return f"({operator}{right})"
