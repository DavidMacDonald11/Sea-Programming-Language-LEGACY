class Memory:
    def __init__(self):
        self.values = []

    def __repr__(self):
        return f"{self.values}"

    def new(self, value):
        size = len(value)

        for address in range(len(self.values) - size + 1):
            possible = self.values[address:address + size]

            if possible != [None] * size:
                continue

            self.modify(address, value)
            return address, size

        address = len(self.values)
        self.values += value

        return address, size

    def access(self, address, size):
        values = self.values[address:address + size]
        return ["0" * 8 if value is None else value for value in values]

    def modify(self, address, value):
        prior = self.values[:address]
        ensuing = self.values[address + len(value):]
        self.values = prior + value + ensuing

    def remove(self, address, size):
        empty_space = [None] * size
        self.modify(address, empty_space)
