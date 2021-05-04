class Memory:
    def __init__(self):
        self.values = []

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
        return self.values[address:address + size]

    def modify(self, address, value):
        prior = self.values[:address]
        ensuing = self.values[address + len(value):]

        self.values = prior + value + ensuing

    def remove(self, address, size):
        empty_space = [None] * size
        self.modify(address, empty_space)
