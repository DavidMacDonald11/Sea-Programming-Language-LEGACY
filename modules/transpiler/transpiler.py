from modules.lexer.lexer import Lexer
from .errors import TranspilerError

def transpile(seafile_path, cfile_path):
    with open(seafile_path) as seafile, open(cfile_path, "w") as cfile:
        lexer = Lexer(seafile)

        try:
            tokens = lexer.make_tokens()
            print(tokens)

            return True
        except TranspilerError as error:
            print_error(lexer, seafile, cfile, error)
            return False

def print_error(lexer, seafile, cfile, error):
    to_print = f"Line #{lexer.line_count} of {seafile.name}: {error.get_message()}"

    print(to_print)
    cfile.write("// Transpilation stopped due to error\n")
    cfile.write(f"/* {to_print} */\n")
