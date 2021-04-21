from modules.lexer.token_types import TT
from .line import make_line
from .expression import make_expression
from ..nodes.collection import NODES
from ...parser import errors

def make_block(parser):
    remove_newlines(parser)

    if not parser.tokens_ahead(*parser.indent):
        raise errors.EmptyBlockError(parser.token)

    parser.depth += 1
    block = make_line(parser, **MAKE_FUNCS)
    remove_newlines(parser)

    while parser.tokens_ahead(*parser.indent):
        right = make_line(parser, **MAKE_FUNCS)
        block = NODES.SequentialOperationNode(block, right)
        remove_newlines(parser)

    parser.depth -= 1
    return block

def remove_newlines(parser):
    while parser.token.type is TT.NEWLINE:
        parser.advance()

def block_or_expression(parser):
    if parser.token.type is TT.NEWLINE:
        return make_block(parser)

    right = make_expression(parser)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return right

MAKE_FUNCS = {
    "block": make_block,
    "block_or_expression": block_or_expression
}
