from .errors import IndentError

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
