# Grammar
As Sea is based on C and Python, most of Sea's grammar is based directly on C.
Specifically, I utilized [Microsoft's C Language Syntax Summary](https://docs.microsoft.com/en-us/cpp/c-language/c-language-syntax-summary?view=msvc-170) to construct this document.

## Tokens

<pre><i>token:
    keyword
    identifier
    constant
    string-literal
    operator
    punctuator
</i></pre>

## Expressions

<pre><i>primary-expression:
    identifier
    constant
    string-literal
    </i><b>(</b><i> expression </i><b>)</b><i>
</i></pre>

<pre><i>postfix-expression:
    primary-expression
    postfix-expression </i><b>[</b><i> expression </i><b>]</b><i>
    postfix-expression </i><b>(</b><i> <u>argument-expression-list</u> </i><b>)</b><i>
    postfix-expression </i><b>.</b><i> identifier
    postfix-expression </i><b>-></b><i> identifier
    postfix-expression </i><b>++</b><i>
    postfix-expression </i><b>--</b><i>
</i></pre>

<pre><i>argument-expression-list:
    assignment-expression
    argument-expression-list </i><b>,</b><i> assignment-expression
</i></pre>

<pre><i>prefix-deviation-expression:
    postfix-expression
    </i><b>++</b><i> prefix-deviation-expression
    </i><b>--</b><i> prefix-deviation-expression
</i></pre>

<pre><i>exponential-expression:
    prefix-deviation-expression
    prefix-deviation-expression </i><b>**</b><i> cast-expression
</i></pre>

<pre><i>unary-expression:
    exponential-expression
    unary-operator cast-expression
    </i><b>size of</b><i> unary-expression
</i></pre>

<pre><i>unary-operator:</i> one of<b>
&  *  +  -  ~
</b></pre>

<pre><i>cast-expression:
    unary-expression
    type-name </i><b>(</b><i> cast-expression </i><b>)</b><i>
</i></pre>

<pre><i>multiplicative-expression:
    cast-expression
    multiplicative-expression </i><b>*</b><i> cast-expression
    multiplicative-expression </i><b>/</b><i> cast-expression
    multiplicative-expression </i><b>%</b><i> cast-expression
</i></pre>

<pre><i>additive-expression:
    multiplicative-expression
    additive-expression </i><b>+</b><i> multiplicative-expression
    additive-expression </i><b>-</b><i> multiplicative-expression
</i></pre>

<pre><i>shift-expression:
    additive-expression
    shift-expression</i><b> << </b><i>additive-expression
    shift-expression</i><b> >> </b><i>additive-expression
</i></pre>

<pre><i>bitwise-and-expression:
    shift-expression
    bitwise-and-expression </i><b>&</b><i> shift-expression
</i></pre>

<pre><i>bitwise-xor-expression:
    bitwise-and-expression
    bitwise-xor-expression </i><b>^</b><i> bitwise-and-expression
</i></pre>

<pre><i>bitwise-or-expression:
    bitwise-xor-expression
    bitwise-or-expression </i><b>|</b><i> bitwise-xor-expression
</i></pre>

<pre><i>comparative-expression:
    bitwise-or-expression
    comparative-expression comparative-opertor bitwise-or-expression
</i></pre>

<pre><i>comparative-operator:</i> one of<b>
<  >  <=  >=  ==  !=
</b></pre>

<pre><i>logical-not-expression:
    comparative-expression
    </i><b>not</b><i> logical-not-expression
</i></pre>

<pre><i>logical-and-expression:
    logical-not-expression
    logical-and-expression </i><b>and</b><i> logical-not-expression
</i></pre>

<pre><i>logical-or-expression:
    logical-and-expression
    logical-or-expression </i><b>or</b><i> logical-and-expression
</i></pre>

<pre><i>conditional-expression:
    logical-or-expression
    logical-or-expression </i><b>if</b><i> expression </i><b>else</b><i> conditional-expression
</i></pre>

<pre><i>assignment-expression:
    conditional-expression
    conditional-expression assignment-operator assignment-expression
</i></pre>

<pre><i>assignment-operator:</i> one of<b>
=  +=  -=  *=  /=  %=  **=  <<=  >>=  &=  ^=  |=
</b></pre>

<pre><i>expression:
    assignment-expression
    expression </i><b>,</b><i> assignment-expression
</i></pre>

<pre><i>constant-expression:
    conditional-expression
</i></pre>

## Declarations

<pre><i>declaration:
    declaration-specifiers <u>init-declarator-list</u>
</i></pre>

<pre><i>declaration-specifiers:
    storage-class-specifier <u>declaration-specifiers</u>
    type-specifier <u>declaration-specifiers</u>
    type-qualifier <u>declaration-specifiers</u>
    function-specifier <u>declaration-specifiers</u>
    alignment-specifier <u>declaration-specifiers</u>
</i></pre>

<pre><i>init-declarator-list:
    init-declarator
    init-declarator-list </i><b>,</b><i> init-declarator
</i></pre>

<pre><i>init-declarator:
    declarator
    declarator </i><b>=</b><i> initializer
</i></pre>

<pre><i>storage-class-specifier: </i><b>
    external
    register
    static
    alias
</b></pre>

<pre><i>type-specifier: </i><b>
    void
    bool
    char
    short
    int
    long
    float
    double
    signed
    unsigned
    complex</b><i>
    struct-or-union-specifier
    enum-specifier
    alias-name
</i></pre>

<pre><i>struct-or-union-specifier:
    struct-or-union identifier
</i></pre>

<pre><i>struct-or-union:</i><b>
    struct
    union
</b></pre>

<pre><i>struct-declaration-list:
    struct-declaration
    struct-delcaration-list struct-declaration
</i></pre>

<pre><i>struct-declaration:
    specifier-qualifier-list <u>struct-declarator-list</u>
</i></pre>

<pre><i>specifier-qualifier-list:
    type-specifier <u>specifier-qualifier-list</u>
    type-qualifier <u>specifier-qualifier-list</u>
</i></pre>

<pre><i>struct-declarator-list:
    struct-declarator
    struct-declarator-list </i><b>,</b><i> struct-declarator
</i></pre>

<pre><i>struct-declarator:
    declarator
    <u>declarator</u></i><b> = </b><i>constant-expresison
</i></pre>

<pre><i>enum-specifier:
    <b>enum</b> identifier
</i></pre>

<pre><i>enumerator-list:
    enumerator
    enumerator-list </i><b>,</b><i> enumerator
</i></pre>

<pre><i>enumerator:
    enumeration-constant
    enumeration-constant </i><b>=</b><i> constant-expression
</i></pre>

<pre><i>type-qualifier:</i><b>
    const
    restrict
    volatile
</b></pre>

<pre><i>function-specifier:</i><b>
    inline
</b></pre>

<pre><i>declarator:
    <u>pointer</u> direct-declarator
</i></pre>

<pre><i>direct-declarator:
    identifier
    </i><b>(</b><i> declarator </i><b>)</b><i>
    direct-declarator </i><b>[</b><i> <u>type-qualifier-list</u> <u>assignment-expression</u> </i><b>]</b><i>
    direct-declarator </i><b>[ static</b><i> <u>type-qualifier-list</u> assignment-expression </i><b>]</b><i>
    direct-declarator </i><b>[</b><i> type-qualifier-list </i><b>static</b><i> assignment-expression </i><b>]</b><i>
    direct-declarator </i><b>[</b><i> <u>type-qualifier-list</u> </i><b>* ]</b><i>
    direct-declarator </i><b>(</b><i> parameter-type-list </i><b>)</b><i>
</i></pre>

<pre><i>pointer:
    </i><b>*</b><i> <u>type-qualifier-list</u>
    </i><b>*</b><i> <u>type-qualifier-list</u> pointer
</i></pre>

<pre><i>type-qualifier-list:
    type-qualifier
    type-qualifier-list type-qualifier
</i></pre>

<pre><i>parameter-type-list:
    parameter-list
    parameter-list </i><b>, ...</b><i>
</i></pre>

<pre><i>parameter-list:
    parameter-declaration
    parameter-list </i><b>,</b><i> parameter-declaration
</i></pre>

<pre><i>parameter-declaration:
    declaration-specifiers declarator
    declaration-specifiers <u>abstract-declarator</u>
</i></pre>

<pre><i>type-name:
    specifier-qualifier-list <u>abstract-declarator</u>
</i></pre>

<pre><i>abstract-declarator:
    pointer
    <u>pointer</u> direct-abstract-declarator
</i></pre>

<pre><i>direct-abstract-declarator:
    </i><b>(</b><i> abstract-declarator </i><b>)</b><i>
    direct-abstract-declarator </i><b>[</b><i> <u>type-qualifier list</u> <u>assignment-expression</u> </i><b>]</b><i>
    direct-abstract-declarator </i><b>[ static</b><i> <u>type-qualifier-list</u> assignment-expression </i><b>]</b><i>
    direct-abstract-declarator </i><b>[</b><i> type-qualifier-list </i><b>static</b><i> assignment-expression </i><b>]</b><i>
    direct-abstract-declarator </i><b>[</b><i> <u>type-qualifier-list</u> </i><b>* ]</b><i>
    <u>direct-abstract-declarator</u> </i><b>(</b><i> <u>parameter-type-list</u> </i><b>)</b><i>
</i></pre>

<pre><i>alias-name:
    identifier
</i></pre>

<pre><i>initializer:
    assignment-expression
</i></pre>

## Statements
