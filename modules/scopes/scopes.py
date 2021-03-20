from .scope import Scope
from .c_scope import CScope
from .multiline_comment import MultilineComment
from .for_loop import ForLoop
from .while_loop import WhileLoop
from .do_while_loop import DoWhileLoop
from .function import FunctionScope

SCOPES = {Scope, CScope}
LOOPS = {ForLoop, WhileLoop, DoWhileLoop}
ALL_SCOPES = {MultilineComment, FunctionScope} | SCOPES | LOOPS

def check_match_all(line):
    for scope_type in ALL_SCOPES:
        if scope_type.check_match(line):
            return scope_type

    return None
