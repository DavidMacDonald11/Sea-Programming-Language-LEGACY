from modules.parser import indent
from modules.scopes import scopes
from modules.scopes.scope import UndeclaredScopeError

class ScopeManager:
    def __init__(self, cfile):
        self.cfile = cfile
        self.scopes = []
        self.line_was_space = False

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        for scope in self.scopes:
            scope.close(self.cfile)

    def has_scopes(self):
        return len(self.scopes) > 0

    def current_indent(self):
        return self.scopes[-1].indent if self.has_scopes() else -1

    def scope_allows_verbatum(self):
        return type(self.scopes[-1]).allows_verbatum

    def interpret_line(self, line):
        self.interpret_space(line)

        if self.line_was_space:
            return

        line = line.rstrip()
        level = self.current_indent()
        new_level = indent.count_in_line(line)

        if self.has_scopes():
            if self.scope_allows_verbatum() and new_level >= level:
                self.scopes[-1].write_line(self.cfile, line)
                return

            if not self.scope_allows_verbatum() and new_level > level:
                raise UndeclaredScopeError()

            if new_level < level:
                self.end_scopes(level - new_level)
                level = self.current_indent()

            if new_level == level:
                self.scopes[-1].is_empty = False

        line = line.strip()

        if new_level == level:
            scope_type = scopes.check_match_all(line)

            if scope_type is None:
                self.scopes[-1].write_line(self.cfile, line)
                return

            self.scopes += [scope_type(level + 1, line)]

    def interpret_space(self, line):
        self.line_was_space = line.isspace() or line == ""

        if self.line_was_space and self.scope_allows_verbatum():
            self.scopes[-1].write_line(line)

    def end_scopes(self, amount):
        for _ in amount:
            self.scopes[-1].close(self.cfile)
            self.scopes = self.scopes[:-1]
