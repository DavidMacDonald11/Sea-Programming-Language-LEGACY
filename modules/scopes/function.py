from .scope import Scope

class FunctionScope(Scope):
    sea_declaration = r"[^():]+\([^():]*\):"
    c_ending = "}\n"

    def get_declaration(self):
        line = self.declaration[:-1]

        parts = line.split("(")
        parts[1] = parts[1][:-1]

        return f"{parts[0]}({parts[1]}) {{"
