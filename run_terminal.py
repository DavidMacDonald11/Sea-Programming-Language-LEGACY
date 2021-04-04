from modules.visitor.io import IO
from modules.visitor.io import NullOutput
from modules.visitor.main import visit
from modules.interpreter.io import TerminalInput
from modules.interpreter.io import TerminalOutput
from modules.interpreter.interpreter import Interpreter

def main():
    io = IO(TerminalInput(), TerminalOutput(), NullOutput())

    print("Sea Programming Language")

    try:
        while True:
            io.input_stream.line = input("sea > ")
            visit(io, Interpreter)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
