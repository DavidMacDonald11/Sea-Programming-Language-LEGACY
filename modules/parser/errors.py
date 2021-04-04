from modules.errors.errors import SeaError

class ParserError(SeaError):
    def __init__(self, token, message = ""):
        self.token = token
        super().__init__(message)

class InvalidSyntaxError(ParserError):
    def get_message(self):
        return "Syntax is invalid."

class FactorError(InvalidSyntaxError):
    def get_message(self):
        return "Token must be an int or a float."

class NoClosingParenthesisError(InvalidSyntaxError):
    def get_message(self):
        return "Missing closing parenthesis."
