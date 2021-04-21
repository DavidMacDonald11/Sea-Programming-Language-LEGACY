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

class ExpectedTokenError(InvalidSyntaxError):
    def __init__(self, token, expected, message = ""):
        self.expected = expected
        super().__init__(token, message)

    def get_message(self):
        return f"Expected {self.expected}."

class AtomError(ExpectedTokenError):
    def get_message(self):
        return "Expected number, identifier, or operation."

class IncorrectBlockError(InvalidSyntaxError):
    def __init__(self, expected, found, position, message = ""):
        self.expected = expected
        self.found = found
        super().__init__(SimpleNamespace(position = position), message)

    def get_message(self):
        return f"Current block is {self.found}, but in block {self.expected}."

class UndefinedContinueError(InvalidSyntaxError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(node.keyword_token)

    def get_message(self):
        return "Continue is undefined in the current block."

class UndefinedBreakError(InvalidSyntaxError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(node.keyword_token)

    def get_message(self):
        return "Break is undefined in the current block."
