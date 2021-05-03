from tokens.operator import Op

def make_bitwise_shift_expression(parser, makes):
    operations = (Op.LSHIFT, Op.RSHIFT)
    return makes.binary_operation(parser, makes, operations, makes.arithmetic_expression)

def make_bitwise_and_expression(parser, makes):
    return makes.binary_operation(parser, makes, Op.AND, make_bitwise_shift_expression)

def make_bitwise_xor_expression(parser, makes):
    return makes.binary_operation(parser, makes, Op.XOR, make_bitwise_and_expression)

def make_bitwise_or_expression(parser, makes):
    return makes.binary_operation(parser, makes, Op.OR, make_bitwise_xor_expression)
