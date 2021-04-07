from types import SimpleNamespace

class ReprNamespace(SimpleNamespace):
    def __repr__(self):
        return self.repr()
