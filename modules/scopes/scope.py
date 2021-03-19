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
        self._write_outside(cfile, type(self).c_declaration)

    def close(self, cfile):
        self.check_empty()
        self._write_outside(cfile, type(self).c_ending)

    def check_empty(self):
        if self.is_empty:
            raise EmptyScopeError(type(self))

    def indent_line(self, line = "", outside = False):
        return " " * 4 * (self.indent - int(outside)) + line

    def _write_outside(self, cfile, line):
        if line is not None:
            cfile.write(f"{self.indent_line(line, True)}\n")

    def write_line(self, cfile, line = ""):
        # TODO transpile line to C
        cfile.write(f"{self.indent_line(line)}\n")

    @classmethod
    def check_match(cls, line):
        return line == cls.sea_declaration

class EmptyScope(Scope):
    def check_empty(self):
        pass

class VerbatumScope(Scope):
    def write_line(self, cfile, line = ""):
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
