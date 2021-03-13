from .error import TranspilerError

def get_from_line(line):
    count = spaces = 0

    for c in line:
        if not c.isspace():
            break

        if c not in (" ", "\t"):
            spaces = 1
            break

        spaces += int(c == " ")

        if c == "\t":
            count += 1
            continue

        if spaces == 4:
            spaces = 0
            count += 1

    if spaces > 0:
        raise IndentError()

    return count

class IndentError(TranspilerError):
    def __init__(self, message = "Indents must be 4 spaces or 1 tab."):
        super().__init__(message)
