from lexing.tokens.punctuator import Punc
from ..node import Node

class ArgumentExpressionListNode(Node):
    @property
    def left(self):
        return self.components[0]

    @property
    def right(self):
        return self.components[2]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        left = f"{spacing}{down}{self.left.tree_repr(depth + 1)}"
        comma = f"{spacing}{down}{self.components[1]}"
        right = f"{spacing}{bottom}{self.right.tree_repr(depth + 1)}"

        return f"{self.node_name}{left}{comma}{right}"

    @classmethod
    def construct(cls, parser):
        def recursive_construct(expression = None, finished = False):
            if expression is None:
                return recursive_construct(parser.make.assignment_expression())

            if finished:
                return expression

            if not parser.token.matches_data(Punc.COMMA):
                return recursive_construct(expression, True)

            node = ArgumentExpressionListNode(
                expression,
                parser.take(),
                parser.make.assignment_expression()
            )

            return recursive_construct(node)

        return recursive_construct()

    def interpret(self):
        pass

    def transpile(self):
        pass
