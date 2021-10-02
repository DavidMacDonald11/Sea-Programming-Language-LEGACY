from .token import Token

class Constant(Token):
    def __init__(self, value, position = None):
        self.value = value
        super().__init__(position)

class NumericalConstant(Constant):
    @property
    def data(self):
        data_type = "int" if self.is_int else "float"
        return (data_type, self.value)

    def __init__(self, is_int, value, position = None):
        self.is_int = is_int
        super().__init__(value, position)

    @classmethod
    def symbols(cls):
        return "0123456789."
