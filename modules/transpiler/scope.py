from modules.parser import indent
from modules.scopes import scopes
from modules.scopes.scope import VerbatumScope
from modules.scopes.scope import EndableScope
from modules.scopes.scope import UndeclaredScopeError
from modules.scopes.scope import UndeclaredEndOfScopeError
from modules.scopes.global_scope import GlobalScope

class Scope:
    @property
    def scope(self):
        return self.scopes[-1]

    @property
    def indent(self):
        return self.scope.indent

    def __init__(self, cfile):
        self.cfile = cfile
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

class Continue(Exception):
    pass

def interpret_line(scope, line):
    scope.line = line

    check_space(scope)
    check_scope_end(scope)
    check_verbatum_line(scope)
    check_undeclared_scope_start(scope)
    check_previous_scope_end(scope)
    check_scope_start(scope)

def check_space(scope):
    if scope.line.isspace() or scope.line == "":
        if scope.is_type(VerbatumScope):
            scope.write_line()

        raise Continue()

    scope.line = scope.line.rstrip()

def check_scope_end(scope):
    scope.new_indent = indent.count_in_line(scope.line)

    if scope.is_type(EndableScope) and scope.scope.check_ending(scope.line):
        if scope.new_indent < scope.indent - 1:
            raise UndeclaredEndOfScopeError()

        scope.close(1)
        raise Continue()

def check_verbatum_line(scope):
    if scope.is_type(VerbatumScope) and scope.new_indent >= scope.indent:
        scope.has_line()
        scope.write_line()
        raise Continue

def check_undeclared_scope_start(scope):
    if not scope.is_type(VerbatumScope) and scope.new_indent > scope.indent:
        raise UndeclaredScopeError()

def check_previous_scope_end(scope):
    if scope.new_indent < scope.indent:
        for i in range(scope.indent - scope.new_indent):
            prev_scope = scope.scopes[-1 - i]

            if prev_scope.is_type(EndableScope) and prev_scope.check_ending(scope.line):
                scope.line = prev_scope.remove_ending(scope.line)

        scope.close(scope.indent - scope.new_indent)

    scope.line = scope.line.strip()

    if scope.line == "":
        raise Continue()

def check_scope_start(scope):
    if scope.new_indent == scope.indent:
        scope.has_line()
        scope_type = scopes.check_match_all(scope.line)

        if scope_type is None:
            scope.write_line()
        else:
            scope.open(scope_type, scope.line)

        raise Continue()
