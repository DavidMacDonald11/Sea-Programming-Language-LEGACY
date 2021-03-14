from .scope import Scope
from .c_scope import CScope

ALL_SCOPES = (Scope, CScope)

def check_match_all(line):
    for ScopeType in ALL_SCOPES:
        if ScopeType.check_match(line):
            return ScopeType

    return None
