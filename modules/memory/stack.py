from types import SimpleNamespace

def stack(memory):
    def __enter__():
        return memory.add_stack()

    def __exit__(e_type, *_):
        if e_type is None:
            return memory.remove_stack()

        return False

    return SimpleNamespace(
        __enter__ = __enter__,
        __exit__ = __exit__
    )
