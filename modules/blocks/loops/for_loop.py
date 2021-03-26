from modules.transpiler import conditionals
from ..basic.block import Block
from ..basic.block import BlockDeclarationError

class ForLoop(Block):
    def get_declaration(self):
        line = self.declaration.replace("for", "", 1)[:-1]

        is_for_each = " in " in line
        parts = ranged_for_parts(line) if is_for_each else for_each_parts(line)

        return f"for({parts[0]}; {parts[1]}; {parts[2]}) {{"

    def get_ending(self):
        return "}\n"

    @classmethod
    def check_match(cls, line):
        return cls.matches_pattern(cls.declaration_pattern, line)

    @classmethod
    def get_declaration_pattern(cls):
        return r"for .+:"

class ForLoopDeclarationError(BlockDeclarationError):
    def get_message(self):
        return "For loop was declared incorrectly."

def ranged_for_parts(line):
    parts = ready_parts(line, " in ", 2)

    name = f"({parts[0]})"
    array = f"({parts[1]})"

    parts = [f"typeof(*{array}) *{name} = {array}"]
    parts += [f"{name} - {array} < sizeof({array}) / sizeof(*{array})"]
    parts += [f"++{name}"]

    return parts

def for_each_parts(line):
    parts = ready_parts(line, ";", 3)
    parts[1] = conditionals.transpile(parts[1])

    return parts

def ready_parts(line, splitter, required):
    parts = line.split(splitter)

    if len(parts) != required:
        raise ForLoopDeclarationError()

    return list(map(lambda x: x.strip(), parts))
