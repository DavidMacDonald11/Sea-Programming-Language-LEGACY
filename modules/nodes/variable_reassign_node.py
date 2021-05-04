from position.position import Position
from .ast_node import ASTNode

class VariableReassignNode(ASTNode):
    def __init__(self, identifier, operator, value = None, left = False):
        self.identifier = identifier
        self.operator = operator
        self.value = value
        self.left = left

        position_start = (operator if left else identifier).position.start

        right = identifier if left else identifier
        position_end = (value if value is not None else right).position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        value = "" if self.value is None else f", {self.value}"

        if self.left:
            return f"({self.operator}, {self.identifier}{value})"

        return f"({self.identifier}, {self.operator}{value})"
