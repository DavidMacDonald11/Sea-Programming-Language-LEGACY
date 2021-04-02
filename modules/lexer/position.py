class Position:
    def __init__(self, start = None, end = None):
        self.start = start
        self.end = end

    def __repr__(self):
        if self.start is None:
            return "Unkown Position"

        if self.end is None or self.end == self.start:
            return f"{self.start}"

        start = f"Line {self.start.line}"
        ending = f"Col {self.start.column} to {self.end.column} of {self.end.filename}"

        if self.end.line == self.start.line:
            return f"{start}, {ending}"

        return f"{start} to {self.end.line}, {ending}"

class FilePosition:
    def __init__(self, file, line = 1, column = -1):
        self.line = line
        self.column = column
        self.filename = file.name

    def __eq__(self, position):
        return self.line == position.line and self.column == position.column

    def __repr__(self):
        return f"Line {self.line}, Col {self.column} of {self.filename}"

    def copy(self):
        file = FilePosition.FakeFile(self.filename)
        return FilePosition(file, self.line, self.column)

    def next(self):
        self.column += 1

    def next_line(self):
        self.line += 1
        self.column = -1

    class FakeFile:
        def __init__(self, filename):
            self.name = filename
