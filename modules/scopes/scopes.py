from modules.transpiler.errors import UnknownScopeError
from .scope import Scope
from .c_scope import CScope

def match_and_get(scope_type):
    if scope_type == "scope":
        return ("empty", "{", "}")

    raise UnknownScopeError(scope_type)

ALL_SCOPES = (Scope, CScope)

def check_match_all(line):
    for ScopeType in ALL_SCOPES:
        if ScopeType.check_match(line):
            return ScopeType

    return None
