from .general import InStream, OutStream, ErrorStream

class FileInStream(InStream):
    def __init__(self, filepath, filename = None):
        if filename is None:
            filename = filepath.split("/")[-1]

        self.file = open(filepath, "r", encoding = "UTF-8")
        super().__init__(filename)

    def __del__(self):
        self.file.close()

    def read_symbol(self):
        return self.file.read(1)

class FileOutStream(OutStream):
    def __init__(self, filepath, filename = None):
        if filename is None:
            filename = filepath.split("/")[-1]

        self.file = open(filepath, "w", encoding = "UTF-8")
        super().__init__(filename)

    def __del__(self):
        self.file.close()

    def write(self, data):
        self.file.write(data)

class FileErrorStream(ErrorStream):
    def __init__(self, filepath, filename = None):
        if filename is None:
            filename = filepath.split("/")[-1]

        self.file = open(filepath, "w", encoding = "UTF-8")
        super().__init__(filename)

    def write_error(self, error, data):
        self.file.write(data)
