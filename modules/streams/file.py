from .basic import InStream, OutStream

class FileInStream(InStream):
    def __init__(self, filename):
        self.file = open(filename, "r")
        super().__init__(filename)

    def __del__(self):
        self.file.close()

    def read(self, amount = 1):
        return self.file.read(amount)

class FileOutStream(OutStream):
    def __init__(self, filename):
        self.file = open(filename, "w")
        super().__init__(filename)

    def __del__(self):
        self.file.close()

    def write(self, data):
        self.file.write(data)
