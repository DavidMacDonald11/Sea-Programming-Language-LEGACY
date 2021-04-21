from .token_types import TT
from .token_types import BadTT
from .position import Position
from .keywords import is_keyword
from .keywords import keyword_declared_type
from ..lexer import errors

class Token:
    def __init__(self, token_type, value = None, position = None):
        self.type = token_type
        self.value = value
        self.position = Position() if position is None else position

    def __repr__(self):
        return f"{self.type}" + ("" if self.value is None else f":{self.value}")

    def matches(self, token_type, value = None):
        if value is None:
            return self.type is token_type

        return self.type is token_type and self.value == value

    def matches_type_keyword(self):
        return self.type is TT.KEYWORD and keyword_declared_type(self.value)

    @classmethod
    def match_type(cls, token_string):
        for token_type in TT:
            if token_type.value.fullmatch(token_string) is not None:
                if token_type not in (TT.KEYWORD, TT.IDENTIFIER):
                    return token_type

                return TT.KEYWORD if is_keyword(token_string) else TT.IDENTIFIER

        for bad_type in BadTT:
            if bad_type.value[0].fullmatch(token_string) is not None:
                raise bad_type.value[1]()

        raise errors.UnknownTokenError(token_string)
