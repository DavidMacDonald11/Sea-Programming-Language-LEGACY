from modules.transpiler.errors import TranspilerError

def count_indent(line):
    count = 0

    while line[0].isspace():
        if line[0] == "\t":
            count += 1
            line = line[1:]
            continue

        if line[0] == " " and line[0:4] == " " * 4:
            count += 1
            line = line[4:]
            continue

        raise IndentError()

    return count

def remove_indent(line, amount):
    for _ in range(amount):
        if len(line) == 0:
            break

        if line[0] == "\t":
            line = line[1:]
            break

        if len(line) >= 4 and line[0:4] == " " * 4:
            line = line[4:]

    return line

class IndentError(TranspilerError):
    def get_message(self):
        return "Indents must be 4 spaces or 1 tab."
