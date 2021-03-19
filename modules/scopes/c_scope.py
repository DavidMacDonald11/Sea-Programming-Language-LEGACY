from .scope import VerbatumScope
from .scope import UnindentedScope
from .scope import EmptyScopeError

class CScope(VerbatumScope, UnindentedScope):
    sea_declaration = "c scope:"
    c_declaration = "// C Scope"
    sea_ending = None
    c_ending = None

    def close(self, cfile):
        try:
            super().close(cfile)
        except EmptyScopeError as e:
            raise EmptyScopeError(None, "C Scope cannot be empty.") from e
