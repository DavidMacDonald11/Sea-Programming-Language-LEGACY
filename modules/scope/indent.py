from modules.transpiler.error import TranspilerError

def get_from_line(line):
    line = line.rstrip()
    count = 0
    spaces = 0

    for c in line:
        if not c.isspace():
            break

        if c not in (" ", "\t"):
            spaces = 1
            break

        spaces += int(c == " ")

        if c == "\t" or spaces == 4:
            if spaces == 4:
                spaces = 0

            count += 1

    if spaces > 0:
        raise IndentError("Indents must be 4 spaces or 1 tab.")

    return count

class IndentError(TranspilerError):
    pass
