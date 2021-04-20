# Boolean Operators

Sea includes the familiar boolean operators:

### C
```c
// AND
&&

// OR
||

// NOT
!
```

### Sea
```sea
// AND
and

// OR
or

// NOT
not
```

Sea also includes the `xor` operator such that `x xor y` is defined as `(x or y) and not (x and y)`.

The order of priority goes from `not` to `and` to `xor` to `or`.

In Sea, `true` is a constant of value 1 and `false` is a constant of value 0. Non-zero values are true and zero values are false.
