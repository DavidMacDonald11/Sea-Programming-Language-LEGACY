from .scope import Scope
from .c_scope import CScope
from .multiline_comment import MultilineComment

ALL_SCOPES = {Scope, CScope, MultilineComment}

def check_match_all(line):
    for scope_type in ALL_SCOPES:
        if scope_type.check_match(line):
            return scope_type

    return None
