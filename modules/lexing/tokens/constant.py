from lexing import errors
from .token import Token

class Constant(Token):
    @property
    def data(self):
        return self.value

    @classmethod
    @property
    def label(cls):
        return "C"

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
    def construct(cls, lexer):
        value = lexer.take(cls.symbols())
        is_int = "." not in value

        if value.count(".") > 1:
            raise errors.FloatError()

        return NumericalConstant(is_int, value)

    @classmethod
    def symbols(cls):
        return "0123456789."
