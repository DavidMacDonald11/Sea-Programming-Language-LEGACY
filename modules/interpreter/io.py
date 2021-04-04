from modules.visitor.io import Input
from modules.visitor.io import Output

class Terminal:
    def __init__(self, terminal):
        self.terminal = terminal

class TerminalInput(Terminal, Input):
    @property
    def name(self):
        return "stdin"

    def read(self, chars):
        return "H"

class TerminalOutput(Terminal, Output):
    def write(self, string):
        print(string)
