from .scope import EmptyScope

class GlobalScope(EmptyScope):
    sea_declaration = None
    c_declaration = None
    sea_ending = None

    def __init__(self):
        super().__init__(0, None)

    def open(self, cfile):
        pass

    def close(self, cfile):
        pass
