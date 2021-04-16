from modules.visitor.visitor import Visitor

class Interpreter(Visitor):
    vocab_base = "Interpret"

    def __init__(self, output_stream):
        super().__init__(output_stream)
        self.symbol_table.interpret = True
