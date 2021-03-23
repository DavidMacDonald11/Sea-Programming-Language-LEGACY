from modules.scopes.global_scope import GlobalScope

class Scope:
    @property
    def scope(self):
        return self.scopes[-1]

    @property
    def indent(self):
        return self.scope.indent

    def __init__(self):
        self.cfile = None
        self.scopes = [GlobalScope()]
        self.new_indent = -1
        self.line = ""

    def open(self, scope_type, line):
        scope = scope_type(self.indent + 1, line)
        scope.open(self.cfile)

        self.scopes += [scope]

    def close(self, amount):
        for _ in range(amount):
            self.scope.close(self.cfile)
            self.scopes = self.scopes[:-1]

    def close_all(self):
        for scope in self.scopes[::-1]:
            scope.close(self.cfile)

    def is_type(self, scope_type):
        return self.scope.is_type(scope_type)

    def write_line(self):
        self.scope.write_line(self.cfile, self.line)

    def has_line(self):
        self.scope.is_empty = False
