from modules.helpers.errors import SeaError
from modules.lexer.lexer import Lexer
from modules.lexer.errors import LexerError
from modules.parser.parser import Parser
from .print_warnings import print_error

def visit(io, visitor_type, debug = False, retain = False, retain_info = None):
    try:
        lexer = parser = visitor = None
        tokens = ast = symbol_table = None

        if retain_info is None:
            retain_info = (None, None, None)

        lexer = Lexer(io.input_stream)
        LexerError.lexer = lexer

        tokens = lexer.make_tokens()

        parser = Parser(tokens)
        ast = parser.parse()

        visitor = visitor_type(io.output_stream) if retain_info[2] is None else retain_info[2]
        visitor.traverse(ast)
        symbol_table = visitor.symbol_table

        return True if not retain else (lexer, parser, visitor)
    except SeaError as error:
        print_error(visitor_type, io, error)
        return False if not retain else (lexer, parser, visitor)
    finally:
        if debug:
            create_debug_file(io.debug_stream, tokens, ast, symbol_table)

def create_debug_file(debug_stream, tokens, ast, symbol_table):
    debug_stream.write(f"Tokens: {tokens} \n")
    debug_stream.write(f"AST: {ast} \n")
    debug_stream.write(f"Symbols: {symbol_table} \n")
