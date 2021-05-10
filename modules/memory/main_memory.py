import struct
from .memory import Memory

class MainMemory:
    @property
    def stack(self):
        return self.stacks[-1]

    def __init__(self):
        self.stacks = [Memory()]
        self.heap = Memory()
        self.table = {}
        self.init_globals()

    def __repr__(self):
        table = f"Table: {self.table}"
        stacks = f"Stacks: {self.stacks}"
        heap = f"Heap: {self.heap}"

        return f"{table}\n\t{stacks}\n\t{heap}"

    def init_globals(self):
        self.implicit_new("bool", "true", 1)
        self.implicit_new("bool", "false", 0)
        self.implicit_new("bool", "null", 0)

    def implicit_new(self, keyword, identifier, value):
        value = type(self).convert_to_value(keyword, value)
        pointer = self.stack.new(value)

        if identifier not in self.table:
            self.table[identifier] = {}

        self.table[identifier][len(self.stacks) - 1] = (pointer[0], keyword)

    def contains(self, identifier, stack = None):
        in_any = identifier in self.table

        if stack is None:
            return in_any

        if not in_any:
            return False

        return stack in self.table[identifier]

    def access(self, identifier):
        partial_pointer, memory = self.get_identifier_pair(identifier)
        address = partial_pointer[0]
        size = type(self).size_of_type(partial_pointer[1])

        return memory.access(address, size)

    def modify(self, identifier, value):
        partial_pointer, memory = self.get_identifier_pair(identifier)
        address = partial_pointer[0]
        value = type(self).convert_to_value(partial_pointer[1], value)

        memory.modify(address, value)

    def remove(self, identifier):
        partial_pointer, memory = self.get_identifier_pair(identifier)
        address = partial_pointer[0]
        size = type(self).size_of_type(partial_pointer[1])

        memory.remove(address, size)

    def get_identifier_pair(self, identifier):
        table = self.table[identifier]
        stack = max(table.keys())

        partial_pointer = table[stack]
        memory = self.heap if stack < 0 else self.stacks[stack]

        return partial_pointer, memory

    def add_stack(self):
        stack = Memory()
        self.stacks += [stack]

        return stack

    def remove_stack(self):
        self.stacks = self.stacks[:-1]

    @classmethod
    def size_of_type(cls, keyword):
        return {
            "bool": 1,
            "int": 4,
            "float": 4
        }[keyword]

    @classmethod
    def convert_to_value(cls, keyword, value):
        c = cls.get_struct_char(keyword)
        return [(bin(x)).replace("0b", "").rjust(8, "0") for x in struct.pack(f"!{c}", value)]

    @classmethod
    def convert_from_value(cls, keyword, value):
        c = cls.get_struct_char(keyword)
        return struct.unpack(f"!{c}", bytes(int(byte, 2) for byte in value))[0]

    @classmethod
    def get_struct_char(cls, keyword):
        return {
            "bool": "?",
            "int": "i",
            "float": "f"
        }[keyword]
