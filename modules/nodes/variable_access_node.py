from visiting import errors
from .ast_node import ASTNode

class VariableAccessNode(ASTNode):
    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(identifier.position)

    def __repr__(self):
        return f"{self.identifier}"

    def interpret(self, memory):
        identifier = self.identifier.data

        if not memory.contains(identifier):
            raise errors.UndefinedIdentifierError(self, identifier)

        return memory.access(identifier)

    def transpile(self, memory):
        self.interpret(memory.memory)
        return f"{self.identifier.data}"
