from modules.transpiler import conditionals
from ..basic.block import Block

class WhileLoop(Block):
    def get_declaration(self):
        line = self.declaration.replace("while", "", 1)[:-1].strip()
        line = conditionals.transpile(line)
        return f"while({line}) {{"

    def get_ending(self):
        return "}\n"

    @classmethod
    def check_match(cls, line):
        return cls.matches_pattern(cls.declaration_pattern, line)

    @classmethod
    def get_declaration_pattern(cls):
        return r"while .+:"
