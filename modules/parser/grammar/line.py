from modules.lexer.position import Position
from modules.lexer.token_types import TT
from .expression import make_expression
from .if_expression import make_if_expression
from ..nodes.collection import NODES
from ...parser import errors

def make_line(parser, **make_funcs):
    if parser.token.type is TT.EOF:
        return NODES.EOFNode(parser.take_token())

    if parser.token.type is TT.NEWLINE:
        parser.advance()
        return make_line(parser, **make_funcs)

    depth, indent_position = get_indent(parser)

    if depth > parser.depth:
        block_error_info = (parser.depth, depth, indent_position)
        raise errors.IncorrectBlockError(*block_error_info)

    if depth < parser.depth:
        return (depth, indent_position)

    make_funcs["make_line"] = make_line
    return special_or_default(parser, **make_funcs)

def get_indent(parser):
    indent_start = parser.token.position.start
    depth = 0

    while parser.token.type is TT.INDENT:
        parser.advance()
        depth += 1

    indent_position = Position(indent_start, parser.token.position.end)

    return (depth, indent_position)

def special_or_default(parser, **make_funcs):
    expression, no_end = {
        "undefine": make_undefine_line,
        "define": make_define_line,
        "if": make_if_expression
    }.get(parser.token.value, default)(parser, **make_funcs)

    return NODES.LineNode(expression, parser.depth, no_end)

def make_undefine_line(parser, **_):
    undefine_token = parser.take_token()
    name = parser.expecting(TT.IDENTIFIER)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return NODES.ConstantUndefineNode(undefine_token, name), True

def make_define_line(parser, **_):
    define_token = parser.take_token()
    name = parser.expecting(TT.IDENTIFIER)
    parser.expecting_keyword("as")

    expression = make_expression(parser)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return NODES.ConstantDefineNode(define_token, name, expression), True

def default(parser, **make_funcs):
    expression = make_expression(parser, **make_funcs)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return expression, False
