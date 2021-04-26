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
    def allowed(cls):
        pass

    def matches(self, what, data):
        return isinstance(self, what) and self.data == data
