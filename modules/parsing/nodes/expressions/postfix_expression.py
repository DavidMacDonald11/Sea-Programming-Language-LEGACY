from lexing.tokens.operator import Op
from lexing.tokens.punctuator import Punc
from ..node import Node

class PostfixExpressionNode(Node):
    @classmethod
    def construct(cls, parser):
        def recursive_construct(expression = None, finished = False):
            if expression is None:
                return recursive_construct(parser.make.primary_expression())

            if finished:
                return expression

            if parser.token.matches_data(Punc.LBRACK):
                node = PostfixExpressionNode(
                    expression,
                    parser.take(),
                    parser.make.expression(),
                    parser.expecting(Punc.RBRACK)
                )

                return recursive_construct(node)

            if parser.token.matches_data(Punc.LPAREN):
                node = PostfixExpressionNode(
                    expression,
                    parser.take(),
                    # TODO make argument expression list
                    parser.expecting(Punc.RPAREN)
                )

                return recursive_construct(node)

            if parser.token.matches_data(Op.ACCESS, Op.POINTER_ACCESS):
                node = PostfixExpressionNode(
                    expression,
                    parser.take(),
                    parser.make.identifier()
                )

                return recursive_construct(node)

            if parser.token.matches_data(Op.INCREMENT, Op.DECREMENT):
                node = PostfixExpressionNode(expression, parser.take())
                return recursive_construct(node)

            return recursive_construct(expression, True)

        return recursive_construct()

    def interpret(self):
        pass

    def transpile(self):
        pass
