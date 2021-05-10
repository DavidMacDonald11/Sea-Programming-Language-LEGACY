from .main_memory import MainMemory

class ContainedMemory:
    def __init__(self):
        self.memory = MainMemory()
        self.table = {}

    def __repr__(self):
        table = f"Contained Table: {self.table}"
        return f"{table}\n\t{self.memory}"

    def new(self, keyword, identifier, value):
        self.table[identifier] = [keyword, value]

    def contains(self, identifier):
        return identifier in self.table

    def access(self, identifier):
        return self.table.get(identifier, None)

    def modify(self, identifier, value):
        self.table[identifier][1] = value

    def remove(self, identifier):
        del self.table[identifier]
