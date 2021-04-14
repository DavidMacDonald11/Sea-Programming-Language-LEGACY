from modules.lexer.position import Position

class ASTNode:
    def __init__(self, position):
        self.position = position

    def get_children(self):
        return tuple()


class NumberNode(ASTNode):
    def __init__(self, token):
        self.token = token
        super().__init__(token.position)

    def __repr__(self):
        return f"{self.token}"

class UnaryOperationNode(ASTNode):
    def __init__(self, operation, right):
        self.operation = operation
        self.right = right

        super().__init__(Position(operation.position.start, right.position.end))

    def __repr__(self):
        return f"({self.operation}, {self.right})"

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        return f"({self.left}, {self.operation}, {self.right})"

class TernaryOperationNode(ASTNode):
    def __init__(self, left, left_operation, middle, right_operation, right):
        self.left = left
        self.left_operation = left_operation
        self.middle = middle
        self.right_operation = right_operation
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        left = f"({self.left}, {self.left_operation}, "
        return left + f"{self.middle}, {self.right_operation}, {self.right})"

class VariableAssignNode(ASTNode):
    def __init__(self, variable_type, variable, value):
        self.type = variable_type
        self.variable = variable
        self.value = value

        super().__init__(variable.position)

    def __repr__(self):
        return f"{self.type}, {self.variable}, TT.EQUALS, {self.value}"

class VariableAccessNode(ASTNode):
    def __init__(self, variable):
        self.variable = variable
        super().__init__(variable.position)

    def __repr__(self):
        return f"{self.variable}"

class EofNode(ASTNode):
    def __init__(self, eof_token):
        self.eof_token = eof_token
        super().__init__(eof_token.position)

    def __repr__(self):
        return f"{self.eof_token}"

class LineNode(ASTNode):
    def __init__(self, expression, depth, is_if = False):
        self.expression = expression
        self.depth = depth
        self.is_if = is_if

        super().__init__(expression.position)

    def __repr__(self):
        return f"[{self.expression}]"

class SequentialOperationNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

        super().__init__(Position(left.position.start, right.position.end))

    def __repr__(self):
        return f"({self.left} THEN {self.right})"

class IfNode(ASTNode):
    def __init__(self, if_token, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        position_start = if_token.position.start
        position_end = (else_case or cases[-1][1]).position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        else_str = "" if not self.else_case else f" ELSE {{{self.else_case}}}"
        return f"IF {{{self.cases}}}" + else_str
