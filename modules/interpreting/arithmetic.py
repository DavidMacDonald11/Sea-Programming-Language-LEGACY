from interpreting import errors

def pow_nums(left, right, node):
    if right == left == 0:
        raise errors.UndefinedOperationError(node, "0 ** 0")

    return left ** right

def div_nums(left, right, node):
    if right == 0:
        raise errors.DivideByZeroError(node)

    return left / right

def mod_nums(left, right, node):
    if right == 0:
        raise errors.DivideByZeroError(node)

    return left % right
