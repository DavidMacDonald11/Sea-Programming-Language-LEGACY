from abc import ABCMeta, abstractmethod
from functools import cache
from modules.transpiler.errors import TranspilerError

class MetaStatement(ABCMeta):
    @property
    def complexity(cls):
        if len(cls.allowed_nested) == 0:
            return 0

        return max(nested.complexity for nested in nested_set for nested_set in cls.allowed_nested)

    @property
    @cache
    def pattern(cls):
        defined = cls.get_pattern()

        if defined is None:
            raise UndefinedStatementPropertyError("Pattern", cls)

        return defined

class Statement(metaclass = MetaStatement):
    allowed_nested = []

    def __init__(self, line):
        self.line = line
        self.statements = []

    def get_line(self):
        cls = type(self)
        structure = cls.get_structure()

        if len(self.statements) != len(structure.count(None)):
            raise NestedStatementCountError(cls)

        lines = (statement.get_line() for statement in self.statements)

        return "".join(next(lines) if part is None else part for part in structure )

    @classmethod
    @abstractmethod
    def get_structure(cls):
        pass

    def strip_structure(self):
        return type(self).pattern.sub(" ", self.line, 1)

    @classmethod
    def check_match(cls, line):
        return cls.matches_pattern(line)

    @classmethod
    def get_pattern(cls):
        return None

    @classmethod
    def matches_pattern(cls, line):
        return len(cls.pattern.match(line)) != 0

    @classmethod
    def sub_pattern(cls, sub, line, count = 0):
        return cls.pattern.sub(sub, line, count)

class StatementError(TranspilerError):
    def __init__(self, statement_type = Statement):
        self.statement_type = statement_type
        self.statement_name = statement_type.__name__

        super().__init__()

    def get_message(self):
        return f"{self.statement_name} had an error."

class StatementDeclarationError(StatementError):
    def get_message(self):
        return f"{self.statement_name} was declared incorrectly."

class StatementClassDeclarationError(StatementDeclarationError):
    def get_message(self):
        return f"The {self.statement_name} class was set up incorrectly."

class UndefinedStatementPropertyError(StatementClassDeclarationError):
    def __init__(self, property_name, statement_type = Statement):
        self.property_name = property_name

        super().__init__(statement_type)

    def get_message(self):
        return f"{self.statement_name} does not define the {self.property_name} property."

class NestedStatementCountError(StatementDeclarationError):
    def get_message(self):
        return f"{self.statement_name} has too many or too few nested statements."

class UnkownStatementError(StatementDeclarationError):
    def get_message(self):
        return "Statement is unknown."
