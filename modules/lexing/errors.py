from errors.errors import SeaError

class LexerError(SeaError):
    lexer = None

    def __init__(self, position = None, message = ""):
        if position is None:
            position = type(self).lexer.position.copy()

        super().__init__(position, message)

class UnknownSymbolError(LexerError):
    def __init__(self, symbol, message = ""):
        self.symbol = symbol
        super().__init__(message = message)

    def get_message(self):
        return f"Symbol \"{self.symbol}\" is unknown to the lexer."

class UnknownOperatorError(LexerError):
    def __init__(self, operator, message = ""):
        self.operator = operator
        super().__init__(message = message)

    def get_message(self):
        return f"Operator \"{self.operator}\" is unknown to the lexer."

class IndentError(LexerError):
    def get_message(self):
        return "Indents must be 4 spaces or 1 tab."

class FloatError(LexerError):
    def get_message(self):
        return "A float cannot contain more than one decimal point."

class UnterminatedStringError(LexerError):
    def get_message(self):
        return "Strings must be closed with the character used to open them."
