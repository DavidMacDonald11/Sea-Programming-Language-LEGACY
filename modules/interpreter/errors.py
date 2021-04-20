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
        return "Cannot divide or mod by 0."

class BitwiseOperationTypeError(InterpreterError):
    def get_message(self):
        return "Bitwise operations can only be used with integers."
