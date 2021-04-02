from modules.transpiler.errors import TranspilerError

class LexerError(TranspilerError):
    pass

class IndentError(LexerError):
    def get_message(self):
        return "Indents must be 4 spaces or 1 tab."

class FloatError(LexerError):
    def get_message(self):
        return "A float cannot contain more than one decimal point."
