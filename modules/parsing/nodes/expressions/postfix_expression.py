from lexing.tokens.operator import Op
from lexing.tokens.punctuator import Punc
from ..node import Node

# TODO add initializer lists?

class PostfixExpressionNode(Node):
    @property
    def expression(self):
        return self.components[0]

    def tree_repr(self, depth):
        spacing, _, bottom = self.tree_parts(depth)
        expression = f"{spacing}{bottom}{self.expression.tree_repr(depth + 1)}"
        return f"{self.node_name}{expression}"

    @classmethod
    def construct(cls, parser):
        def recursive_construct(expression = None, finished = False):
            if expression is None:
                return recursive_construct(parser.make.primary_expression())

            if finished:
                return expression

            parser.cache = expression

            node = PostfixIndexExpressionNode.construct(parser)
            node = node or PostfixCallExpressionNode.construct(parser)
            node = node or PostfixAccessExpressionNode.construct(parser)
            node = node or PostfixDeviationExpressionNode.construct(parser)

            condition = node is None
            return recursive_construct(expression if condition else node, condition)

        return recursive_construct()

    def interpret(self):
        pass

    def transpile(self):
        pass

class PostfixIndexExpressionNode(PostfixExpressionNode):
    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        lbrace = f"{spacing}{down}{self.components[1]}"
        expression = f"{spacing}{down}{self.expression.tree_repr(depth + 1)}"
        rbrace = f"{spacing}{bottom}{self.components[-1]}"

        return f"{self.node_name}{lbrace}{expression}{rbrace}"

    @classmethod
    def construct(cls, parser):
        if not parser.token.matches_data(Punc.LBRACK):
            return None

        return PostfixIndexExpressionNode(
            parser.cache,
            parser.take(),
            parser.make.expression(),
            parser.expecting(Punc.RBRACK)
        )

class PostfixCallExpressionNode(PostfixExpressionNode):
    @property
    def arguments(self):
        return self.components[2]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        identifier = f"{spacing}{down}{self.expression.tree_repr(depth + 1)}"
        lparen = f"{spacing}{down}{self.components[1]}"
        rparen = f"{spacing}{bottom}{self.components[-1]}"
        arguments = ""

        if self.arguments is not None:
            arguments = f"{spacing}{down}{self.arguments.tree_repr(depth + 1)}"

        return f"{self.node_name}{identifier}{lparen}{arguments}{rparen}"

    @classmethod
    def construct(cls, parser):
        if not parser.token.matches_data(Punc.LPAREN):
            return None

        lparen = parser.take()
        arguments = None

        if not parser.token.matches_data(Punc.RPAREN):
            arguments = parser.make.argument_expression_list()

        return PostfixCallExpressionNode(
            parser.cache,
            lparen,
            arguments,
            parser.expecting(Punc.RPAREN)
        )

class PostfixDeviationExpressionNode(PostfixExpressionNode):
    @property
    def operator(self):
        return self.components[1]

    def tree_repr(self, depth):
        spacing, _, bottom = self.tree_parts(depth)
        beginning = super().tree_repr(depth).replace("└", "├", 1)
        operator = f"{spacing}{bottom}{self.operator}"

        return f"{beginning}{operator}"

    @classmethod
    def construct(cls, parser):
        if not parser.token.matches_data(Op.INCREMENT, Op.DECREMENT):
            return None

        return PostfixDeviationExpressionNode(parser.cache, parser.take())

class PostfixAccessExpressionNode(PostfixDeviationExpressionNode):
    @property
    def identifier(self):
        return self.components[-1]

    def tree_repr(self, depth):
        spacing, _, bottom = self.tree_parts(depth)
        beginning = super().tree_repr(depth)[::-1].replace("└", "├", 1)[::-1]
        identifier = f"{spacing}{bottom}{self.identifier.tree_repr(depth + 1)}"

        return f"{beginning}{identifier}"

    @classmethod
    def construct(cls, parser):
        if not parser.token.matches_data(Op.ACCESS, Op.POINTER_ACCESS):
            return None

        return PostfixAccessExpressionNode(
            parser.cache,
            parser.take(),
            parser.make.identifier()
        )
