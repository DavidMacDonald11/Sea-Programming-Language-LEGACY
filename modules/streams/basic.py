from abc import ABC, abstractmethod

class InStream(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def read(self, amount = 1):
        pass

class OutStream(ABC):
    @abstractmethod
    def write(self, data):
        pass

class NullStream(InStream, OutStream):
    def __init__(self):
        super().__init__("null")

    def read(self, amount = 1):
        return ""

    def write(self, data):
        pass
