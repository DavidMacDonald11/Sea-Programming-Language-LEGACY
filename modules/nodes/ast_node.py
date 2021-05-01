from abc import ABC, abstractmethod

class ASTNode(ABC):
    def __init__(self, position):
        self.position = position
