from .block import Block
from .block import EmptyBlockError

#pylint: disable=W0223
class VerbatumBlock(Block):
    """A block that does not transpile its lines."""
    def close(self, cfile, outside = True):
        try:
            super().close(cfile, outside)
        except EmptyBlockError as e:
            raise EmptyVerbatumBlockError(type(self)) from e

    def indent_line(self, line = "", outside = False):
        if outside:
            return super().indent_line(line, outside)

        return line

    def write_line(self, cfile, line = "", outside = False):
        if outside:
            super().write_line(cfile, line, outside)
            return

        line = line.rstrip()
        cfile.write(f"{self.indent_line(line)}\n")

class EmptyVerbatumBlockError(EmptyBlockError):
    def get_message(self):
        return f"{self.block_name} cannot be empty."
