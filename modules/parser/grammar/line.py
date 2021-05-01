from parser import errors
from position.position import Position
from tokens.symbol import Symbol, Sym
from tokens.keyword import Keyword
from nodes.eof_node import EOFNode
from nodes.line_node import LineNode

def make_line_node(parser, makes):
    if parser.token.data is Sym.EOF:
        return EOFNode(parser.take())

    if parser.token.data is Sym.NEWLINE:
        parser.take()
        return make_line_node(parser, makes)

    check_indent(parser)
    return make_expressions(parser, makes)

def check_indent(parser):
    parser.advance(parser.depth - 1)
    indent_position = parser.position

    parser.advance()
    depth = sum(1 if token.data is Sym.INDENT else 0 for token in parser.tokens)

    parser.take(parser.depth)

    if parser.depth == depth:
        raise errors.IncorrectBlockError(depth, indent_position)

def make_expressions(parser, makes):
    specials = {
        "pass": make_pass,
        "break": make_break_or_continue,
        "continue": make_break_or_continue,
        "do": make_do_while_expression,
        "while": make_while_expression,
        "for": make_for_expression,
        "if": make_if_expression
    }

    no_end = parser.token.data in specials
    expression = specials.get(parser.token.data, default)(parser, makes)

    return LineNode(expression, parser.depth, no_end)

def default(parser, makes):
    expression = makes.expression(parser, makes)
    parser.expecting((Sym.NEWLINE, Sym.EOF))

    return expression
