from tokens.operator import Op

def make_arithmetic_expression(parser, makes):
    return makes.binary_operation(parser, makes, (Op.PLUS, Op.MINUS), makes.term)
