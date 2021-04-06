import sys
from modules.visitor.io import IO
from modules.visitor.main import visit
from modules.interpreter.io import TerminalInput
from modules.interpreter.io import TerminalOutput
from modules.interpreter.interpreter import Interpreter

def main():
    debug = sys.argv[1] == "True"

    io = IO(TerminalInput(), TerminalOutput(), TerminalOutput())

    print("Sea Programming Language")

    try:
        while True:
            io.input_stream.line = input("sea > ")
            visit(io, Interpreter, debug)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
