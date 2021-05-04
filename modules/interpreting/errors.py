from errors.errors import SeaError

class InterpreterError(SeaError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(node.position, message)
