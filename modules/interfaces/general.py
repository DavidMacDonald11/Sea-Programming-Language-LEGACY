from parser.parser import Parser
from parser.errors import ParserError
from lexer.lexer import Lexer
from lexer.errors import LexerError
from preprocessor.preprocessor import PreProcessor
from errors.errors import SeaError

def main(streams, debug):
    try:
        preprocessor = lexer = parser = None
        in_file = None

        preprocessor = PreProcessor(streams.in_stream)
        in_file = preprocessor.make_processed_file()

        LexerError.lexer = lexer = Lexer(in_file)
        lexer.make_tokens()

        ParserError.parser = parser = Parser(lexer)
        parser.make_ast()
    except SeaError as error:
        streams.error_stream.write(error)
    finally:
        print_debug_info(debug, streams.debug_stream, lexer, parser)

def print_debug_info(debug, debug_stream, lexer, parser):
    if not debug:
        return

    debug_stream.write(f"Tokens: {None if lexer is None else lexer.tokens}\n")
    debug_stream.write(f"AST: {None if parser is None else parser.ast}\n")
