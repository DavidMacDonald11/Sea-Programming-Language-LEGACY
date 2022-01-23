from abc import ABC, abstractmethod

class Token(ABC):
    @property
    @abstractmethod
    def data(self):
        pass

    @classmethod
    @property
    def label(cls):
        return cls.__name__[0]

    def __init__(self, position = None):
        self.position = position

    def __repr__(self):
        return f"{type(self).label}{{{self.data}}}"

    @classmethod
    @abstractmethod
    def construct(cls, lexer):
        pass

    @classmethod
    @abstractmethod
    def symbols(cls):
        pass

    def matches(self, what, *datas):
        is_what = isinstance(self, what)

        if len(datas) == 0:
            return is_what

        return is_what and self.data in datas
