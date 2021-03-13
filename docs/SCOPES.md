# Indentation
Similar to Python, Sea uses indentation rather than brackets to determine scope. Indents must be made up of 4 spaces or 1 tab. Empty lines are ignored, but it is highly reccomended to use empty lines in a manner sufficient to create readable code.

# Basic Scope
In C, you have the ability to create a scope in order to separate variables, organize code, etc. All scopes must have at least one line, so use the keyword `pass` to allow for an empty scope for testing purposes.

### C
```c
{

}
```

### Sea
```sea
scope:
    pass
```

# C Scope
There will be times when you'd rather right something directly in C. Just use a C Scope. If you want to use C inline, see [Inline C](TO_BE_ADDED).

### C
```c
// C Scope:
#include <stdio.h>

int main()
{
    printf("Hello World!");
    return 0;
}
```

### Sea
```sea
c scope:
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
- A c scope does not create a new scope in the final c code.