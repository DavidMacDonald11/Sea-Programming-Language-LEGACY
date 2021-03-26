from modules.blocks import collection
from modules.blocks.basic.verbatum_block import VerbatumBlock
from modules.blocks.basic.endable_block import EndableBlock
from modules.blocks.basic.endable_block import UndeclaredEndOfBlockError
from modules.blocks.basic.block import UndeclaredBlockError
from modules.parser.indentation import count_indent
from .block_state import BlockState

class Continue(Exception):
    pass

def interpret_line(line):
    BlockState.line = line

    check_space()
    check_space()
    check_block_end()
    check_verbatum_line()
    check_undeclared_block_start()
    check_previous_block_end()
    check_block_start()

def check_space():
    if BlockState.line.isspace() or BlockState.line == "":
        if BlockState.is_type(VerbatumBlock):
            BlockState.write_line()

        raise Continue()

    BlockState.line = BlockState.line.rstrip()

def check_block_end():
    BlockState.new_indent = count_indent(BlockState.line)

    if BlockState.is_type(EndableBlock) and BlockState.check_ending():
        if BlockState.new_indent < BlockState.indent - 1:
            raise UndeclaredEndOfBlockError()

        BlockState.close(1)
        raise Continue()

def check_verbatum_line():
    if BlockState.is_type(VerbatumBlock) and BlockState.new_indent >= BlockState.indent:
        BlockState.has_line()
        BlockState.write_line()
        raise Continue()

def check_undeclared_block_start():
    if not BlockState.is_type(VerbatumBlock) and BlockState.new_indent > BlockState.indent:
        raise UndeclaredBlockError()

def check_previous_block_end():
    if BlockState.new_indent < BlockState.indent:
        indent_difference = BlockState.indent - BlockState.new_indent

        for i in range(indent_difference):
            prev_block = BlockState.blocks[-1 - i]

            if prev_block.is_type(EndableBlock) and prev_block.check_ending(BlockState.line):
                prev_block.ending = BlockState.line
                BlockState.line = prev_block.remove_ending(BlockState.line)

        BlockState.close(indent_difference)

    BlockState.line = BlockState.line.strip()

    if BlockState.line == "":
        raise Continue()

def check_block_start():
    if BlockState.new_indent == BlockState.indent:
        BlockState.has_line()
        block_type = collection.check_match_all(BlockState.line)

        if block_type is None:
            BlockState.write_line()
        else:
            BlockState.open(block_type)

        raise Continue()
