from modules.errors import errors
from .helpers import convert_to_camel_case

class VisitorError(errors.SeaError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(message)

    def get_position(self):
        return self.node.position

class UndefinedVisitMethod(VisitorError):
    def __init__(self, node, message = ""):
        self.name = type(node).__name__
        super().__init__(node, message)

    def get_message(self):
        return f"No visit{convert_to_camel_case(self.name)} method defined."

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
