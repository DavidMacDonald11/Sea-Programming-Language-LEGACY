from ..transpiler.scopes import ScopeManager
from .error import TranspilerError

def transpile(filename, src_dir, bin_dir):
    new_filename = filename.replace(src_dir, bin_dir, 1)
    new_filename = new_filename.replace(".hea", ".h")
    new_filename = new_filename.replace(".sea", ".c")

    with open(filename) as seafile, open(new_filename, "w") as cfile:
        i = -1

        with ScopeManager(cfile) as scope:
            try:
                for i, line in enumerate(seafile):
                    if line.isspace():
                        continue

                    scope.validate(line)
                    line = line.strip()

            except TranspilerError as e:
                print(f"Line #{i + 1}: {e.message}")
                cfile.write("// Transpilation stopped due to error")
