from .unary_expression import UnaryExpressionNode

class LogicalNotExpressionNode(UnaryExpressionNode):
    @classmethod
    def construct(cls, parser):
        if parser.token.matches_data("not"):
            return LogicalNotExpressionNode(parser.take(), parser.make.logical_not_expression())

        return parser.make.comparison_expression()
