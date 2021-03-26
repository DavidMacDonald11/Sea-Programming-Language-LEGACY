from .basic.block import Block

class FunctionBlock(Block):
    def get_declaration(self):
        line = self.declaration[:-1]

        parts = line.split("(")
        parts[1] = parts[1][:-1]

        return f"{parts[0]}({parts[1]}) {{"

    def get_ending(self):
        return "}\n"

    @classmethod
    def check_match(cls, line):
        return cls.matches_pattern(cls.declaration_pattern, line)

    @classmethod
    def get_declaration_pattern(cls):
        return r"[^():]+\([^():]*\):"
