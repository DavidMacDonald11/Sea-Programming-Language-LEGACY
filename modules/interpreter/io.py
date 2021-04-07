from types import SimpleNamespace
from modules.visitor.io import new_input
from modules.visitor.io import new_output

TERMINAL = SimpleNamespace()
TERMINAL.line = ""

def new_terminal_input():
    def read():
        if TERMINAL.line == "":
            return None

        c = TERMINAL.line[0]
        TERMINAL.line = TERMINAL.line[1:]

        return c

    return new_input("stdin", read)

def new_terminal_output():
    def write(string):
        print(string, end = "")

    return new_output(write)
