from tokens.operator import Op

def make_factor(parser, makes):
    return makes.binary_operation(parser, makes, Op.POWER, makes.part)
