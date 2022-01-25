from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, pos_carrier1, pos_carrier2):
        self.position = pos_carrier1.position.copy()

        if pos_carrier2 is not None:
            self.position.end = pos_carrier2.position.end.copy()

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
