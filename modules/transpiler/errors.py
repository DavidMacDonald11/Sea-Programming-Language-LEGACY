from modules.visitor.errors import VisitorError

class TranspilerError(VisitorError):
    pass

class UnimplementedOperationError(TranspilerError):
    def __init__(self, node, message = ""):
        self.token_type = node.operation_token.type
        super().__init__(node, message)

    def get_message(self):
        return f"Token type {self.token_type} is unknown to the transpiler."
