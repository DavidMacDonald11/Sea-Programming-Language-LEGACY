from modules.parser.text import generate
from ..abstract.statement import Statement

class PassStatement(Statement):
    @classmethod
    def get_structure(cls):
        return ["// pass"]

    @classmethod
    def get_pattern(cls):
        return generate.keyword_pattern("pass")
