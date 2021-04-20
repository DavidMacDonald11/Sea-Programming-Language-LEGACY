from abc import ABC
from abc import abstractmethod

class ASTNode(ABC):
    def __init__(self, position):
        self.position = position

    def visit(self, visitor):
        visitor_type = visitor.type

        return {
            "Interpreter": self.interpret,
            "Transpiler": self.transpile,
            "Compiler": self.compile
        }[visitor_type](visitor)

    @abstractmethod
    def interpret(self, interpreter):
        pass

    @abstractmethod
    def transpile(self, transpiler):
        pass

    def compile(self, compiler):
        pass
