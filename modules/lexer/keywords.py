from ..lexer import errors

TYPE_KEYWORDS = {
    "int",
    "float"
}

KEYWORDS = TYPE_KEYWORDS

def is_keyword(token_value):
    return token_value in KEYWORDS

def keyword_declared_type(keyword):
    return keyword in TYPE_KEYWORDS

def cast_value_to_type(var_type, var_value, explicit = False):
    if var_type == "int":
        is_float_str = isinstance(var_value, str) and "." in var_value
        is_float = isinstance(var_value, float) or is_float_str

        if not explicit and is_float:
            raise errors.ImplicitCastError(var_type, "float")

        return int(var_value)

    if var_type == "float":
        return float(var_value)

    return var_value
