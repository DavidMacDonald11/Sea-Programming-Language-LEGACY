from .c_block import CBlock
from .function_block import FunctionBlock
from .multiline_comment import MultilineComment
from .nameless_block import NamelessBlock
from .loops.do_while_loop import DoWhileLoop
from .loops.while_loop import WhileLoop
from .loops.for_loop import ForLoop

BLOCKS = {NamelessBlock, CBlock, FunctionBlock, MultilineComment}
LOOPS = {DoWhileLoop, WhileLoop, ForLoop}
ALL_BLOCKS = BLOCKS | LOOPS

def check_match_all(line):
    for block_type in ALL_BLOCKS:
        if block_type.check_match(line):
            return block_type

    return None
