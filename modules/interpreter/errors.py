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
