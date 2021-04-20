from ..interpreter import errors

def lshift_nums(x, y):
    return get_and_check(x, y, lambda x, y: x << y)

def rshift_nums(x, y):
    return get_and_check(x, y, lambda x, y: x >> y)

def and_nums(x, y):
    return get_and_check(x, y, lambda x, y: x & y)

def xor_nums(x, y):
    return get_and_check(x, y, lambda x, y: x ^ y)

def or_nums(x, y):
    return get_and_check(x, y, lambda x, y: x | y)

def get_and_check(x, y, func):
    try:
        return func(x, y)
    except TypeError as e:
        raise errors.BitwiseOperationTypeError(None) from e
