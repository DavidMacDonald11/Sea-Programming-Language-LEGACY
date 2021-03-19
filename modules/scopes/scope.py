from modules.parser import indent
from modules.transpiler.errors import TranspilerError

class Scope:
    sea_declaration = "scope:"
    c_declaration = "{"
    sea_ending = None
    c_ending = "}\n"

    def __init__(self, indentation, declaration):
        self.indent = indentation
        self.declaration = declaration
        self.is_empty = True

    def open(self, cfile):
        self.write_line(cfile, type(self).c_declaration, True)

    def close(self, cfile):
        cls = type(self)

        if self.is_empty:
            raise EmptyScopeError(cls)

        self.write_line(cfile, cls.c_ending, True)

    def indent_line(self, line = "", outside = False):
        return " " * 4 * (self.indent - int(outside)) + line

    def write_line(self, cfile, line = "", outside = False):
        if line is not None:
            line = self.transpile_line(line)
            cfile.write(f"{self.indent_line(line, outside)}\n")

    # TODO transpile line to C
    def transpile_line(self, line):
        return line

    @classmethod
    def check_match(cls, line):
        return line == cls.sea_declaration

class EmptyScope(Scope):
    def close(self, cfile):
        self.is_empty = False
        super().close(cfile)

class VerbatumScope(Scope):
    def write_line(self, cfile, line = "", outside = False):
        if outside:
            super().write_line(cfile, line, outside)
            return

        line = line.rstrip()
        cfile.write(f"{self.indent_line(line)}\n")

class UnindentedScope(Scope):
    def indent_line(self, line = "", outside = False):
        if outside:
            return super().indent_line(line, outside)

        return indent.remove(line, 1)

class ScopeError(TranspilerError):
    pass

class UndeclaredScopeError(ScopeError):
    def __init__(self, message = None):
        if message is None:
            message = "Too many indents for the current scope."

        super().__init__(message)

class EmptyScopeError(ScopeError):
    def __init__(self, scope_type = Scope, message = None):
        if message is None:
            message = f"{scope_type.__name__} cannot be empty. Use pass to declare empty scope."

        super().__init__(message)
