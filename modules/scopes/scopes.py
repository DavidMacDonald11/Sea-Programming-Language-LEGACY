from modules.transpiler.errors import UnknownScopeError

def match_and_get(scope_type):
    if scope_type == "scope":
        return ("empty", "{", "}")

    raise UnknownScopeError(scope_type)
