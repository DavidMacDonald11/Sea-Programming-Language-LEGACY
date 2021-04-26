from abc import ABC, abstractmethod
from errors import errors

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

class ErrorStream(OutStream):
    def __init__(self, name, output_warnings = True):
        self.output_warnings = output_warnings
        super().__init__(self, name)

    def write(self, data):
        if not self.output_warnings and isinstance(data, errors.SeaWarning):
            return

        to_print = f"{type(data).__name__} at {data.position}: {data.get_message()}\n"
        self.write_error(data, to_print)

    @abstractmethod
    def write_error(self, error, data):
        pass

class NullStream(InStream, OutStream):
    def __init__(self):
        super().__init__("null")

    def read(self, amount = 1):
        return ""

    def write(self, data):
        pass
