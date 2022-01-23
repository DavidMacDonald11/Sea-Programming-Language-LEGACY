from .constant.numerical_constant import NumericalConstant
from .punctuator.punctuator import Punctuator
from .punctuator.operator import Operator

TOKEN_TYPES = {
    NumericalConstant,
    Punctuator,
    Operator
}
