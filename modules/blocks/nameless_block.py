from .basic.block import Block

class NamelessBlock(Block):
    def get_declaration(self):
        return "{"

    def get_ending(self):
        return "}\n"

    @classmethod
    def check_match(cls, line):
        return line == "block:"
