import re
from modules.parser import indent
from modules.transpiler import statements
from modules.transpiler.errors import TranspilerError

class Scope:
    sea_declaration = "scope:"
    c_declaration = "{"
    c_ending = "}\n"

    def __init__(self, indentation, declaration):
        self.indent = indentation
        self.declaration = declaration
        self.is_empty = True

    def open(self, cfile):
        self.write_line(cfile, self.get_declaration(), True)

    def close(self, cfile):
        cls = type(self)

        if self.is_empty:
            raise EmptyScopeError(cls)

        self.write_line(cfile, self.get_ending(), True)

    def indent_line(self, line = "", outside = False):
        return " " * 4 * (self.indent - int(outside)) + line

    def write_line(self, cfile, line = "", outside = False):
        if line is not None:
            if not outside:
                line = statements.transpile(line)

            cfile.write(f"{self.indent_line(line, outside)}\n")

    def get_declaration(self):
        return type(self).c_declaration

    def get_ending(self):
        return type(self).c_ending

    @classmethod
    def check_match(cls, line):
        return re.fullmatch(cls.sea_declaration, line) is not None

class EmptyScope(Scope):
    """A scope that can be empty."""
    def close(self, cfile):
        self.is_empty = False
        super().close(cfile)

class VerbatumScope(Scope):
    """A scope that does not transpile its lines."""
    def indent_line(self, line = "", outside = False):
        if outside:
            return super().indent_line(line, outside)

        return line

    def write_line(self, cfile, line = "", outside = False):
        if outside:
            super().write_line(cfile, line, outside)
            return

        line = line.rstrip()
        cfile.write(f"{self.indent_line(line)}\n")

class UnindentedScope(Scope):
    """A scope that should not be indented in C, but is in Sea."""
    def indent_line(self, line = "", outside = False):
        if outside:
            return super().indent_line(line, outside)

        return indent.remove(line, 1)

class EndableScope(Scope):
    """A scope that has a defined Sea ending."""
    sea_ending = "Override Ending"

    def __init__(self, indentation, declaration):
        self.ending = None
        super().__init__(indentation, declaration)

    def check_ending(self, line):
        cls = type(self)
        ending = cls.sea_ending

        if ending == "Override Ending":
            raise UnoverridenMethodError(cls)

        if re.fullmatch(ending, line) is not None:
            self.ending = line
            return True

        return False

    def get_ending(self):
        if self.ending is None:
            raise UndeclaredEndOfScopeError()

        return self.ending

    def close(self, cfile):
        super().close(cfile)
        cfile.write("\n")

class InlineScope(Scope):
    """A scope that can start or stop beside other declarations."""
    def get_declaration(self):
        return self.declaration

    def close(self, cfile):
        cls = type(self)

        if self.is_empty:
            raise EmptyScopeError(cls)

        self.write_line(cfile, self.get_ending(), False)


class ScopeError(TranspilerError):
    pass

class ScopeDeclarationError(ScopeError):
    def __init__(self, message = None):
        if message is None:
            message = "Scope was declared incorrectly."

        super().__init__(message)

class UndeclaredScopeError(ScopeDeclarationError):
    def __init__(self, message = None):
        if message is None:
            message = "Too many indents for the current scope."

        super().__init__(message)

class EmptyScopeError(ScopeError):
    def __init__(self, scope_type = Scope, message = None):
        if message is None:
            message = f"{scope_type.__name__} cannot be empty. Use pass to declare empty scope."

        super().__init__(message)

class UndeclaredEndOfScopeError(ScopeError):
    def __init__(self, message = None):
        if message is None:
            message = "Scope ended without required end declaration."

        super().__init__(message)

class UnoverridenMethodError(ScopeError):
    def __init__(self, scope_type = Scope, message = None):
        if message is None:
            message = f"{scope_type.__name__} must override sea_ending class property."

        super().__init__(message)
