from errors.errors import SeaError

class VisitorError(SeaError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(node.position, message)

class RedeclaredIdentifierError(VisitorError):
    def __init__(self, node, identifier, message = ""):
        self.identifier = identifier
        super().__init__(node, message)

    def get_message(self):
        return
