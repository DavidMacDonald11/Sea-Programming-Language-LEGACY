# Indentation
Similar to Python, Sea uses indentation rather than brackets to determine block. Indents must be made up of 4 spaces or 1 tab. Empty lines are ignored, but it is highly reccomended to use empty lines in a manner sufficient to create readable code.

# Basic Block
In C, you have the ability to create a block in order to separate variables, organize code, etc. Most blocks must have at least one line, so use the keyword `pass` to allow for an empty block for testing purposes.

### C
```c
{

}
```

### Sea
```sea
block:
    pass
```

# C Block
There will be times when you'd rather right something directly in C. Just use a C Block. If you want to use C inline, see [Inline C](./TO_BE_ADDED.md).

### C
```c
// C Block:
#include <stdio.h>

int main()
{
    printf("Hello World!");
    return 0;
}
```

### Sea
```sea
c block:
    #include <stdio.h>

    int main()
    {
        printf("Hello World!");
        return 0;
    }
```

Notes:
- Relative leading spaces are preserved.
- Empty lines are preserved.
- A c block does not create a new block in the final c code.
