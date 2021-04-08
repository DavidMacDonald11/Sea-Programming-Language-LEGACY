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

KEYWORDS = TYPE_KEYWORDS | BOOL_KEYWORDS

def is_keyword(token_value):
    return token_value in KEYWORDS

def keyword_declared_type(keyword):
    return keyword in TYPE_KEYWORDS

def cast_value_to_type(var_type, var_value, explicit = False):
    if var_type == "bool":
        is_str = isinstance(var_value, str)
        is_non_bool_str = is_str and (len(var_value) > 1 or var_value not in "01")
        is_non_bool_num = (var_value != 0 or var_value != 1)

        if not explicit and (is_non_bool_num or is_non_bool_str):
            raise_warning(errors.ImplicitCastWarning(var_type, "non-boolean type"))

        return bool(var_type)

    if var_type == "int":
        is_float_str = isinstance(var_value, str) and "." in var_value
        is_float = isinstance(var_value, float) or is_float_str

        if not explicit and is_float:
            raise_warning(errors.ImplicitCastWarning(var_type, "float"))

        return int(var_value)

    if var_type == "float":
        return float(var_value)

    return var_value
