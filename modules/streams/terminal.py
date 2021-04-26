from .basic import InStream, OutStream

class TerminalInStream(InStream):
    buffer = ""

    def __init__(self):
        super().__init__("stdin")

    def read(self, amount = 1):
        c = type(self).buffer[0:1]
        type(self).buffer = type(self).buffer[1:]

        return c

class TerminalOutStream(OutStream):
    def __init__(self):
        super().__init__("stdout")

    def write(self, data):
        print(data, end = "")
