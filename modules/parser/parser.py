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
        taken = self.tokens[:amount]
        self.tokens = self.tokens[amount:]

        if len(self.tokens) < 1:
            self.advance()

        return taken[0] if len(taken) == 1 else taken

    def make_ast(self):
        pass
