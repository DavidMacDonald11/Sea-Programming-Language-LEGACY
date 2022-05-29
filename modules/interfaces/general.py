from lexing.lexer import Lexer
from lexing.errors import LexerError
from parsing.parser import Parser
from parsing.errors import ParserError
from errors.errors import SeaError

def interface(streams, debug, mode):
    try:
        lexer = parser = None

        LexerError.lexer = lexer = Lexer(streams.in_stream)
        lexer.make_tokens()

        ParserError.parser = parser = Parser(lexer)
        parser.make_nodes()
    except SeaError as error:
        streams.error_stream.write(error)
    finally:
        print_debug_info(debug, streams.debug_stream, lexer, parser)

def print_debug_info(debug, debug_stream, lexer, parser):
    if not debug:
        return

    debug_stream.write(f"Tokens:\n\t{None if lexer is None else lexer.tokens}")
    debug_stream.write(f"\nAST:\n\t{None if parser is None else parser.ast}\n")
