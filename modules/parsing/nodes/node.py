from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = tokens[0].position.copy()
        self.position.end = tokens[-1].position.end.copy()

    def __repr__(self):
        return f"{type(self).__name__}{self.tokens}"

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
