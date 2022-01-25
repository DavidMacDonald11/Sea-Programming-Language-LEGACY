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
        return cls(parser.take()) if parser.token.matches(Identifier) else None

class ConstantNode(PrimaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches(Constant) else None

class StringLiteralNode(PrimaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        return cls(parser.take()) if parser.token.matches(StringLiteral) else None

class ParentheticalExpressionNode(PrimaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        try:
            parser.expecting(Punc.LPAREN)
        except errors.ExpectedTokenError as e:
            raise errors.PrimaryExpressionError(e.position, e.message) from e

        # TODO Replace with expression
        node = parser.make.primary_expression()
        parser.expecting(Punc.RPAREN)

        return node

PRIMARY_MAKES = {
    "primary_expression": PrimaryExpressionNode,
    "identifier": IdentifierNode,
    "constant": ConstantNode,
    "string_literal": StringLiteralNode,
    "parenthetical_expression": ParentheticalExpressionNode
}
