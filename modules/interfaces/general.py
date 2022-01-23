from lexing.lexer import Lexer
from lexing.errors import LexerError
from errors.errors import SeaError

def interface(streams, debug, mode):
    try:
        lexer = None

        LexerError.lexer = lexer = Lexer(streams.in_stream)
        lexer.make_tokens()
    except SeaError as error:
        streams.error_stream.write(error)
    finally:
        print_debug_info(debug, streams.debug_stream, lexer)

def print_debug_info(debug, debug_stream, lexer):
    if not debug:
        return

    debug_stream.write(f"\nTokens:\n\t{None if lexer is None else lexer.tokens}\n")
