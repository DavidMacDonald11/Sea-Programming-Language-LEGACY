from types import SimpleNamespace
from .grammar.expression import make_expression, binary_operation, ternary_operation
from .grammar.line import make_line
from .grammar.block import make_block, make_block_or_expression

MAKES = SimpleNamespace(
    expression = make_expression,
    ternary_operation = ternary_operation,
    binary_operation = binary_operation,
    line = make_line,
    block = make_block,
    block_or_expression = make_block_or_expression
)
