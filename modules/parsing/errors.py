from errors.errors import SeaError

class ParserError(SeaError):
    parser = None

    def __init__(self, position = None, message = ""):
        if position is None:
            position = type(self).parser.token.position.copy()

        super().__init__(position, message)

class IncorrectBlockError(ParserError):
    def __init__(self, depth, position, message = ""):
        self.depth = depth
        self.expected = type(self).parser.depth
        super().__init__(position, message)

    def get_message(self):
        return f"Found {self.depth} indents, but expected {self.expected}."

class ExpectedTokenError(ParserError):
    def __init__(self, expected, message = ""):
        self.expected = expected
        super().__init__(None, message)

    def get_message(self):
        return f"Expected {self.expected}."

class AtomError(ParserError):
    def get_message(self):
        return "Token is unrecognized by the parser."

class EmptyBlockError(ParserError):
    def get_message(self):
        return "Blocks cannot be empty. Consider using pass."