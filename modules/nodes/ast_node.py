from abc import ABC, abstractmethod

class ASTNode(ABC):
    def __init__(self, position):
        self.position = position

    def visit(self, mode, memory):
        return {
            "i": self.interpret,
            "t": self.transpile,
            "c": self.compile
        }[mode](memory)

    @abstractmethod
    def interpret(self, memory):
        pass

    @abstractmethod
    def transpile(self, memory):
        pass

    def compile(self, memory):
        pass
