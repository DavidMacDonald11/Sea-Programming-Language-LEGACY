from .token import Token
from .. import errors

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
    def construct(cls, lexer):
        value = lexer.take_token_string(cls.symbols())
        is_int = "." not in value

        if value.count(".") > 1:
            raise errors.FloatError()

        return NumericalConstant(is_int, value)

    @classmethod
    def symbols(cls):
        return "0123456789."
