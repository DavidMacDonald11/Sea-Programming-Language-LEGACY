from modules.errors.errors import HandledSeaError
from modules.lexer.lexer import Lexer
from modules.lexer.errors import LexerError
from modules.parser.parser import Parser
from modules.parser.errors import ParserError
from modules.transpiler.transpiler import Transpiler
from modules.interpreter.interpreter import Interpreter
from .errors import VisitorError

def visit(io, visitor_type, debug = False, retain = False, retain_info = None):
    try:
        lexer = parser = visitor = None
        tokens = ast = None

        if retain_info is None:
            retain_info = (None, None, None)

        try:
            lexer = Lexer(io.input_stream)
            tokens = lexer.make_tokens()

            parser = Parser(tokens)
            ast = parser.parse()

            visitor = visitor_type(io.output_stream) if retain_info[2] is None else retain_info[2]
            visitor.traverse(ast)

            return True if not retain else (lexer, parser, visitor)
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
        print_error(visitor_type, position, io, error)
        return False if not retain else (lexer, parser, visitor)
    finally:
        if debug:
            create_debug_file(io.debug_stream, tokens, ast)

def print_error(visitor_type, position, io, error):
    to_print = f"{error.get_name()} at {position}: {error.get_message()}"

    io.error_stream.write(f"{to_print}\n")

    if visitor_type is Transpiler:
        io.output_stream.write("// Transpilation stopped due to error\n")
        io.output_stream.write(f"/* {to_print} */\n")
    elif visitor_type is Interpreter:
        io.output_stream.write(f"{to_print}\n")

def create_debug_file(debug_stream, tokens, ast):
    debug_stream.write(f"Tokens: {tokens} \n")
    debug_stream.write(f"AST: {ast} \n")
