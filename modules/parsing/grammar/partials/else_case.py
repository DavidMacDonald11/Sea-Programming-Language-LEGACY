from tokens.symbol import Sym

def make_else_case(parser, makes):
    if parser.wanting(*parser.indent, "else") is None:
        return None

    parser.expecting(Sym.COLON)
    return makes.block_or_expression(parser, makes)
