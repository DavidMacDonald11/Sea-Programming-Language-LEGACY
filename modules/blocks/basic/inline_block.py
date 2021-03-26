from .block import Block

#pylint: disable=W0223
class InlineBlock(Block):
    """A scope that can start or stop beside other declarations."""
    def get_declaration(self):
        return self.declaration

    def close(self, cfile, outside = False):
        super().close(cfile, outside)
