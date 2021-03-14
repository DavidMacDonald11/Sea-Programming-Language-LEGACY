from ..transpiler.scopes import ScopeManager
from .error import TranspilerError

def transpile(filename, new_filename):
    with open(filename) as seafile, open(new_filename, "w") as cfile:
        i = -1

        with ScopeManager(cfile) as scope:
            try:
                for i, line in enumerate(seafile):
                    if line.isspace():
                        if scope.in_c_scope:
                            cfile.write("\n")

                        continue

                    c_scope_declaration = scope.validate(line)

                    if scope.in_c_scope:
                        if c_scope_declaration:
                            cfile.write(f"{scope.get_indent(True)}// C Scope:\n")
                            continue

                        line = line[4:] if line[0] == " " else line[1:]
                        cfile.write(f"{line.rstrip()}\n")

                        continue

                    line = line.strip()

            except TranspilerError as e:
                print(f"Line #{i + 1}: {e.message}")
                cfile.write("// Transpilation stopped due to error")
