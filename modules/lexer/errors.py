from modules.errors.errors import SeaError

class LexerError(SeaError):
    pass

class UnknownTokenError(LexerError):
    def __init__(self, token, message = ""):
        self.token = token
        super().__init__(message)

    def get_message(self):
        return f"Token \"{self.token}\" is undefined."

class IndentError(LexerError):
    def get_message(self):
        return "Indents must be 4 spaces or 1 tab."

class FloatError(LexerError):
    def get_message(self):
        return "A float cannot contain more than one decimal point."

class ImplicitCastError(LexerError):
    def __init__(self, var_type, data_type, message = ""):
        self.var_type = var_type
        self.data_type = data_type
        super().__init__(message)

    def get_message(self):
        return f"Cannot implicitly cast {self.data_type} to {self.var_type}."
