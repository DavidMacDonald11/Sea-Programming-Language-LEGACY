from .identifier import Identifier

class Keyword(Identifier):
    @property
    def keyword(self):
        return self.identifier

    @classmethod
    def construct(cls, lexer):
        token_string = lexer.take(cls.symbols())
        keyword = cls.get_keyword(token_string)

        return Identifier(token_string) if keyword is None else Keyword(keyword)

    @classmethod
    def get_keyword(cls, token_string):
        for keyword in KEYWORDS:
            if keyword == token_string:
                return keyword

        return None

    def matches_type(self, what):
        return False if what is Identifier else super().matches_type(what)

TYPE_KEYWORDS = { "int", "bool", "str", "float" }

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
    "pass",
    "return",
    "in",
    "size",
    "of"
}

KEYWORDS = TYPE_KEYWORDS | BOOL_KEYWORDS | SYNTAX_KEYWORDS
