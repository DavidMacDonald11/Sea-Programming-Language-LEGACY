from .identifier import Identifier

class Keyword(Identifier):
    @property
    def keyword(self):
        return self.identifier

    @classmethod
    def construct(cls, lexer):
        token_string = lexer.take_token_string(cls.allowed())
        keyword = cls.get_keyword(token_string)

        if keyword is None:
            return super().construct_from_child(lexer, token_string)

        return Keyword(keyword)

    @classmethod
    def get_keyword(cls, token_string):
        for keyword in KEYWORDS:
            if keyword == token_string:
                return keyword

        return None

TYPE_KEYWORDS = { "int", "float", "bool" }
BOOL_KEYWORDS = { "not", "and", "or" }

SYNTAX_KEYWORDS = {
    "if",
    "elif",
    "else",
    "for",
    "while",
    "do",
    "break",
    "continue",
    "pass"
}

KEYWORDS = TYPE_KEYWORDS | BOOL_KEYWORDS | SYNTAX_KEYWORDS
