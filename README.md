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

# Usage

`> python rpn.py`

should open the graphical user interface.
