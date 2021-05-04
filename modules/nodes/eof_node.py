from .ast_node import ASTNode

class EOFNode(ASTNode):
    def __init__(self, eof_token):
        self.eof_token = eof_token
        super().__init__(eof_token.position)

    def __repr__(self):
        return f"{self.eof_token}"

    def interpret(self, memory):
        return ""

    def transpile(self, memory):
        return ""
