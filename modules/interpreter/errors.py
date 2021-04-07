from modules.visitor.errors import VisitorError

class InterpreterError(VisitorError):
    pass

class NumericalError(InterpreterError):
    pass

class UndefinedOperationError(NumericalError):
    def get_message(self):
        return f"{self.message} is undefined."

class DivideByZeroError(UndefinedOperationError):
    def get_message(self):
        return "Cannot divide by 0."

class VariableError(InterpreterError):
    def __init__(self, node, message = ""):
        self.variable_name = node.variable_token.value
        super().__init__(node, message)

class UndefinedVariableError(VariableError):
    def get_message(self):
        return f"{self.variable_name} is undefined."
