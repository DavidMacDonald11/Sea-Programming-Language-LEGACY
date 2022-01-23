from dataclasses import dataclass
from .general import InStream, OutStream, ErrorStream

@dataclass
class StreamHolder:
    in_stream: InStream = None
    out_stream: OutStream = None
    error_stream: ErrorStream = None
    debug_stream: OutStream = None
