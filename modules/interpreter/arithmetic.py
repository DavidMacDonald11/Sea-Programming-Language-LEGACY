from ..interpreter import errors

def pow_nums(left, right):
    if right == left == 0:
        raise errors.UndefinedOperationError("0 ** 0")

    return left ** right

def div_nums(left, right):
    if right == 0:
        raise errors.DivideByZeroError(None)

    return left / right

def mod_nums(left, right):
    if right == 0:
        raise errors.DivideByZeroError(None)

    return left % right
