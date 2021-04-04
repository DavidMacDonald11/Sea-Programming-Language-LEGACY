from modules.visitor.io import Input
from modules.visitor.io import Output

class Terminal:
    def __init__(self):
        self.line = ""

class TerminalInput(Terminal, Input):
    @property
    def name(self):
        return "stdin"

    def read(self):
        if self.line == "":
            return None

        c = self.line[0]
        self.line = self.line[1:]
        return c


class TerminalOutput(Terminal, Output):
    def write(self, string):
        print(string)
