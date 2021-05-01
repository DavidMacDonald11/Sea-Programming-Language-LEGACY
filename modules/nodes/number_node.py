from .ast_node import ASTNode

class NumberNode(ASTNode):
    def __init__(self, literal):
        self.literal = literal
        super().__init__(literal.position)

    def __repr__(self):
        return f"{self.literal}"
