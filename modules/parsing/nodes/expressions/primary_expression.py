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
    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches_type(Identifier) else None

class ConstantNode(PrimaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches_type(Constant) else None

class StringLiteralNode(PrimaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches_type(StringLiteral) else None

class ParentheticalExpressionNode(PrimaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        try:
            left = parser.expecting(Punc.LPAREN)
        except errors.ExpectedTokenError as e:
            raise errors.PrimaryExpressionError(e.position, e.message) from e

        expression = parser.make.expression()
        right = parser.expecting(Punc.RPAREN)

        return ParentheticalExpressionNode(left, expression, right)

# TODO delete expression declaration

PRIMARY_MAKES = {
    "expression": PrimaryExpressionNode,
    "primary_expression": PrimaryExpressionNode,
    "identifier": IdentifierNode,
    "constant": ConstantNode,
    "string_literal": StringLiteralNode,
    "parenthetical_expression": ParentheticalExpressionNode
}
