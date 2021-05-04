from position.position import Position
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
        pass

    def transpile(self, memory):
        pass
