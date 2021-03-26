from .errors import TranspilerError
from .block import interpret_line
from .block import Continue
from .block_state import BlockState

def transpile(filename, new_filename):
    with open(filename) as seafile, open(new_filename, "w") as cfile:
        write_header(cfile)

        line_number = -1
        BlockState.restart(cfile)

        try:
            for line_number, line in enumerate(seafile):
                try:
                    interpret_line(line)
                except Continue:
                    continue

            BlockState.close_all()
            return True
        except TranspilerError as e:
            print_error(line_number, seafile, cfile, e)
            return False

def write_header(cfile):
    cfile.write("#define true 1\n")
    cfile.write("#define false 0\n")
    cfile.write("\n")

def print_error(line_number, seafile, cfile, error):
    to_print = f"Line #{line_number + 1} of {seafile.name}: {error.get_message()}"

    print(to_print)
    cfile.write("// Transpilation stopped due to error\n")
    cfile.write(f"/* {to_print} */\n")
