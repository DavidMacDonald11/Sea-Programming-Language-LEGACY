from modules.lexer.token_types import TT
from .boolean_or_expression import make_boolean_or_expression
from ..nodes.collection import NODES

def make_expression(parser, **make_funcs):
    make_funcs["expression"] = make_expression
    make_funcs["binary_operation"] = binary_operation
    make_funcs["ternary_operation"] = ternary_operation

    if parser.token.matches_type_keyword():
        return make_var_assign(parser, **make_funcs)

    operations = [(TT.KEYWORD, "if"), (TT.KEYWORD, "else")]
    return ternary_operation(parser, make_boolean_or_expression, operations, **make_funcs)

def make_var_assign(parser, **make_funcs):
    keyword_token = parser.take_token()
    variable_token = parser.expecting(TT.IDENTIFIER)
    parser.expecting(TT.EQUALS)

    expression = make_funcs["expression"](parser, **make_funcs)
    return NODES.VariableAssignNode(keyword_token, variable_token, expression)

def ternary_operation(parser, left_func, operations, right_func = None, **make_funcs):
    if right_func is None:
        right_func = left_func

    left = left_func(parser, **make_funcs)
    token_type_value = (parser.token.type, parser.token.value)

    if parser.token.type not in operations[0] and token_type_value not in operations[0]:
        return left

    left_operation = parser.take_token()
    middle = right_func(parser, **make_funcs)

    token_type_value = (parser.token.type, parser.token.value)

    if parser.token.type not in operations[1] and token_type_value not in operations[1]:
        return NODES.BinaryOperationNode(left, left_operation, middle)

    right_operation = parser.take_token()
    right = right_func(parser, **make_funcs)

    operations = (left_operation, right_operation)
    values = (left, middle, right)

    return NODES.TernaryOperationNode(operations, values)

def binary_operation(parser, left_func, operations, right_func = None, **make_funcs):
    if right_func is None:
        right_func = left_func

    left = left_func(parser, **make_funcs)
    token_type_value = (parser.token.type, parser.token.value)

    while parser.token.type in operations or token_type_value in operations:
        operation = parser.take_token()
        right = right_func(parser, **make_funcs)
        left = NODES.BinaryOperationNode(left, operation, right)

        token_type_value = (parser.token.type, parser.token.value)

    return left
