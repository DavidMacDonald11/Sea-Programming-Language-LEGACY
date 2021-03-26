import re
from abc import abstractmethod
from .block import Block
from .block import MetaBlock
from .block import UndeclaredBlockError

class MetaEndableBlock(MetaBlock):
    @property
    def ending_pattern(cls):
        if cls._ending_pattern is None:
            cls._ending_pattern = re.compile(cls.get_ending_pattern())

        return cls._ending_pattern

class EndableBlock(Block, metaclass = MetaEndableBlock):
    """A block that has a defined Sea ending."""
    _ending_pattern = None

    def __init__(self, indent, declaration):
        self.ending = None
        super().__init__(indent, declaration)

    def get_ending(self):
        if self.ending is None:
            raise UndeclaredEndOfBlockError()

        return self.ending

    def close(self, cfile, outside = True):
        super().close(cfile, outside)
        cfile.write("\n")

    @classmethod
    def check_ending(cls, line):
        return cls.matches_pattern(cls.ending_pattern, line)

    @classmethod
    def remove_ending(cls, line):
        return cls.sub_pattern(cls.ending_pattern, "", line)

    @classmethod
    @abstractmethod
    def get_ending_pattern(cls):
        pass

class UndeclaredEndOfBlockError(UndeclaredBlockError):
    def get_message(self):
        return f"{self.block_name} ended without required end declaration."
