from modules.parser import indent
from modules.scopes import scopes
from modules.scopes.scope import VerbatumScope
from modules.scopes.scope import UndeclaredScopeError
from .errors import TranspilerError

class ScopeManager:
    def __init__(self, cfile):
        self.cfile = cfile
        self.scopes = []
        self.line_was_space = False
        self.line_count = 0

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        def error(message):
            print(f"Line #{self.line_count}: {message}")
            self.cfile.write("// Transpilation stopped due to error")

        if e_type is not None:
            error(e_traceback)

        try:
            for scope in self.scopes:
                scope.close(self.cfile)
        except TranspilerError as e:
            error(e.message)

    def has_scopes(self):
        return len(self.scopes) > 0

    def current_indent(self):
        return self.scopes[-1].indent if self.has_scopes() else 0

    def scope_allows_verbatum(self):
        return isinstance(self.scopes[-1], VerbatumScope)

    def interpret_line(self, line):
        self.line_count += 1
        self.interpret_space(line)

        if self.line_was_space:
            return

        line = line.rstrip()
        level = self.current_indent()
        new_level = indent.count_in_line(line)

        # TODO check for end of scope if Scope.c_ending is not None

        if self.has_scopes():
            if self.scope_allows_verbatum() and new_level >= level:
                self.scopes[-1].is_empty = False
                self.scopes[-1].write_line(self.cfile, line)
                return

            if not self.scope_allows_verbatum() and new_level > level:
                raise UndeclaredScopeError()

            if new_level < level:
                self.end_scopes(level - new_level)
                level = self.current_indent()

        line = line.strip()

        if new_level == level:
            if self.has_scopes():
                self.scopes[-1].is_empty = False

            scope_type = scopes.check_match_all(line)

            if scope_type is None:
                self.scopes[-1].write_line(self.cfile, line)
                return

            self.start_scope(scope_type, level, line)

    def interpret_space(self, line):
        self.line_was_space = line.isspace() or line == ""

        if self.line_was_space and self.has_scopes() and self.scope_allows_verbatum():
            self.scopes[-1].write_line(self.cfile, line)

    def start_scope(self, scope_type, level, line):
        scope = scope_type(level + 1, line)
        scope.open(self.cfile)

        self.scopes += [scope]

    def end_scopes(self, amount):
        for _ in range(amount):
            self.scopes[-1].close(self.cfile)
            self.scopes = self.scopes[:-1]
