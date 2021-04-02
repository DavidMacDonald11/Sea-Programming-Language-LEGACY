from modules.lexer.lexer import Lexer
from modules.lexer.position import Position
from modules.lexer.errors import LexerError
from modules.parser.parser import Parser
from modules.parser.errors import ParserError
from modules.compiler.compiler import  Compiler
from modules.compiler.errors import CompilerError
from .errors import HandledTranspilerError

def transpile(seafile_path, cfile_path):
    with open(seafile_path) as seafile, open(cfile_path, "w") as cfile:
        lexer = Lexer(seafile)

        try:
            try:
                tokens = lexer.make_tokens()

                parser = Parser(tokens)
                ast = parser.parse()

                compiler = Compiler(cfile)
                cfile.write(compiler.visit(ast))

                return True
            except LexerError as error:
                position = Position(lexer.file_position, lexer.end_position)
                raise HandledTranspilerError(position, error) from error
            except ParserError as error:
                position = error.token.position
                raise HandledTranspilerError(position, error) from error
            except CompilerError as error:
                position = error.node.position
                raise HandledTranspilerError(position, error) from error
        except HandledTranspilerError as error:
            print_error(position, cfile, error)
            return False
        finally:
            create_debug_file(cfile_path, tokens, ast)


def print_error(position, cfile, error):
    to_print = f"{position}: {error.get_message()}"

    print(to_print)
    cfile.write("// Transpilation stopped due to error\n")
    cfile.write(f"/* {to_print} */\n")

def create_debug_file(cfile_path, tokens, ast):
    with open(cfile_path + ".debug", "w") as file:
        file.write(f"Tokens: \n{tokens} \n\n")
        file.write(f"AST: \n{ast} \n\n")
