from types import SimpleNamespace
from modules.helpers.errors import SeaError

class ParserError(SeaError):
    def __init__(self, token, message = ""):
        self.token = token
        super().__init__(message)

    def get_position(self):
        return self.token.position

class InvalidSyntaxError(ParserError):
    def get_message(self):
        return "Syntax is invalid."

class AtomError(InvalidSyntaxError):
    def get_message(self):
        return "Token must be an int or a float."

class NoClosingParenthesisError(InvalidSyntaxError):
    def get_message(self):
        return "Missing closing parenthesis."

class NoIdentifierError(InvalidSyntaxError):
    def get_message(self):
        return "Expected an identifier."

class NoEqualsError(InvalidSyntaxError):
    def get_message(self):
        return "Expected '='."

class IncorrectBlockError(InvalidSyntaxError):
    def __init__(self, expected, found, position, message = ""):
        self.expected = expected
        self.found = found
        super().__init__(SimpleNamespace(position = position), message)

    def get_message(self):
        return f"Current block is {self.found}, but in block {self.expected}."

class NoLineTerminationError(InvalidSyntaxError):
    def get_message(self):
        return "Expected a newline or end of file."

class NoColonError(InvalidSyntaxError):
    def get_message(self):
        return "Expected ':'."

class NoAsError(InvalidSyntaxError):
    def get_message(self):
        return "Expected 'as'."

class TernaryError(InvalidSyntaxError):
    def __init__(self, missing_if, token, message = ""):
        self.missing_if = missing_if
        super().__init__(token, message)

    def get_message(self):
        return f"Expected {'if' if self.missing_if else 'else'}."
