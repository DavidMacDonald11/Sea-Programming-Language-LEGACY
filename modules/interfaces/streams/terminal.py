from .general import InStream, OutStream, ErrorStream

class TerminalInStream(InStream):
    def __init__(self):
        self.buffer = ""
        super().__init__("stdin")

    def read_symbol(self):
        c = self.buffer[:1]
        self.buffer = self.buffer[1:]

        return c

class TerminalOutStream(OutStream):
    def __init__(self, out = None):
        self.out = out
        super().__init__("stdout")

    def write(self, data):
        if self.out is not None:
            self.out(data)
        else:
            print(data, end = "")

class TerminalErrorStream(ErrorStream):
    def __init__(self, out = None):
        self.out = out
        super().__init__("stderr")

    def write_error(self, error, data):
        if self.out is not None:
            self.out(data)
        else:
            print(data, end = "")
