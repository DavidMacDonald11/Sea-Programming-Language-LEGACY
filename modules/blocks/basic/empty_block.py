from .block import Block

#pylint: disable=W0223
class EmptyBlock(Block):
    """A block that can be empty."""
    def close(self, cfile, outside = True):
        self.is_empty = False
        super().close(cfile, outside)
