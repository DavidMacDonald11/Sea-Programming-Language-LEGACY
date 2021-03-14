from modules.parser import indent
from modules.transpiler.errors import TranspilerError
from .meta_scope import MetaScope

class Scope(metaclass = MetaScope):
    _allows_empty = False
    _allows_verbatum = False
    _lines_are_indented = True
    _sea_declaration = "scope:"
    _c_declaration = "{"
    _sea_ending = None
    _c_ending = "}"

    def __init__(self, indentation, declaration):
        self.indent = indentation
        self.declaration = declaration
        self.is_empty = True

    def open(self, cfile):
        cls = type(self)
        self._write_outside(cfile, cls.c_declaration)

    def close(self, cfile):
        cls = type(self)

        if not cls.allows_empty and self.is_empty:
            raise EmptyScopeError(cls)

        self._write_outside(cfile, cls.c_ending)

    def get_indent(self, outside = False):
        return " " * 4 * (self.indent - int(outside))

    def _write_outside(self, cfile, line = ""):
        cfile.write(f"{self.get_indent(True)}")
        cfile.write(line + "\n")

    def write_line(self, cfile, line = ""):
        cls = type(self)

        if cls.allows_verbatum:
            line = line.rstrip()

            if cls.lines_are_indented:
                line = indent.remove(line, 1)
                cfile.write(f"{line}\n")
                return

        # TODO transpile line to C

        cfile.write(f"{self.get_indent()}\n")

    @classmethod
    def check_match(cls, line):
        return line == cls.sea_declaration

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
