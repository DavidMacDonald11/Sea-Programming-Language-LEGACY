from types import SimpleNamespace

class Position:
    def __init__(self, start = None, end = None):
        self.start = start
        self.end = start if end is None else end

    def __repr__(self):
        if self.start is None:
            return "Unknown Position"

        if self.end == self.start:
            return f"{self.start}"

        line = f"Line {self.start.line}"
        column = f"Col {self.start.column}"
        file = f"of {self.start.filename}"

        if self.end.line == self.start.line:
            return f"{line}, {column} {file}"

        line = f"{line} to {self.end.line}"

        if self.end.column == self.start.column:
            return f"{line}, {column} {file}"

        return f"{line}, {column} to {self.end.column} {file}"

    def copy(self):
        position = (self.start, self.end)
        position = tuple(map(lambda x: x if x is None else x.copy(), position))

        return Position(*position)

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
        file = SimpleNamespace()
        file.name = self.filename

        return FilePosition(file, self.line, self.column)

    def next(self):
        self.column += 1

    def next_line(self):
        self.line += 1
        self.column = -1
