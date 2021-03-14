from .scope import Scope
from .scope import EmptyScopeError

class CScope(Scope):
    _allows_empty = False
    _allows_verbatum = True
    _lines_are_indented = True
    _sea_declaration = "c scope:"
    _c_declaration = "// C Scope"
    _sea_ending = None
    _c_ending = None

    def close(self, cfile):
        try:
            super().close(cfile)
        except EmptyScopeError as e:
            raise EmptyScopeError(None, "C Scope cannot be empty.") from e
