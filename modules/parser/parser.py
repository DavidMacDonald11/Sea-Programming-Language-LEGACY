from modules.lexer.position import Position
from modules.lexer.token_types import TT
from .nodes.collection import NODES
from ..parser import errors

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_i = -1
        self.token = None
        self.advance()

        self.depth = 0

    def take_token(self):
        token = self.token
        self.advance()
        return token

    def advance(self):
        self.token_i += 1

        if self.token_i < len(self.tokens):
            self.token = self.tokens[self.token_i]

        return self.token

    def parse(self):
        line = self.line()

        if isinstance(line, NODES.EOFNode):
            return line

        return NODES.SequentialOperationNode(line, self.parse())

    def atom(self):
        if self.token.type in (TT.INT, TT.FLOAT):
            return NODES.NumberNode(self.take_token())

        if self.token.type == TT.IDENTIFIER:
            return NODES.SymbolAccessNode(self.take_token())

        if self.token.type == TT.LPAREN:
            self.advance()
            node = self.expression()

            if self.token.type == TT.RPAREN:
                self.advance()
                return node

            raise errors.NoClosingParenthesisError(self.token)

        raise errors.AtomError(self.token)

    def power(self):
        return self.binary_operation(self.atom, (TT.POWER,), self.factor)

    def factor(self):
        if self.token.type in (TT.PLUS, TT.MINUS):
            operation_token = self.take_token()
            return NODES.LeftUnaryOperationNode(operation_token, self.factor())

        return self.power()

    def term(self):
        return self.binary_operation(self.factor, (TT.MULTIPLY, TT.DIVIDE))

    def arithmetic_expression(self):
        return self.binary_operation(self.term, (TT.PLUS, TT.MINUS))

    def comparison_expression(self):
        if self.token.matches(TT.KEYWORD, "not"):
            operation_token = self.take_token()
            node = self.comparison_expression()

            return NODES.LeftUnaryOperationNode(operation_token, node)

        operations = (TT.EQ, TT.NE, TT.LT, TT.GT, TT.LTE, TT.GTE)

        return self.binary_operation(self.arithmetic_expression, operations)

    def boolean_and_expression(self):
        return self.binary_operation(self.comparison_expression, ((TT.KEYWORD, "and"), ))

    def boolean_or_expression(self):
        return self.binary_operation(self.boolean_and_expression, ((TT.KEYWORD, "or"), ))

    def expression(self):
        if not self.token.matches_type_keyword():
            operations = [(TT.KEYWORD, "if"), (TT.KEYWORD, "else")]
            return self.ternary_operation(self.boolean_or_expression, operations)

        keyword_token = self.take_token()

        if self.token.type is not TT.IDENTIFIER:
            raise errors.NoIdentifierError(self.token)

        variable_token = self.take_token()

        if self.token.type is not TT.EQUALS:
            raise errors.NoEqualsError(self.token)

        self.advance()

        return NODES.VariableAssignNode(keyword_token, variable_token, self.expression())

    def if_expression(self):
        cases = []
        else_case = None

        if_token = self.take_token()
        condition = self.expression()
        self.colon()

        cases += [(condition, self.block_or_expression())]

        while self.token.matches(TT.KEYWORD, "elif"):
            self.advance()
            condition = self.expression()
            self.colon()

            cases += [(condition, self.block_or_expression())]

        if self.token.matches(TT.KEYWORD, "else"):
            self.advance()
            self.colon()

            else_case = self.block_or_expression()

        return NODES.IfNode(if_token, cases, else_case)

    def line(self):
        if self.token.type is TT.EOF:
            return NODES.EOFNode(self.take_token())

        if self.token.type is TT.NEWLINE:
            self.advance()
            return self.line()

        indent_start = self.token.position.start
        depth = 0

        while self.token.type is TT.INDENT:
            self.advance()
            depth += 1

        indent_position = Position(indent_start, self.token.position.end)

        if depth > self.depth:
            block_error_info = (self.depth, depth, indent_position)
            raise errors.IncorrectBlockError(*block_error_info)

        if depth < self.depth:
            return (depth, indent_position)

        if self.token.value == "undefine":
            return NODES.LineNode(self.undefine_line(), depth, True)

        if self.token.value == "define":
            return NODES.LineNode(self.define_line(), depth, True)

        if self.token.value == "if":
            return NODES.LineNode(self.if_expression(), depth, True)

        expression = self.expression()

        if self.token.type not in (TT.NEWLINE, TT.EOF):
            raise errors.NoLineTerminationError(self.token)

        self.advance()

        return NODES.LineNode(expression, depth)

    def block(self):
        self.depth += 1
        left = self.line()

        if not is_normal(left):
            depth, indent_position = left
            block_error_info = (self.depth, depth, indent_position)

            raise errors.IncorrectBlockError(*block_error_info)

        block = left
        right = self.line()

        while is_normal(right):
            block = NODES.SequentialOperationNode(block, right)
            right = self.line()

        self.depth -= 1
        return block

    def binary_operation(self, left_func, operations, right_func = None):
        if right_func is None:
            right_func = left_func

        left = left_func()
        token_type_value = (self.token.type, self.token.value)

        while self.token.type in operations or token_type_value in operations:
            operation = self.take_token()
            right = right_func()
            left = NODES.BinaryOperationNode(left, operation, right)

            token_type_value = (self.token.type, self.token.value)

        return left

    def ternary_operation(self, left_func, operations, right_func = None):
        if right_func is None:
            right_func = left_func

        left = left_func()
        token_type_value = (self.token.type, self.token.value)

        if self.token.type not in operations[0] and token_type_value not in operations[0]:
            return left

        left_operation = self.take_token()
        middle = right_func()

        token_type_value = (self.token.type, self.token.value)

        if self.token.type not in operations[1] and token_type_value not in operations[1]:
            return NODES.BinaryOperationNode(left, left_operation, middle)

        right_operation = self.take_token()
        right = right_func()

        operations = (left_operation, right_operation)
        values = (left, middle, right)

        return NODES.TernaryOperationNode(operations, values)

    def define_line(self):
        define_token = self.take_token()

        if self.token.type is not TT.IDENTIFIER:
            raise errors.NoIdentifierError(self.token)

        name = self.take_token()

        if not self.token.matches(TT.KEYWORD, "as"):
            raise errors.NoAsError(self.token)

        self.advance()

        expression = self.expression()

        if self.token.type not in (TT.NEWLINE, TT.EOF):
            raise errors.NoLineTerminationError(self.token)

        self.advance()

        return NODES.ConstantDefineNode(define_token, name, expression)

    def undefine_line(self):
        undefine_token = self.take_token()

        if self.token.type is not TT.IDENTIFIER:
            raise errors.NoIdentifierError(self.token)

        name = self.take_token()

        if self.token.type not in (TT.NEWLINE, TT.EOF):
            raise errors.NoLineTerminationError(self.token)

        self.advance()

        return NODES.ConstantUndefineNode(undefine_token, name)

    def block_or_expression(self):
        if self.token.type is TT.NEWLINE:
            return self.block()

        right = self.expression()

        if self.token.type not in (TT.NEWLINE, TT.EOF):
            raise errors.NoLineTerminationError(self.token)

        self.advance()

        return right

    def colon(self):
        if self.token.type is not TT.COLON:
            raise errors.NoColonError(self.token)

        return self.take_token()

def is_normal(node):
    return isinstance(node, NODES.ASTNode) and not isinstance(node, NODES.EOFNode)
