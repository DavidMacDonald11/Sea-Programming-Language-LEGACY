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
        return self.expression.interpret(memory)

    def transpile(self, memory):
        memory.line_depth = self.depth
        expression = self.expression.transpile(memory)
        indent = "\t" * self.depth

        return f"{indent}{expression}{'' if self.no_end else ';'}"
