from ..token import Token

class Constant(Token):
    def __init__(self, value, position = None):
        self.value = value
        super().__init__(position)
