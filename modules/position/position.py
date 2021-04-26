class Position:
    def __init__(self, stream, start = None, end = None):
        self.stream = stream
        self.start = start
        self.end = end if end is not None else start

    def __repr__(self):
        if self.start is None:
            return "Unknown Position"

        line = f"Line {self.start.line}"
        column = f"Col {self.start.column}"
        stream = f"of {self.stream}"

        if self.start.column != self.end.column:
            column += f" to {self.end.column}"

        if self.start.line != self.end.line:
            line += f" to {self.end.line}"

        return f"{line}, {column} {stream}"

    def copy(self):
        positions = (self.start, self.end)
        positions = tuple(map(lambda x: x if x is None else x.copy(), positions))

        return Position(self.stream, *positions)
