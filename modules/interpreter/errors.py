from modules.visitor.errors import VisitorError

class InterpreterError(VisitorError):
    pass

class NumericalError(InterpreterError):
    pass

class DivideByZeroError(NumericalError):
    def get_message(self):
        return "Cannot divide by 0."
