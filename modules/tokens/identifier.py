import string
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
        raise NotImplementedError()

    @classmethod
    def construct_from_child(cls, _, token_string):
        return Identifier(token_string)

    @classmethod
    def allowed(cls):
        return string.ascii_letters + "0123456789_"
