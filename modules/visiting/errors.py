from errors.errors import SeaError

class VisitorError(SeaError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(node.position, message)

class IdentifierError(VisitorError):
    def __init__(self, node, identifier, message = ""):
        self.identifier = identifier
        super().__init__(node, message)

class RedeclaredIdentifierError(IdentifierError):
    def get_message(self):
        return f"Identifier {self.identifier} has already been declared in this scope."

class UndefinedIdentifierError(IdentifierError):
    def get_message(self):
        return f"Identifier {self.identifier} is undefined in any scope."
