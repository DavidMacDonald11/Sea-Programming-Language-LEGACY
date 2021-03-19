import re
from .scope import EmptyScope
from .scope import VerbatumScope
from .scope import EndableScope
from .scope import InlineScope

class MultilineComment(EmptyScope, VerbatumScope, EndableScope, InlineScope):
    # TODO make declaration able to follow a statement
    # TODO make multiline comment able to be 1 line
    # TODO update documentation
    sea_declaration = r"/\*.*"
    sea_ending = r".*\*/"
    c_declaration = "/*"
    c_ending = "*/\n"

    @classmethod
    def check_match(cls, line):
        matches = super().check_match(line)
        return matches and not re.fullmatch(cls.sea_ending, line)
