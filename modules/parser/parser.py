from modules.lexer.token_types import TT
from .grammar.block import MAKE_FUNCS
from .grammar.line import make_line
from .nodes.collection import NODES
from ..parser import errors

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_i = -1
        self.token = None
        self.advance()

        self.depth = 0

    def take_token(self):
        token = self.token
        self.advance()
        return token

    def advance(self):
        self.token_i += 1

        if self.token_i < len(self.tokens):
            self.token = self.tokens[self.token_i]

        return self.token

    def parse(self):
        line = make_line(self, **MAKE_FUNCS)

        if isinstance(line, NODES.EOFNode):
            return line

        return NODES.SequentialOperationNode(line, self.parse())

    def expecting(self, *valid_token_types):
        if self.token.type not in valid_token_types:
            raise errors.ExpectedTokenError(self.token, valid_token_types)

        return self.take_token()

    def expecting_keyword(self, *valid_keywords):
        if self.token.type is not TT.KEYWORD or self.token.value not in valid_keywords:
            raise errors.ExpectedTokenError(self.token, valid_keywords)

        return self.take_token()
