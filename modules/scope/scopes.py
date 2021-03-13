from modules.transpiler.error import TranspilerError

def match_and_transpile(scope_type, scope, cfile):
    scope_type = match_and_get(scope_type)

    indent = get_indent(scope, True)
    cfile.write(f"{indent}{scope_type[1]}\n")

    return [scope_type[2]]

def match_and_get(scope_type):
    if scope_type == "scope":
        return ("empty", "{", "}")

    raise UnknownScopeError(f"Scope defined by \"{scope_type}:\" is unknown.")

def end_scope(scopes_end, scope, cfile):
    while len(scopes_end) > scope:
        indent = get_indent(len(scopes_end), True)
        cfile.write(f"{indent}{scopes_end[-1]}\n\n")
        scopes_end = scopes_end[:-1]

    return scopes_end

def get_indent(scope, end = False):
    return " " * 4 * (scope if not end else scope - 1)

class UnknownScopeError(TranspilerError):
    pass

class IncorrectScopeError(TranspilerError):
    pass

class EmptyScopeError(TranspilerError):
    pass
