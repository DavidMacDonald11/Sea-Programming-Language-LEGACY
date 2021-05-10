from preprocessing.preprocessor import PreProcessor
from lexing.lexer import Lexer
from lexing.errors import LexerError
from parsing.parser import Parser
from parsing.errors import ParserError
from errors.errors import SeaError
from memory.main_memory import MainMemory
from memory.contained_memory import ContainedMemory

def main(streams, debug, mode):
    try:
        preprocessor = lexer = parser = memory = None
        in_file = None

        preprocessor = PreProcessor(streams.in_stream)
        in_file = preprocessor.make_processed_file()

        LexerError.lexer = lexer = Lexer(in_file)
        lexer.make_tokens()

        ParserError.parser = parser = Parser(lexer)
        parser.make_ast()

        memory = MainMemory() if mode == "i" else ContainedMemory()
        streams.out_stream.write(f"{parser.ast.visit(mode, memory)}\n")
    except SeaError as error:
        streams.error_stream.write(error)
    finally:
        print_debug_info(debug, streams.debug_stream, lexer, parser, memory)

def print_debug_info(debug, debug_stream, lexer, parser, memory):
    if not debug:
        return

    debug_stream.write(f"\nTokens:\n\t{None if lexer is None else lexer.tokens}\n")
    debug_stream.write(f"AST:\n\t{None if parser is None else parser.ast}\n")
    debug_stream.write(f"Memory:\n\t{None if memory is None else memory}\n\n")
