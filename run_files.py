import sys
from modules.helpers.file_handler import visit_files
from modules.interpreter.interpreter import Interpreter
from modules.compiler.compiler import Compiler
from modules.transpiler.transpiler import Transpiler

def main():
    visitors = {
        "transpile": (Transpiler, 3),
        "compile": (Compiler, 2),
        "interpret": (Interpreter, 1)
    }

    visit_files(sys.argv[2:], *visitors[sys.argv[1].lower()])

if __name__ == "__main__":
    main()
