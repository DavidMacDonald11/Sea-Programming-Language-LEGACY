from .basic.verbatum_block import VerbatumBlock
from .basic.unindented_block import UnindentedBlock

class CBlock(UnindentedBlock, VerbatumBlock):
    def get_declaration(self):
        return "// C Block"

    def get_ending(self):
        return None

    @classmethod
    def check_match(cls, line):
        return line == "c block:"
