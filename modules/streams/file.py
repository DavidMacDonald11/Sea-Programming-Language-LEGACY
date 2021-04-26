from .basic import InStream, OutStream, ErrorStream

class File:
    def __init__(self, filename, method):
        self.file = open(filename, method)
        super().__init__(filename)

    def __del__(self):
        self.file.close()

class FileInStream(File, InStream):
    def __init__(self, filename):
        super().__init__(filename, "r")

    def read(self, amount = 1):
        return self.file.read(amount)

class FileOutStream(File, OutStream):
    def __init__(self, filename):
        super().__init__(filename, "w")

    def write(self, data):
        self.file.write(data)

class FileErrorStream(File, ErrorStream):
    def __init__(self, filename):
        super().__init__(filename, "w")

    def write_error(self, error, data):
        self.file.write(data)
