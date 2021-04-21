from modules.lexer.position import Position
from modules.lexer.token_types import TT
from .expression import make_expression
from .if_expression import make_if_expression
from .while_expression import make_while_expression
from ..nodes.collection import NODES
from ...parser import errors

def make_line(parser, **make_funcs):
    make_funcs["make_line"] = make_line

    if parser.token.type is TT.EOF:
        return NODES.EOFNode(parser.take_token())

    if parser.token.type is TT.NEWLINE:
        parser.advance()
        return make_line(parser,  **make_funcs)

    has_indent = parser.tokens_ahead(*parser.indent)
    token_after_indent = parser.token_ahead(len(parser.indent) + 1)
    has_indent = has_indent and token_after_indent.type is not TT.INDENT

    depth, indent_position = take_indent(parser)

    if not has_indent:
        block_error_info = (parser.depth, depth, indent_position)
        raise errors.IncorrectBlockError(*block_error_info)

    return special_or_default(parser, **make_funcs)

def take_indent(parser):
    indent_start = parser.token.position.start
    tokens = []

    while parser.token.type is TT.INDENT:
        tokens += [parser.take_token()]

    indent_position = Position(indent_start, parser.token.position.end)

    return len(tokens), indent_position

def special_or_default(parser, **make_funcs):
    special = {
        "pass": make_pass,
        "break": make_break_or_continue,
        "continue": make_break_or_continue,
        "redefine": make_redefine_line,
        "undefine": make_undefine_line,
        "define": make_define_line,
        "if": make_if_expression,
        "while": make_while_expression
    }

    no_end = parser.token.value in special
    expression = special.get(parser.token.value, default)(parser, **make_funcs)

    return NODES.LineNode(expression, parser.depth, no_end)

def make_pass(parser, **_):
    return NODES.KeywordOperationNode(parser.take_token())

def make_break_or_continue(parser, **make_funcs):
    keyword = parser.take_token()
    condition = None

    if parser.token.matches(TT.KEYWORD, "if"):
        parser.take_token()
        condition = make_expression(parser, **make_funcs)

    parser.expecting(TT.NEWLINE, TT.EOF)

    return NODES.KeywordOperationNode(keyword, None, condition)

def make_redefine_line(parser, **make_funcs):
    redefine_token = parser.take_token()
    name = parser.expecting(TT.IDENTIFIER)
    parser.expecting_keyword("as")

    expression = make_expression(parser, **make_funcs)
    parser.expecting(TT.NEWLINE, TT.EOF)

    undefine = NODES.ConstantUndefineNode(redefine_token, name)
    define = NODES.ConstantDefineNode(redefine_token, name, expression)

    return NODES.SequentialOperationNode(undefine, define)

def make_undefine_line(parser, **_):
    undefine_token = parser.take_token()
    name = parser.expecting(TT.IDENTIFIER)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return NODES.ConstantUndefineNode(undefine_token, name)

def make_define_line(parser, **make_funcs):
    define_token = parser.take_token()
    name = parser.expecting(TT.IDENTIFIER)
    parser.expecting_keyword("as")

    expression = make_expression(parser, **make_funcs)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return NODES.ConstantDefineNode(define_token, name, expression)

def default(parser, **make_funcs):
    expression = make_expression(parser, **make_funcs)
    parser.expecting(TT.NEWLINE, TT.EOF)

    return expression
