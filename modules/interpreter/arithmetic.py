from ..interpreter import errors

def neg_num(num):
    return -num

def pos_num(num):
    return num

def add_nums(left, right):
    return left + right

def sub_nums(left, right):
    return left - right

def mul_nums(left, right):
    return left * right

def div_nums(left, right):
    if right == 0:
        raise errors.DivideByZeroError(None)

    return left / right
