from visiting.errors import VisitorError

class InterpreterError(VisitorError):
    pass

class UndefinedOperationError(InterpreterError):
    def __init__(self, node, operation, message = ""):
        self.operation = operation
        super().__init__(node, message)

    def get_message(self):
        return f"{self.operation} is undefined."

class DivideByZeroError(InterpreterError):
    def get_message(self):
        return "Cannot divide nor mod by zero."

class BitwiseOperationTypeError(InterpreterError):
    def get_message(self):
        return "Bitwise operations can only be used with integers."
