from .ast_node import ASTNode

class NumberNode(ASTNode):
    def __init__(self, literal):
        self.literal = literal
        self.value = self.literal.get_consistent_value()
        super().__init__(literal.position)

    def __repr__(self):
        return f"{self.literal}"

    def interpret(self, memory):
        return self.value

    def transpile(self, memory):
        return str(self.value)
