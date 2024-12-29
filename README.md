# rpn.py

This is an implementation of a Reverse Polish Notation (RPN) Calculator.
Its written in Python.

RPN is neat because you can do fancy calculations without having
to worry about parenthesis. Putting the operator after the operands
allow the operator to infer which are its operands without the clarification
offered by paranthesis.

1 + 2 becomes 1 2 + \
3 * 4 becomes 3 4 * \
1/(2-(3*(4+5))) becomes \
1 2 3 4 5 + * - / \
1 2 3 9 * - / \
1 2 27 - / \
1 -25 / \
and the answer is -0.04

The opposite of Reverse Polish Notation is Polish Notation, where the operator
is written before the operands. Many programmers will recognise this as the
above calculation can be written as div(1, sub(2, mult(3, add(4, 5)))).

# Usage

`> python rpn.py`

should open the graphical user interface.

It is also possible to run the rpn.py file from an IDE.

# bug? Hwat bug?

If you find a bug in my code, please make an issue. Describe what goes wrong
and how to replicate it. I'll try to fix it.

# version

This script is written using Python 3.8.8 and the modules
- `math`
- `tkinter`
- `random`
- `re` \

all of which are part of the Python standard library.
