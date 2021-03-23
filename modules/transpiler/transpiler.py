from modules.parser import indent
from modules.scopes import scopes
from modules.scopes.scope import VerbatumScope
from modules.scopes.scope import EndableScope
from modules.scopes.scope import UndeclaredScopeError
from modules.scopes.scope import UndeclaredEndOfScopeError
from .errors import TranspilerError
from .scope import Scope

class Continue(Exception):
    pass

scope = Scope()

def transpile(filename, new_filename):
    with open(filename) as seafile, open(new_filename, "w") as cfile:
        write_header(cfile)

        line_number = -1
        scope.cfile = cfile

        try:
            for line_number, line in enumerate(seafile):
                try:
                    scope.line = line
                    interpret_line()
                except Continue:
                    continue

            scope.close_all()
        except TranspilerError as e:
            print_error(line_number, seafile, cfile, e)

def write_header(cfile):
    cfile.write("#define true 1\n")
    cfile.write("#define false 0\n")
    cfile.write("\n")

def interpret_line():
    check_space()
    check_scope_end()
    check_verbatum_line()
    check_undeclared_scope_start()
    check_previous_scope_end()
    check_scope_start()

def print_error(line_number, seafile, cfile, error):
    to_print = f"Line #{line_number + 1} of {seafile.name}:\n{error.message}"

    print(to_print)
    cfile.write("// Transpilation stopped due to error\n")
    cfile.write(f"/* {to_print} */\n")

def check_space():
    if scope.line.isspace() or scope.line == "":
        if scope.is_type(VerbatumScope):
            scope.write_line()

        raise Continue()

    scope.line = scope.line.rstrip()

def check_scope_end():
    scope.new_indent = indent.count_in_line(scope.line)

    if scope.is_type(EndableScope) and scope.scope.check_ending(scope.line):
        if scope.new_indent < scope.indent - 1:
            raise UndeclaredEndOfScopeError()

        scope.close(1)
        raise Continue()

def check_verbatum_line():
    if scope.is_type(VerbatumScope) and scope.new_indent >= scope.indent:
        scope.has_line()
        scope.write_line()
        raise Continue

def check_undeclared_scope_start():
    if not scope.is_type(VerbatumScope) and scope.new_indent > scope.indent:
        raise UndeclaredScopeError()

def check_previous_scope_end():
    if scope.new_indent < scope.indent:
        for i in range(scope.indent - scope.new_indent):
            prev_scope = scope.scopes[-1 - i]

            if prev_scope.is_type(EndableScope) and prev_scope.check_ending(scope.line):
                scope.line = prev_scope.remove_ending(scope.line)

        scope.close(scope.indent - scope.new_indent)

    scope.line = scope.line.strip()

    if scope.line == "":
        raise Continue()

def check_scope_start():
    if scope.new_indent == scope.indent:
        scope.has_line()
        scope_type = scopes.check_match_all(scope.line)

        if scope_type is None:
            scope.write_line()
        else:
            scope.open(scope_type, scope.line)

        raise Continue()
