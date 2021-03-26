from modules.parser.indentation import remove_indent
from .block import Block

#pylint: disable=W0223
class UnindentedBlock(Block):
    """A block that should not be indented in C, but is in Sea."""
    def indent_line(self, line = "", outside = False):
        if outside:
            return super().indent_line(line, outside)

        return remove_indent(line, 1)
