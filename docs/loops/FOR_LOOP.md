# For Loops
For loops are mostly the same as in C. Unecessary parenthesis are removed and brackets are replaced with a colon and indentation:

### C
```c
for(int i = 0; i < 10; ++i) {
    ...
}
```

### Sea
```sea
for int i = 0; i < 10; ++i:
    ...
```

Similar to C, certain aspects of the for loop can be left blank:

### C
```c
for(;true;) {
    ...
}
```

### Sea
```sea
for ;true;:
    ...
```

Sea also includes a foreach loop syntax:
### C
```c
int* arr = {1, 2, 3}

for(int *p = arr; p - arr < sizeof(arr) / sizeof(*arr); ++p) {
    ...
}

```

### Sea
```sea
int* arr = {1, 2, 3}

for p in arr:
    ...

```

The type of the variable, in this case `p`, is defined as a pointer to `typeof(*arr)`.
