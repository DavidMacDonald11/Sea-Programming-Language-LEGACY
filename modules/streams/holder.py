from dataclasses import dataclass
from .basic import InStream, OutStream, ErrorStream

@dataclass
class StreamHolder:
    in_stream: InStream
    out_stream: OutStream
    error_stream: ErrorStream
    debug_stream: OutStream
