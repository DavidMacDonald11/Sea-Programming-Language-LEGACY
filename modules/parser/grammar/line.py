from parser import errors
from tokens.symbol import Sym
from nodes.eof_node import EOFNode
from nodes.line_node import LineNode
from nodes.operations.keyword_node import KeywordOperationNode
from .expressions.do_while_expression import make_do_while_expression
from .expressions.while_expression import make_while_expression
from .expressions.for_expression import make_for_expression
from .expressions.if_expression import make_if_expression

def make_line(parser, makes):
    if parser.token.data is Sym.EOF:
        return EOFNode(parser.take())

    check_indent(parser)

    return make_expressions(parser, makes)

def check_indent(parser):
    try:
        parser.mark()
        parser.expecting(*parser.indent)
        indent_position = parser.position

        if parser.token.data == Sym.INDENT:
            raise errors.IncorrectBlockError(parser.depth + 1, indent_position)
    except errors.ExpectedTokenError as e:
        depth = parser.bounds[1] - parser.bounds[0]
        raise errors.IncorrectBlockError(depth, indent_position) from e

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

def make_pass(parser, _):
    return KeywordOperationNode(parser.take())

def make_break_or_continue(parser, makes):
    keyword_token = parser.take()
    condition = None

    if parser.token.data == "if":
        parser.take()
        condition = makes.expression_node(parser, makes)

    parser.expecting((Sym.NEWLINE, Sym.EOF))

    return KeywordOperationNode(keyword_token, None, condition)

def default(parser, makes):
    expression = makes.expression(parser, makes)
    parser.expecting((Sym.NEWLINE, Sym.EOF))

    return expression
