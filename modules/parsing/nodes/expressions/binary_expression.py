from abc import abstractmethod
from ..node import Node

class BinaryExpressionNode(Node):
    @property
    def left(self):
        return self.components[0]

    @property
    def operator(self):
        return self.components[1]

    @property
    def right(self):
        return self.components[2]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        left = f"{spacing}{down}{self.left.tree_repr(depth + 1)}"
        operator = f"{spacing}{down}{self.operator}"
        right = f"{spacing}{bottom}{self.right.tree_repr(depth + 1)}"

        return f"{self.node_name}{left}{operator}{right}"

    @classmethod
    @abstractmethod
    def construct_info(cls, parser):
        pass

    @classmethod
    def construct(cls, parser):
        left, operators, right = cls.construct_info(parser)

        def recursive_construct(expression = None, finished = False):
            if expression is None:
                return recursive_construct(left())

            if finished:
                return expression

            if not parser.token.matches_data(*operators):
                return recursive_construct(expression, True)

            node = cls(
                expression,
                parser.take(),
                right()
            )

            return recursive_construct(node)

        return recursive_construct()
