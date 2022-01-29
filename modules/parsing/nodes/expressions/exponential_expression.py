from lexing.tokens.operator import Op
from ..node import Node

class ExponentialExpressionNode(Node):
    @property
    def left(self):
        return self.components[0]

    @property
    def right(self):
        return self.components[2]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        left = f"{spacing}{down}{self.left.tree_repr(depth + 1)}"
        operator = f"{spacing}{down}{self.components[1]}"
        right = f"{spacing}{bottom}{self.right.tree_repr(depth + 1)}"

        return f"{self.node_name}{left}{operator}{right}"

    @classmethod
    def construct(cls, parser):
        def recursive_construct(expression = None, finished = False):
            if expression is None:
                return recursive_construct(parser.make.postfix_expression())

            if finished:
                return expression

            if not parser.token.matches_data(Op.POWER):
                return recursive_construct(expression, True)

            node = ExponentialExpressionNode(
                expression,
                parser.take(),
                parser.make.cast_expression()
            )

            return recursive_construct(node)

        return recursive_construct()

    def interpret(self):
        pass

    def transpile(self):
        pass
