from modules.transpiler import conditionals
from ..basic.endable_block import EndableBlock

class DoWhileLoop(EndableBlock):
    def get_declaration(self):
        return "do {"

    def get_ending(self):
        ending = super().get_ending()
        line = ending.replace("while", "", 1).strip()
        line = conditionals.transpile(line)

        return f"}} while({line});"

    @classmethod
    def check_match(cls, line):
        return line == "do:"

    @classmethod
    def get_ending_pattern(cls):
        return r"\s*while [^:]+"
