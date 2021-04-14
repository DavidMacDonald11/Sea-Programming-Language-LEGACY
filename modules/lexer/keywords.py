from modules.helpers.warnings import raise_warning
from ..lexer import errors

TYPE_KEYWORDS = {
    "int",
    "float",
    "bool"
}

BOOL_KEYWORDS = {
    "not",
    "and",
    "or"
}

SYNTAX_KEYWORDS = {
    "if",
    "elif",
    "else",
    "define",
    "as"
}

KEYWORDS = TYPE_KEYWORDS | BOOL_KEYWORDS | SYNTAX_KEYWORDS

def is_keyword(token_value):
    return token_value in KEYWORDS

def keyword_declared_type(keyword):
    return keyword in TYPE_KEYWORDS

def cast_value_to_type(var_type, var_value, explicit = False):
    if var_type == "bool":
        return cast_value_to_bool(var_value, explicit)

    if var_type == "int":
        return cast_value_to_int(var_value, explicit)

    if var_type == "float":
        return float(var_value)

    return var_value

def cast_value_to_bool(value, explicit):
    is_str = isinstance(value, str)
    is_non_bool_str = is_str and (len(value) > 1 or value not in "01")
    is_non_bool_num = (value not in (0, 1))

    if not explicit and (is_non_bool_num or is_non_bool_str):
        raise_warning(errors.ImplicitCastWarning("bool", "non-boolean type"))

    return 1 if value else 0

def cast_value_to_int(value, explicit):
    is_float_str = isinstance(value, str) and "." in value
    is_float = isinstance(value, float) or is_float_str

    if not explicit and is_float:
        raise_warning(errors.ImplicitCastWarning("int", "float"))

    return int(value)
