from modules.transpiler.errors import TranspilerError

class CompilerError(TranspilerError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(message)

class UndefinedVisitMethod(CompilerError):
    def __init__(self, node, message = ""):
        self.name = type(node).__name__
        super().__init__(node, message)

    def get_message(self):
        return f"No visit_{self.name} method defined."
