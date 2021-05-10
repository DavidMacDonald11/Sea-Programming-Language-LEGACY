def stack(memory):
    class Stack:
        def __enter__(self):
            return memory.add_stack()

        def __exit__(self, e_type, *_):
            if e_type is None:
                return memory.remove_stack()

            return False

    return Stack()
