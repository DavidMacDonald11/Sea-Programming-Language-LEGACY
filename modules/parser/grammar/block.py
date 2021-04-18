from modules.lexer.token_types import TT
from .line import make_line
from .expression import make_expression
from ..nodes.collection import NODES
from ...parser import errors

def make_block(parser):
    parser.depth += 1
    left = make_line(parser, **MAKE_FUNCS)

    if not is_normal(left):
        depth, indent_position = left
        block_error_info = (parser.depth, depth, indent_position)

        raise errors.IncorrectBlockError(*block_error_info)

    block = left
    right = make_line(parser, **MAKE_FUNCS)

    while is_normal(right):
        block = NODES.SequentialOperationNode(block, right)
        right = make_line(parser, **MAKE_FUNCS)

    parser.depth -= 1
    return block

def block_or_expression(parser):
    if parser.token.type is TT.NEWLINE:
        return make_block(parser)

    right = make_expression(parser)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return right

def is_normal(node):
    return isinstance(node, NODES.ASTNode) and not isinstance(node, NODES.EOFNode)

MAKE_FUNCS = {
    "block": make_block,
    "block_or_expression": block_or_expression
}
