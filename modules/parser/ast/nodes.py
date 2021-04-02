from modules.lexer.position import Position

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.position = token.position

    def __repr__(self):
        return f"{self.token}"

class BinaryOperationNode:
    def __init__(self, left_node, operation_token, right_node):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node
        self.position = Position(left_node.position.start, right_node.position.end)

    def __repr__(self):
        return f"({self.left_node}, {self.operation_token}, {self.right_node})"

class UnaryOperationNode:
    def __init__(self, operation_token, node):
        self.operation_token = operation_token
        self.node = node
        self.position = Position(operation_token.position.start, node.position.end)

    def __repr__(self):
        return f"({self.operation_token}, {self.node})"
