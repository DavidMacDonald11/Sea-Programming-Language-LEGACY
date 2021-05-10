from position.position import Position
from visiting import errors
from .ast_node import ASTNode

class VariableAssignNode(ASTNode):
    def __init__(self, keyword, identifier, value):
        self.keyword = keyword
        self.identifier = identifier
        self.value = value

        super().__init__(Position(keyword.position.start, value.position.end))

    def __repr__(self):
        return f"({self.keyword}, {self.identifier}, EQUALS, {self.value})"

    def interpret(self, memory):
        keyword = self.keyword.data
        identifier = self.identifier.data
        value = self.value.interpret(memory)

        if memory.contains(identifier, memory.scope_id):
            raise errors.RedeclaredIdentifierError(self, identifier)

        memory.implicit_new(keyword, identifier, value)

        return value

    def transpile(self, memory):
        self.interpret(memory.memory)

        keyword = self.keyword.data
        identifier = self.identifier.data
        tvalue = self.value.transpile(memory)

        memory.new(keyword, identifier, tvalue)
        return f"{keyword} {identifier} = {tvalue}"
