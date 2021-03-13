from modules.transpiler.error import TranspilerError

def match_and_get(scope_type):
    if scope_type == "scope":
        return ("empty", "{", "}")

    raise UnknownScopeError(scope_type)

class UnknownScopeError(TranspilerError):
    def __init__(self, scope_type, message = ""):
        if message == "":
            message = f"Scope defined by \"{scope_type}:\" is unknown."

        super().__init__(message)
