from .identifier import Identifier

class Keyword(Identifier):
    @property
    def keyword(self):
        return self.identifier

    @classmethod
    def construct(cls, lexer):
        pass

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
