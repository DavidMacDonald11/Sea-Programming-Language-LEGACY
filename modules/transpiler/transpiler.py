
from .errors import TranspilerError
from .scope import Scope
from .scope import Continue
from .scope import interpret_line

def transpile(filename, new_filename):
    with open(filename) as seafile, open(new_filename, "w") as cfile:
        write_header(cfile)

        line_number = -1
        scope = Scope(cfile)

        try:
            for line_number, line in enumerate(seafile):
                try:
                    interpret_line(scope, line)
                except Continue:
                    continue

            scope.close_all()
        except TranspilerError as e:
            print_error(line_number, seafile, cfile, e)

def write_header(cfile):
    cfile.write("#define true 1\n")
    cfile.write("#define false 0\n")
    cfile.write("\n")

def print_error(line_number, seafile, cfile, error):
    to_print = f"Line #{line_number + 1} of {seafile.name}:\n{error.message}"

    print(to_print)
    cfile.write("// Transpilation stopped due to error\n")
    cfile.write(f"/* {to_print} */\n")
