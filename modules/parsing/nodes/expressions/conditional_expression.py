from ..node import Node

class ConditionalExpressionNode(Node):
    @property
    def left(self):
        return self.components[0]

    @property
    def condition(self):
        return self.components[2]

    @property
    def right(self):
        return self.components[4]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        left = f"{spacing}{down}{self.left.tree_repr(depth + 1)}"
        if_token = f"{spacing}{down}{self.components[1]}"
        condition = f"{spacing}{down}{self.condition.tree_repr(depth + 1)}"
        else_token = f"{spacing}{down}{self.components[3]}"
        right = f"{spacing}{bottom}{self.right.tree_repr(depth + 1)}"

        return f"{self.node_name}{left}{if_token}{condition}{else_token}{right}"

    @classmethod
    def construct(cls, parser):
        def recursive_construct(expression = None, finished = False):
            if expression is None:
                return recursive_construct(parser.make.logical_or_expression())

            if finished:
                return expression

            if not parser.token.matches_data("if"):
                return recursive_construct(expression, True)

            node = ConditionalExpressionNode(
                expression,
                parser.take(),
                parser.make.expression(),
                parser.expecting("else"),
                parser.make.conditional_expression()
            )

            return recursive_construct(node)

        return recursive_construct()

    def interpret(self):
        pass

    def transpile(self):
        pass
