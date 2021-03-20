from .scope import EndableScope

class DoWhileLoop(EndableScope):
    sea_declaration = "do:"
    c_declaration = "do {"
    sea_ending = r"\s*while [^:]+"

    def get_ending(self):
        ending = super().get_ending()
        line = ending.replace("while", "", 1).strip()

        return f"}} while({line});"
