from parser import errors
from nodes.eof_node import EOFNode
from nodes.operations.sequential_node import SequentialOperationNode
from .makes import MAKES

class Parser:
    @property
    def token(self):
        return self.tokens[0]

    @property
    def position(self):
        position = self.tokens[0].position.copy()
        position.end = self.tokens[-1].position.end.copy()

        return position

    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.ast = None
        self.depth = 0
        self.i = 0

        self.advance()

    def advance(self, amount = 1):
        if amount < 1:
            return

        i = self.i
        self.i += amount

        self.tokens += self.lexer.tokens[i:self.i]

    def take(self, amount = 1):
        if amount < 1:
            return

        taken = self.tokens[:amount]
        self.tokens = self.tokens[amount:]

        if len(self.tokens) < 1:
            self.advance()

        return taken[0] if len(taken) == 1 else taken

    def expecting(self, *datas):
        self.advance(len(datas))
        tokens = []

        for data in datas:
            data_tuple = data if isinstance(data, (tuple, list)) else (data,)

            if self.token.data not in data_tuple:
                raise errors.ExpectedTokenError(data)

            tokens += [self.take()]

        return tokens[0] if len(tokens) == 1 else tokens

    def make_ast(self):
        def make_node():
            line = MAKES.line_node(self, MAKES)

            if isinstance(line, EOFNode):
                return line

            return SequentialOperationNode(line, make_node())

        self.ast = make_node()
