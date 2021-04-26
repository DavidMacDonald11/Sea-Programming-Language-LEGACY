from dataclasses import dataclass
from .basic import InStream, OutStream

@dataclass
class StreamHolder:
    in_stream: InStream
    out_stream: OutStream
    error_stream: OutStream
    debug_stream: OutStream
