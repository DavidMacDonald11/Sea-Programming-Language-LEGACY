# Comments
Comments in Sea are basically identical to comments in C.

### C
```c
// Single line comments

/*
    Multi
    Line
    Comment
*/
```

### Sea
```sea
// Single line comments

/*
    Multi
    Line
    Comment
*/
```

As of right now, however, the following are not allowed:

### Sea
```sea
... // Comment starting after statement

.../* Multiline comment starting after statement
*/

/* Multiline comment in one line */

/* Multiline comment with statement after
*/ ...
```
