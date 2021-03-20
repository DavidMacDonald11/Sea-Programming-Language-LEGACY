from .scope import Scope
from .scope import ScopeDeclarationError

def ready_parts(line, splitter, required):
    parts = line.split(splitter)

    if len(parts) != required:
        raise ForLoopDeclarationError()

    return list(map(lambda x: x.strip(), parts))

class ForLoop(Scope):
    sea_declaration = r"for .+:"
    c_ending = "}\n"

    def get_declaration(self):
        line = self.declaration.replace("for", "", 1)[:-1]

        if " in " in line:
            parts = ready_parts(line, " in ", 2)

            name = f"({parts[0]})"
            array = f"({parts[1]})"

            parts = [f"typeof(*{array}) *{name} = {array}"]
            parts += [f"{name} - {array} < sizeof({array}) / sizeof(*{array})"]
            parts += [f"++{name}"]
        else:
            parts = ready_parts(line, ";", 3)

        return f"for({parts[0]}; {parts[1]}; {parts[2]}) {{"

class ForLoopDeclarationError(ScopeDeclarationError):
    def __init__(self, message = None):
        if message is None:
            message = "For loop was declared incorrectly."

        super().__init__(message)
