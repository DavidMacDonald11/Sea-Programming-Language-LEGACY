from modules.helpers.repr_namespace import ReprNamespace
from modules.lexer.position import Position

def new_ast_node(position):
    node = ReprNamespace()
    node.position = position

    return node

def new_number_node(token):
    node = new_ast_node(token.position)
    node.token = token

    def node_repr():
        return f"{node.token}"

    node.repr = node_repr
    node.__name__ = "NumberNode"

    return node

def new_binary_operation_node(left_node, operation_token, right_node):
    node = new_ast_node(Position(left_node.position.start, right_node.position.end))

    node.left_node = left_node
    node.operation_token = operation_token
    node.right_node = right_node

    def node_repr():
        return f"({node.left_node}, {node.operation_token}, {node.right_node})"

    node.repr = node_repr
    node.__name__ = "BinaryOperationNode"

    return node

def new_unary_operation_node(operation_token, right_node):
    node = new_ast_node(Position(operation_token.position.start, right_node.position.end))

    node.operation_token = operation_token
    node.node = right_node

    def node_repr():
        return f"({node.operation_token}, {node.node})"

    node.repr = node_repr
    node.__name__ = "UnaryOperationNode"

    return node

def new_var_assign_node(keyword_token, variable_token, value_node):
    node = new_ast_node(variable_token.position)

    node.keyword_token = keyword_token
    node.variable_token = variable_token
    node.value_node = value_node

    def node_repr():
        return f"{node.keyword_token} {node.variable_token} = {node.value_node}"

    node.repr = node_repr
    node.__name__ = "VariableAssignNode"

    return node

def new_var_access_node(variable_token):
    node = new_ast_node(variable_token.position)
    node.variable_token = variable_token

    def node_repr():
        return f"{node.variable_token}"

    node.repr = node_repr
    node.__name__ = "VariableAccessNode"

    return node
