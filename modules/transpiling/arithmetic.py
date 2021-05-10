def pow_nums(x, y, memory):
    memory.headers.add("#include <math.h>")
    return f"powl({x}, {y})"
