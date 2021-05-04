from tokens.operator import Op

def make_term(parser, makes):
    return makes.binary_operation(parser, makes, (Op.MULTIPLY, Op.DIVIDE, Op.MODULO), makes.factor)
