from string import ascii_letters
from .token import Token

class Identifier(Token):
    @property
    def data(self):
        return self.identifier

    def __init__(self, identifier, position = None):
        self.identifier = identifier
        super().__init__(position)

    @classmethod
    def construct(cls, lexer):
        raise NotImplementedError("Identifiers must be constructed by the Keyword class.")

    @classmethod
    def symbols(cls):
        return ascii_letters + "0123456789_"
