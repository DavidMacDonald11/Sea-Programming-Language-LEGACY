class CharPosition:
    def __init__(self, line = 1, column = 0):
        self.line = line
        self.column = column

    def __eq__(self, position):
        return self.line == position.line and self.column == position.column

    def __repr__(self):
        return f"Line {self.line}, Col {self.column}"

    def copy(self):
        return CharPosition(self.line, self.column)

    def advance(self, amount = 1):
        self.column += amount

    def advance_line(self, amount = 1):
        self.line += amount
        self.column = 0
