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

    def matches_type(self, what):
        return isinstance(self, what)

    def matches_data(self, *datas):
        return len(datas) == 0 or self.data in datas

    def matches(self, what, *datas):
        return self.matches_type(what) and self.matches_data(*datas)
