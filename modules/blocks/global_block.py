from .basic.empty_block import EmptyBlock

class GlobalBlock(EmptyBlock):
    def __init__(self):
        super().__init__(0, None)

    def open(self, cfile, outside = True):
        pass

    def close(self, cfile, outside = True):
        pass

    def get_declaration(self):
        pass

    def get_ending(self):
        pass

    @classmethod
    def check_match(cls, line):
        return False
