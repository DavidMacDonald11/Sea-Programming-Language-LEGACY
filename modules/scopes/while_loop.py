from modules.transpiler import conditionals
from .scope import Scope

class WhileLoop(Scope):
    sea_declaration = r"while .+:"
    c_ending = "}\n"

    def get_declaration(self):
        line = self.declaration.replace("while", "", 1)[:-1].strip()
        line = conditionals.transpile(line)
        return f"while({line}) {{"
