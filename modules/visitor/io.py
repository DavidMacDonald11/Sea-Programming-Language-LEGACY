from abc import ABC
from abc import abstractmethod

class IO:
    def __init__(self, input_stream, output_stream, error_stream):
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.error_stream = error_stream

class Input(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def read(self):
        pass

class Output(ABC):
    @abstractmethod
    def write(self, string):
        pass

class File:
    def __init__(self, file):
        self.file = file

class FileInput(File, Input):
    @property
    def name(self):
        return self.file.name

    def read(self):
        return self.file.read(1)

class FileOutput(File, Output):
    def write(self, string):
        self.file.write(string)

class NullOutput(Output):
    def write(self, string):
        pass
