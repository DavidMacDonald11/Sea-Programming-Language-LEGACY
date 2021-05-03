from types import SimpleNamespace
from .grammar.bitwise_expression import make_bitwise_shift_expression
from .grammar.bitwise_expression import make_bitwise_and_expression
from .grammar.bitwise_expression import make_bitwise_xor_expression
from .grammar.bitwise_expression import make_bitwise_or_expression
from .grammar.comparison_expression import make_comparison_expression
from .grammar.boolean_expression import make_boolean_not_expression
from .grammar.boolean_expression import make_boolean_and_expression
from .grammar.boolean_expression import make_boolean_or_expression
from .grammar.expression import make_expression, binary_operation, ternary_operation
from .grammar.line import make_line
from .grammar.block import make_block, make_block_or_expression

MAKES = SimpleNamespace(
    bitwise_shift_expression = make_bitwise_shift_expression,
    bitwise_and_expression = make_bitwise_and_expression,
    bitwise_xor_expression = make_bitwise_xor_expression,
    bitwise_or_expression = make_bitwise_or_expression,
    comparison_expression = make_comparison_expression,
    boolean_not_expression = make_boolean_not_expression,
    boolean_and_expression = make_boolean_and_expression,
    boolean_or_expression = make_boolean_or_expression,
    expression = make_expression,
    ternary_operation = ternary_operation,
    binary_operation = binary_operation,
    line = make_line,
    block = make_block,
    block_or_expression = make_block_or_expression
)
