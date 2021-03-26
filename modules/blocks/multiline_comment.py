from .basic.empty_block import EmptyBlock
from .basic.endable_block import EndableBlock
from .basic.inline_block import InlineBlock
from .basic.verbatum_block import VerbatumBlock

class MultilineComment(EmptyBlock, VerbatumBlock, EndableBlock, InlineBlock):
    @classmethod
    def check_match(cls, line):
        matches = cls.matches_pattern(cls.declaration_pattern, line)
        return matches and not cls.check_ending(line)

    @classmethod
    def get_declaration_pattern(cls):
        return r"/\*(?!.*\*/.*).*"

    @classmethod
    def get_ending_pattern(cls):
        return r"(?!.*/\*.*).*\*/"
