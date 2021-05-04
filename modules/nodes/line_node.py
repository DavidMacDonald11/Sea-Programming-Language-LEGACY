from .ast_node import ASTNode

class LineNode(ASTNode):
    def __init__(self, expression, depth, no_end = False):
        self.expression = expression
        self.depth = depth
        self.no_end = no_end

        super().__init__(expression.position)

    def __repr__(self):
        return f"[{self.expression}]"

    def interpret(self, memory):
        pass

    def transpile(self, memory):
        pass
