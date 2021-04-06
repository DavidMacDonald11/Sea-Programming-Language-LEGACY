from abc import ABC
from abc import abstractmethod
from modules.lexer.position import Position

class ASTNode(ABC):
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def __repr__(self):
        pass

class NumberNode(ASTNode):
    def __init__(self, token):
        self.token = token
        super().__init__(token.position)

    def __repr__(self):
        return f"{self.token}"

class BinaryOperationNode(ASTNode):
    def __init__(self, left_node, operation_token, right_node):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

        super().__init__(Position(left_node.position.start, right_node.position.end))

    def __repr__(self):
        return f"({self.left_node}, {self.operation_token}, {self.right_node})"

class UnaryOperationNode(ASTNode):
    def __init__(self, operation_token, node):
        self.operation_token = operation_token
        self.node = node
        super().__init__(Position(operation_token.position.start, node.position.end))

    def __repr__(self):
        return f"({self.operation_token}, {self.node})"
