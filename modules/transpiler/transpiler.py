from modules.lexer.lexer import Lexer
from modules.lexer.position import Position
from modules.lexer.errors import LexerError
from modules.parser.parser import Parser
from modules.parser.errors import ParserError
from .errors import HandledTranspilerError

def transpile(seafile_path, cfile_path):
    with open(seafile_path) as seafile, open(cfile_path, "w") as cfile:
        lexer = Lexer(seafile)

        try:
            try:
                tokens = lexer.make_tokens()
                print(tokens)
                parser = Parser(tokens)
                ast = parser.parse()
                print(ast)

                return True
            except LexerError as error:
                position = Position(lexer.file_position, lexer.end_position)
                raise HandledTranspilerError(position, error) from error
            except ParserError as error:
                position = error.token.position
                raise HandledTranspilerError(position, error) from error
        except HandledTranspilerError as error:
            print_error(position, cfile, error)
            return False

def print_error(position, cfile, error):
    to_print = f"{position}: {error.get_message()}"

    print(to_print)
    cfile.write("// Transpilation stopped due to error\n")
    cfile.write(f"/* {to_print} */\n")
