from parser import errors
from tokens.symbol import Sym
from nodes.operations.sequential_node import SequentialOperationNode

def make_block(parser, makes):
    if parser.wanting(*parser.indent) is None:
        raise errors.EmptyBlockError()

    parser.retreat(parser.depth)
    parser.depth += 1
    block = makes.line(parser, makes)

    while parser.wanting(*parser.indent) is not None:
        parser.retreat(parser.depth)
        right = makes.line(parser, makes)
        block = SequentialOperationNode(block, right)

    parser.depth -= 1
    return block

def make_block_or_expression(parser, makes):
    if parser.token.data is Sym.NEWLINE:
        return make_block(parser, makes)

    expression = makes.expression(parser, makes)
    parser.expecting((Sym.NEWLINE, Sym.EOF))

    return expression
