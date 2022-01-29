from parsing import errors
from lexing.tokens.punctuator import Punc
from lexing.tokens.constant import Constant
from lexing.tokens.identifier import Identifier
from lexing.tokens.string_literal import StringLiteral
from ..node import Node

class PrimaryExpressionNode(Node):
    @classmethod
    def construct(cls, parser):
        node = parser.make.identifier()
        node = node or parser.make.constant()
        node = node or parser.make.string_literal()

        return node or parser.make.parenthetical_expression()

    def interpret(self):
        pass

    def transpile(self):
        pass

class IdentifierNode(PrimaryExpressionNode):
    @property
    def identifier(self):
        return self.components[0]

    def tree_repr(self, depth = 1):
        return f"{self.node_name}({self.identifier})"

    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches_type(Identifier) else None

class ConstantNode(PrimaryExpressionNode):
    @property
    def constant(self):
        return self.components[0]

    def tree_repr(self, depth):
        return f"{self.node_name}({self.constant})"

    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches_type(Constant) else None

class StringLiteralNode(PrimaryExpressionNode):
    @property
    def string_literal(self):
        return self.components[0]

    def tree_repr(self, depth):
        return f"{self.node_name}({self.string_literal})"

    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches_type(StringLiteral) else None

class ParentheticalExpressionNode(PrimaryExpressionNode):
    @property
    def expression(self):
        return self.components[1]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        expression = f"{spacing}{bottom}{self.expression.tree_repr(depth + 1)}"
        return f"{self.node_name}{expression}"

    @classmethod
    def construct(cls, parser):
        try:
            left = parser.expecting(Punc.LPAREN)
        except errors.ExpectedTokenError as e:
            raise errors.PrimaryExpressionError(e.position, e.message) from e

        expression = parser.make.expression()
        right = parser.expecting(Punc.RPAREN)

        return ParentheticalExpressionNode(left, expression, right)

PRIMARY_MAKES = {
    "primary_expression": PrimaryExpressionNode,
    "identifier": IdentifierNode,
    "constant": ConstantNode,
    "string_literal": StringLiteralNode,
    "parenthetical_expression": ParentheticalExpressionNode
}
