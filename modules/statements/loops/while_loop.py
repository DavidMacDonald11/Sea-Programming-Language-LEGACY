from modules.parser.text import generate
from ..abstract.statement import Statement

class WhileStatement(Statement):
    @classmethod
    def get_structure(cls):
        return ["while(", None, ")"]

    @classmethod
    def get_pattern(cls):
        return generate.keyword_pattern("while")
