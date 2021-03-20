from .scope_manager import ScopeManager

def transpile(filename, new_filename):
    with open(filename) as seafile, open(new_filename, "w") as cfile:
        with ScopeManager(seafile, cfile) as scope:
            cfile.write("#define true 1\n")
            cfile.write("#define false 0\n")
            cfile.write("\n")

            for line in seafile:
                scope.interpret_line(line)

                if scope.line_was_space:
                    continue
