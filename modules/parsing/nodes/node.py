import re
from abc import ABC, abstractmethod

class Node(ABC):
    @property
    def node_name(self):
        return type(self).__name__[:-4]

    def __init__(self, *components):
        self.components = components
        self.position = components[0].position.copy()
        self.position.end = components[-1].position.end.copy()

    def __repr__(self):
        tree = self.tree_repr(2).split("\n")
        lines = [re.sub(".\b", "", line) for line in tree]
        table = [[line[i] for i in range(7, len(line), 8)] for line in lines]

        longest = len(max(table, key = len))

        for i, row in enumerate(table):
            table[i] = row + [""] * (longest - len(row))

        for i, row in enumerate(table):
            for j, symbol in enumerate(row):
                if symbol != "|":
                    continue

                if "├" not in str([table[k][j] for k in range(i)]).split("└")[-1]:
                    table[i][j] = " "

        result = [""] * len(lines)

        for j, line in enumerate(lines):
            table_i = -1

            for i, symbol in enumerate(line):
                if i % 8 == 7:
                    table_i += 1
                    result[j] += table[j][table_i]
                else:
                    result[j] += symbol

        return "\n".join(result)

    @abstractmethod
    def tree_repr(self, depth):
        pass

    def tree_parts(self, depth):
        return "\n" + "       |" * depth, "\b├── ", "\b└── "

    @classmethod
    @abstractmethod
    def construct(cls, parser):
        pass

    def visit(self, mode):
        return {
            "i": self.interpret,
            "t": self.transpile,
            "c": self.compile
        }[mode]()

    @abstractmethod
    def interpret(self):
        pass

    @abstractmethod
    def transpile(self):
        pass

    def compile(self):
        pass
