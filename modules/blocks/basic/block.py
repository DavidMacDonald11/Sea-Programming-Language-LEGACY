import re
from abc import ABCMeta, abstractmethod
from modules.transpiler import statements
from modules.transpiler.errors import TranspilerError

class MetaBlock(ABCMeta):
    @property
    def declaration_pattern(cls):
        if cls._declaration_pattern is None:
            defined = cls.get_declaration_pattern()

            if defined is None:
                raise UndefinedBlockPropertyError("Declaration Pattern", cls)

            cls._declaration_pattern = re.compile(defined)

        return cls._declaration_pattern

class Block(metaclass = MetaBlock):
    _declaration_pattern = None

    def __init__(self, indent, declaration):
        self.indent = indent
        self.declaration = declaration
        self.is_empty = True

    def open(self, cfile, outside = True):
        self.write_line(cfile, self.get_declaration(), outside)

    def close(self, cfile, outside = True):
        cls = type(self)

        if self.is_empty:
            raise EmptyBlockError(cls)

        self.write_line(cfile, self.get_ending(), outside)

    def indent_line(self, line = "", outside = False):
        return " " * 4 * (self.indent - int(outside)) + line

    def write_line(self, cfile, line = "", outside = False):
        if line is not None:
            if not outside:
                line = statements.transpile(line)

            cfile.write(f"{self.indent_line(line, outside)}\n")

    def is_type(self, block_type):
        return isinstance(self, block_type)

    @abstractmethod
    def get_declaration(self):
        pass

    @abstractmethod
    def get_ending(self):
        pass

    @classmethod
    @abstractmethod
    def check_match(cls, line):
        pass

    @classmethod
    def get_declaration_pattern(cls):
        return None

    @classmethod
    def matches_pattern(cls, pattern, line):
        return pattern.fullmatch(line) is not None

    @classmethod
    def sub_pattern(cls, pattern, sub, line):
        return pattern.sub(sub, line)

class BlockError(TranspilerError):
    def __init__(self, block_type = Block):
        self.block_type = block_type
        self.block_name = block_type.__name__

        super().__init__()

    def get_message(self):
        return f"{self.block_name} had an error."

class EmptyBlockError(BlockError):
    def get_message(self):
        return f"{self.block_name} cannot be empty. Use pass to declare empty block."

class BlockDeclarationError(BlockError):
    def get_message(self):
        return f"{self.block_name} was declared incorrectly."

class BlockClassDeclarationError(BlockDeclarationError):
    def get_message(self):
        return f"The {self.block_name} class was set up incorrectly."

class UndefinedBlockPropertyError(BlockClassDeclarationError):
    def __init__(self, property_name, block_type = Block):
        self.property_name = property_name

        super().__init__(block_type)

    def get_message(self):
        return f"{self.block_name} does not define the {self.property_name} property."

class UndeclaredBlockError(BlockDeclarationError):
    def get_message(self):
        return "Too many indents for the current block."
