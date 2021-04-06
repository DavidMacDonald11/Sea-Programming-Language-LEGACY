from types import SimpleNamespace
from modules.lexer.position import Position

def new_ast_node(position):
    node = SimpleNamespace()
    node.position = position

    return node

def new_number_node(token):
    node = new_ast_node(token.position)
    node.token = token

    def node_repr():
        return f"{node.token}"

    node.__repr__ = node_repr
    node.__name__ = "NumberNode"

    return node

def new_binary_operation_node(left_node, operation_token, right_node):
    node = new_ast_node(Position(left_node.position.start, right_node.position.end))

    node.left_node = left_node
    node.operation_token = operation_token
    node.right_node = right_node

    def node_repr():
        return f"({node.left_node}, {node.operation_token}, {node.right_node})"

    node.__repr__ = node_repr
    node.__name__ = "BinaryOperationNode"

    return node

def new_unary_operation_node(operation_token, right_node):
    node = new_ast_node(Position(operation_token.position.start, right_node.position.end))

    node.operation_token = operation_token
    node.node = right_node

    def node_repr():
        return f"({node.operation_token}, {node.node})"

    node.__repr__ = node_repr
    node.__name__ = "UnaryOperationNode"

    return node
