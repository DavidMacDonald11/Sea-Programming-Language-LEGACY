from types import SimpleNamespace
from .grammar.line import make_line
from .grammar.block import make_block, make_block_or_expression

MAKES = SimpleNamespace(
    line = make_line,
    block = make_block,
    block_or_expression = make_block_or_expression
)
