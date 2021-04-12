from modules.errors.errors import SeaError

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
    def __init__(self, expected, found, token, message = ""):
        self.expected = expected
        self.found = found
        super().__init__(token, message)

    def get_message(self):
        return f"Current block is {self.found}, but in block {self.expected}."

class NoLineTerminationError(InvalidSyntaxError):
    def get_message(self):
        return "Expected a newline or end of file."
