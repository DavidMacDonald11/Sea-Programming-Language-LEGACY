from .memory import Memory

class MainMemory:
    def __init__(self):
        self.stack = [Memory()]
        self.heap = Memory()
