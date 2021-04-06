from modules.errors.errors import HandledSeaError
from modules.lexer.lexer import Lexer
from modules.lexer.errors import LexerError
from modules.parser.parser import Parser
from modules.parser.errors import ParserError
from .errors import VisitorError

def visit(io, visitor_type, debug = False):
    try:
        try:
            lexer = Lexer(io.input_stream)
            tokens = lexer.make_tokens()

            parser = Parser(tokens)
            ast = parser.parse()

            visitor = visitor_type(io.output_stream)
            visitor.traverse(ast)

            return True
        except LexerError as error:
            position = lexer.position
            raise HandledSeaError(position, error) from error
        except ParserError as error:
            position = error.token.position
            raise HandledSeaError(position, error) from error
        except VisitorError as error:
            position = error.node.position
            raise HandledSeaError(position, error) from error
    except HandledSeaError as error:
        print_error(position, io.output_stream, error)
        return False
    finally:
        if debug:
            create_debug_file(io.debug_stream, tokens, ast)

def print_error(position, output_stream, error):
    to_print = f"{position}: {error.get_message()}"

    print(to_print)
    output_stream.write("// Transpilation stopped due to error\n")
    output_stream.write(f"/* {to_print} */\n")

def create_debug_file(debug_stream, tokens, ast):
    debug_stream.write(f"Tokens: \n{tokens} \n")
    debug_stream.write(f"AST: \n{ast} \n")
