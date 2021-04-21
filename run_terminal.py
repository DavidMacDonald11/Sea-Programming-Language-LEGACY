import sys
from modules.visitor.io import new_io
from modules.visitor.io import new_null_output
from modules.visitor.main import visit
from modules.visitor.print_warnings import init_global_warning
from modules.visitor.io import TERMINAL
from modules.visitor.io import new_terminal_input
from modules.visitor.io import new_terminal_output

def main():
    debug = sys.argv[1] == "True"
    io = new_io(new_terminal_input(), new_terminal_output(), new_null_output())

    init_global_warning(io.output_stream)

    retain_info = None
    print("Sea Programming Language")

    try:
        while True:
            TERMINAL.line = input("sea > ")

            if TERMINAL.line == "":
                continue

            if TERMINAL.line == "exit":
                raise EOFError()

            if TERMINAL.line in ("debug", "nodebug"):
                debug = TERMINAL.line == "debug"
                continue

            TERMINAL.line += "\n"

            if TERMINAL.line.rstrip()[-1] == ":":
                TERMINAL.line += "\n"

                line = ""

                while line != "\n":
                    line = input("...   ") + "\n"
                    TERMINAL.line += line

            retain_info = visit(io, "Interpreter", debug, True, retain_info)
    except KeyboardInterrupt:
        print()
    except EOFError:
        pass

if __name__ == "__main__":
    main()
