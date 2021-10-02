from abc import ABC, abstractmethod

class InStream(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def read_symbol(self):
        pass

class OutStream(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def write(self, data):
        pass

class ErrorStream(OutStream):
    def write(self, data):
        to_print = f"{type(data).__name__}: {data.get_message()}\n"
        self.write_error(data, to_print)

    @abstractmethod
    def write_error(self, error, data):
        pass

class NullStream(InStream, ErrorStream):
    def __init__(self):
        super().__init__("null")

    def read_symbol(self):
        return ""

    def write(self, data):
        pass

    def write_error(self, error, data):
        pass
