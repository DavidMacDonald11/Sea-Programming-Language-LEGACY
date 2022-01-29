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

<pre><i>constant-expression
    conditional-expression
</i></pre>
