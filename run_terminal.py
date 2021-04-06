import sys
from modules.visitor.io import new_io
from modules.visitor.main import visit
from modules.interpreter.io import TERMINAL
from modules.interpreter.io import new_terminal_input
from modules.interpreter.io import new_terminal_output
from modules.interpreter.interpreter import Interpreter

def main():
    debug = sys.argv[1] == "True"
    io = new_io(new_terminal_input(), new_terminal_output())

    print("Sea Programming Language")

    try:
        while True:
            TERMINAL.line = input("sea > ")
            visit(io, Interpreter, debug)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
