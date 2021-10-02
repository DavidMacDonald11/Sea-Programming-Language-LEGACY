from abc import ABC, abstractmethod

class Token(ABC):
    @property
    @abstractmethod
    def data(self):
        pass

    def __init__(self, position = None):
        self.position = position

    def __repr__(self):
        return f"{type(self).__name__}: {self.data}"

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
