from lexing.tokens.operator import Op
from lexing.tokens.punctuator import Punc
from ..node import Node

# TODO add initializer lists?

class PostfixExpressionNode(Node):
    @property
    def expression(self):
        return self.components[0]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        expression = f"{spacing}{bottom}{self.expression.tree_repr(depth + 1)}"
        return f"{self.node_name}{expression}"

    @classmethod
    def construct(cls, parser):
        def recursive_construct(expression = None, finished = False):
            if expression is None:
                return recursive_construct(parser.make.primary_expression())

            if finished:
                return expression

            if parser.token.matches_data(Punc.LBRACK):
                node = PostfixIndexExpressionNode(
                    expression,
                    parser.take(),
                    parser.make.expression(),
                    parser.expecting(Punc.RBRACK)
                )

                return recursive_construct(node)

            if parser.token.matches_data(Punc.LPAREN):
                lparen = parser.take()
                arguments = None

                if not parser.token.matches_data(Punc.RPAREN):
                    arguments = parser.make.argument_expression_list()

                node = PostfixCallExpressionNode(
                    expression,
                    lparen,
                    arguments,
                    parser.expecting(Punc.RPAREN)
                )

                return recursive_construct(node)

            if parser.token.matches_data(Op.ACCESS, Op.POINTER_ACCESS):
                node = PostfixAccessExpressionNode(
                    expression,
                    parser.take(),
                    parser.make.identifier()
                )

                return recursive_construct(node)

            if parser.token.matches_data(Op.INCREMENT, Op.DECREMENT):
                node = PostfixDeviationExpressionNode(expression, parser.take())
                return recursive_construct(node)

            return recursive_construct(expression, True)

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
        raise NotImplementedError()

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
        raise NotImplementedError()

class PostfixDeviationExpressionNode(PostfixExpressionNode):
    @property
    def operator(self):
        return self.components[1]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        beginning = super().tree_repr(depth).replace("└", "├", 1)
        operator = f"{spacing}{bottom}{self.operator}"

        return f"{beginning}{operator}"

    @classmethod
    def construct(cls, parser):
        raise NotImplementedError()

class PostfixAccessExpressionNode(PostfixDeviationExpressionNode):
    @property
    def identifier(self):
        return self.components[-1]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        beginning = super().tree_repr(depth)[::-1].replace("└", "├", 1)[::-1]
        identifier = f"{spacing}{bottom}{self.identifier.tree_repr(depth + 1)}"

        return f"{beginning}{identifier}"
