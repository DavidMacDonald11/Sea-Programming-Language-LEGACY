from modules.transpiler.errors import TranspilerError

def count_in_line(line):
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

def remove(line, amount):
    if amount < 1:
        return line

    if line[0] == "\t":
        return remove(line[1:], amount - 1)

    if len(line) < 4 or line[0:4] != " " * 4:
        return line

    return remove(line[4:], amount - 1)

class IndentError(TranspilerError):
    def __init__(self, message = "Indents must be 4 spaces or 1 tab."):
        super().__init__(message)
