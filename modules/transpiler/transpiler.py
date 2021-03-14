from .scope_manager import ScopeManager

def transpile(filename, new_filename):
    with open(filename) as seafile, open(new_filename, "w") as cfile:
        with ScopeManager(cfile) as scope:
            for line in seafile:
                scope.interpret_line(line)

                if scope.line_was_space:
                    continue
