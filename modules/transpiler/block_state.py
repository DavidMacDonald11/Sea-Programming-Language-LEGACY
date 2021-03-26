from modules.blocks.global_block import GlobalBlock
from .errors import TranspilerError

class MetaBlockState(type):
    @property
    def blocks(cls):
        return cls._blocks

    @blocks.setter
    def blocks(cls, value):
        cls._blocks = value

    @property
    def cfile(cls):
        if cls._cfile is None:
            raise UndefinedCFileError()

        return cls._cfile

    @cfile.setter
    def cfile(cls, value):
        cls._cfile = value

    @property
    def new_indent(cls):
        return cls._new_indent

    @new_indent.setter
    def new_indent(cls, value):
        cls._new_indent = value

    @property
    def line(cls):
        return cls._line

    @line.setter
    def line(cls, value):
        cls._line = value

    @property
    def block(cls):
        return cls._blocks[-1]

    @property
    def indent(cls):
        return cls._blocks[-1].indent

class UndefinedCFileError(TranspilerError):
    def get_message(self):
        return "The Block State class must have a cfile to write to."

class BlockState(metaclass = MetaBlockState):
    """Keeps track of the current block state during transpilation."""
    _blocks = [GlobalBlock()]
    _cfile = None
    _new_indent = -1
    _line = ""

    @classmethod
    def open(cls, block_type):
        block = block_type(cls.indent + 1, cls.line)
        block.open(cls.cfile)

        cls.blocks += [block]

    @classmethod
    def close(cls, amount):
        for _ in range(amount):
            cls.block.close(cls.cfile)
            cls.blocks = cls.blocks[:-1]

    @classmethod
    def close_all(cls):
        for block in cls.blocks[::-1]:
            block.close(cls.cfile)

    @classmethod
    def restart(cls, cfile):
        cls.blocks = [GlobalBlock()]
        cls.cfile = cfile
        cls.new_indent = -1
        cls.line = ""

    @classmethod
    def is_type(cls, block_type):
        return cls.block.is_type(block_type)

    @classmethod
    def write_line(cls):
        cls.block.write_line(cls.cfile, cls.line)

    @classmethod
    def has_line(cls):
        cls.block.is_empty = False

    @classmethod
    def check_ending(cls):
        is_ending = cls.block.check_ending(cls.line)

        if is_ending:
            cls.block.ending = cls.line

        return is_ending
