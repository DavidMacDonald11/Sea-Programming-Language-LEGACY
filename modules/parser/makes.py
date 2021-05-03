from types import SimpleNamespace
from .grammar.expressions.comparison_expression import make_comparison_expression
from .grammar.expressions.boolean_expression import make_boolean_not_expression
from .grammar.expressions.boolean_expression import make_boolean_and_expression
from .grammar.expressions.boolean_expression import make_boolean_or_expression
from .grammar.expression import make_expression, binary_operation, ternary_operation
from .grammar.line import make_line
from .grammar.block import make_block, make_block_or_expression

MAKES = SimpleNamespace(
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
