from modules.lexer.token_types import TT
from .ast_node import ASTNode

class NumberNode(ASTNode):
    def __init__(self, token):
        self.token = token
        super().__init__(token.position)

    def __repr__(self):
        return f"{self.token}"

    def interpret(self, interpreter):
        value = self.token.value
        return int(value) if self.token.type is TT.INT else float(value)

    def transpile(self, transpiler):
        return self.token.value
