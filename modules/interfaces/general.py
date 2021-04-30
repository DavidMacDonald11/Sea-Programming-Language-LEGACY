from preprocessor.preprocessor import PreProcessor
from lexer.lexer import Lexer
from lexer.errors import LexerError
from errors.errors import SeaError

def main(streams, debug):
    try:
        preprocessor = lexer = None
        in_file = None

        preprocessor = PreProcessor(streams.in_stream)
        in_file = preprocessor.make_processed_file()

        LexerError.lexer = lexer = Lexer(in_file)
        lexer.make_tokens()
    except SeaError as error:
        streams.error_stream.write(error)
    finally:
        print_debug_info(debug, streams.debug_stream, lexer)

def print_debug_info(debug, debug_stream, lexer):
    if not debug:
        return

    debug_stream.write(f"Tokens: {None if lexer is None else lexer.tokens}\n")
