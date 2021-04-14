class SymbolTable:
    def __init__(self, parent = None):
        self.symbols = {}
        self.parent = parent

    def __repr__(self):
        return "{" + ", ".join(f"{symbol}" for symbol in self.symbols.values()) + "}"

    def __getitem__(self, name):
        value = self.symbols.get(name, None)

        if value is None and self.parent is not None:
            return self.parent[name]

        return value

    def __setitem__(self, name, symbol):
        self.symbols[name] = symbol

    def __delitem__(self, name):
        del self.symbols[name]
