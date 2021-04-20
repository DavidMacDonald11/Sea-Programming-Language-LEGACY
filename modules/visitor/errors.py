from modules.helpers import errors

class VisitorError(errors.SeaError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(message)

    def get_position(self):
        return self.node.position

class SymbolError(VisitorError):
    def __init__(self, node, symbol, message = ""):
        self.symbol = symbol
        super().__init__(node, message)

class VariableError(VisitorError):
    def __init__(self, node, message = ""):
        self.variable_name = node.variable.value
        super().__init__(node, message)

class UndefinedSymbolError(SymbolError):
    def get_message(self):
        return f"{self.symbol} is undefined."

class RedeclaredVariableError(VariableError):
    def get_message(self):
        return f"{self.variable_name} has already been declared."

class ModifyingConstantError(SymbolError):
    def get_message(self):
        return f"Attempted to modify constant value {self.symbol.name}."

class UndefiningUndefinedSymbolError(UndefinedSymbolError):
    def get_message(self):
        return f"{self.symbol} is already undefined and cannot be undefined."

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

class TranspilerError(VisitorError):
    pass

class UnimplementedOperationError(TranspilerError):
    def __init__(self, node, message = ""):
        self.token_type = node.operation.type
        super().__init__(node, message)

    def get_message(self):
        return f"Token type {self.token_type} is unknown to the transpiler."
