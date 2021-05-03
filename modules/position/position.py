from .char_position import CharPosition

class Position:
    def __init__(self, stream, start = None, end = None):
        self.stream = stream
        self.start = start if start is not None else CharPosition()
        self.end = end if end is not None else self.start.copy()

    def __repr__(self):
        line = f"Line {self.start.line}"
        column = f"Col {self.start.column}"
        stream = f"of {self.stream.name}"

        if self.start.column != self.end.column:
            column += f" to {self.end.column}"

        if self.start.line != self.end.line:
            line += f" to {self.end.line}"

        return f"{line}, {column} {stream}"

    def copy(self):
        positions = (self.start, self.end)
        positions = tuple(map(lambda x: x if x is None else x.copy(), positions))

        return Position(self.stream, *positions)
