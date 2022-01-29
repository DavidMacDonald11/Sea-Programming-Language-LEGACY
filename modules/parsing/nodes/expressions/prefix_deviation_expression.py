from lexing.tokens.operator import Op
from .unary_expression import UnaryExpressionNode

class PrefixDeviationExpressionNode(UnaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        if parser.token.matches_data(Op.INCREMENT, Op.DECREMENT):
            return PrefixDeviationExpressionNode(
                parser.take(),
                parser.make.prefix_deviation_expression()
            )

        return parser.make.postfix_expression()
