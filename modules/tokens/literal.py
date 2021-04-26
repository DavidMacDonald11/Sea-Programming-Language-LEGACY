from .token import Token

class Literal(Token):
    @property
    def data(self):
        return (self.type, self.value)

    def __init__(self, literal_type, value, position = None):
        self.type = literal_type
        self.value = value
        super().__init__(position)

    @classmethod
    def construct(cls, lexer):
        pass

    @classmethod
    def allowed(cls):
        return "0123456789."
