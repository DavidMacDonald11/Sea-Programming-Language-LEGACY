from modules.scopes.scopes import match_and_get
from ..transpiler import indent
from .error import TranspilerError

class ScopeManager:
    def __init__(self, cfile):
        self.cfile = cfile
        self.scope = 0
        self.endings = []
        self.lines_per = {0 : 0}

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        self.end_scopes()
        return True

    def validate(self, line):
        scope = indent.get_from_line(line.rstrip())
        line = line.strip()

        if scope > self.scope:
            raise IncorrectScopeError(self.scope, scope)

        if scope < self.scope:
            if self.lines_per[scope] < 1:
                raise EmptyScopeError()

            self.end_scopes(self.scope - scope)

        if scope == self.scope:
            self.lines_per[scope] += 1

            if line[-1] == ":":
                self.start_scope(line[:-1])

    def start_scope(self, line):
        self.scope += 1
        self.lines_per[self.scope] = 0

        scope_type = match_and_get(line)
        self.endings += [scope_type[2]]
        self.cfile.write(f"{self.get_indent(True)}{scope_type[1]}\n")

    def end_scopes(self, count = None):
        if count is None:
            count = self.scope

        for _ in range(count):
            self.cfile.write(f"{self.get_indent(True)}{self.endings[-1]}\n\n")
            self.scope -= 1
            self.endings = self.endings[:-1]

    def get_indent(self, ending = False):
        return " " * 4 * (self.scope - int(ending))

class IncorrectScopeError(TranspilerError):
    def __init__(self, correct_scope, scope, message = ""):
        if message == "":
            message = f"Current scope is {correct_scope} indents deep not {scope}."

        super().__init__(message)

class EmptyScopeError(TranspilerError):
    def __init__(self, message = "Scope cannot be empty. Use pass to declare empty scope."):
        super().__init__(message)
