from errors.errors import SeaError

class LexerError(SeaError):
    lexer = None

    def __init__(self, position = None, message = ""):
        if position is None:
            position = type(self).lexer.position.copy()

        super().__init__(position, message)
