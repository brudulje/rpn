import tkinter as tk
from tkinter import messagebox
import math
import random
import re


class RPN():
    stack = []  # Stack for RPN calculation
    operator_2 = {'+', '-', '\u00d7',  # times
                  '/', '^', '\u00f7',  # int div
                  '%', 'n\u221a',  # nth root
                  'E', 'nCk',
                  '\u2295',  # circled pluss
                  }
    operator_1 = {'\u221a',  # root
                  'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
                  'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
                  'ln', 'log', 'lg2',
                  '1/x', '!', '=', '2^x', 'x^2', '\u2684'}  # dice5
    operator_0 = {'\u03c0', '\u03c4', '\u03c6', 'e', 'Rand'}  # pi, tau, phi, e

    def evaluate_two(self, expression):
        """Operate operators taking two operands."""

        try:
            operand1 = expression[0]
            operand2 = expression[1]
            operator = expression[2]  # Operator
            # _ = float(operand1)
            # _ = float(operand2)
        except ValueError as e:
            # Does this ever happen?
            messagebox.showerror("ValueError", f"{str(e)}")
            return None
        except TypeError as e:
            # Does this ever happen?
            messagebox.showerror("TypeError", f"{str(e)}")
            return None
        except IndexError:
            messagebox.showerror("IndexError",
                                 f"Too few operands to {expression}.")
            return None
        # Perform the operation based on the operator
        if operator == '+':
            try:
                return operand1 + operand2
            except OverflowError as e:
                messagebox.showerror("OverflowError", str(e))
        elif operator == '-':
            return operand1 - operand2
        elif operator == '\u00d7':  # times
            try:
                return operand1 * operand2
            except OverflowError as e:
                messagebox.showerror("OverflowError", str(e))
        elif operator == '/' or operator == '\u00f7':
            # \u00f7 is division symbol for integer division
            if operand2 == 0:
                messagebox.showerror("Error",
                                     "Division by zero is undefined.")
            elif operand1 % operand2 == 0 or operator == '\u00f7':
                # Keeps the result an int if possible
                return operand1 // operand2
            else:
                return operand1 / operand2
        elif operator == '^':
            try:
                return operand1 ** operand2
            except OverflowError as e:
                messagebox.showerror("OverflowError", str(e))
        elif operator == '%':
            return operand1 % operand2
        elif operator == 'n\u221a':
            if operand1 < 0:
                messagebox.showerror("Error",
                                     "Root of negative numbers not supported.")
                return None
            else:
                return operand1 ** (1/operand2)
        elif operator == '\u2295':  # Circled pluss
            try:
                return math.sqrt(operand1**2 + operand2**2)
            except OverflowError as e:
                messagebox.showerror("OverflowError",
                                     f"{operand1}, {operand2}, {operator} "
                                     + "does not work", str(e))
        elif operator == 'E':
            try:
                return operand1 * 10 ** operand2
            except OverflowError as e:
                messagebox.showerror("OverflowError",
                                     f"{operand1}, {operand2}, {operator} "
                                     + "does not work", str(e))
        elif operator == 'nCk':
            try:
                return math.comb(operand1, operand2)
            except TypeError as e:
                messagebox.showerror("TypeError",
                                     f"{operand1}, {operand2}, {operator} "
                                     + "does not work", str(e))
        else:
            messagebox.showerror("Error", f"Unknown 2operator {operator}.")
        return None

    def evaluate_one(self, expression):
        """Operate operators taking a single operand."""
        # {'\u221a', 'sin', 'cos', 'tan', 'ln', 'log', 'x^2', '1/x'}
        try:
            operand = expression[0]
            operator = expression[1]
        except IndexError:
            messagebox.showerror("IndexError",
                                 f"Too few arguments to {expression}.")
            return None

        if operator == '\u221a':
            if operand < 0:
                messagebox.showerror("Error",
                                     "Root of negative numbers not supported.")
                return None
            else:
                return math.sqrt(operand)
        elif operator == 'sin':
            return math.sin(operand)
        elif operator == 'cos':
            return math.cos(operand)
        elif operator == 'tan':
            return math.tan(operand)
        elif operator == 'ln':
            return math.log(operand)
        elif operator == 'lg2':
            return math.log2(operand)
        elif operator == 'log':
            return math.log10(operand)
        elif operator == '1/x':
            # print(operator, operand)
            return 1 / operand
        elif operator == 'asin':
            return math.asin(operand)
        elif operator == 'acos':
            return math.acos(operand)
        elif operator == 'atan':
            return math.atan(operand)
        elif operator == '!':
            if type(operand) == int:
                return math.factorial(operand)
            else:
                return math.gamma(operand + 1)
        elif operator == '=':  # Rounds last operand to an int
            return int(operand)
        elif operator == 'x^2':  # Depricated  # Reintroduced
            try:
                return operand ** 2
            except OverflowError as e:
                messagebox.showerror("OverflowError", str(e))
        elif operator == '2^x':
            try:
                return 2 ** operand
            except OverflowError as e:
                messagebox.showerror("OverflowError", str(e))
        elif operator == '\u2684':  # dice5
            return math.ceil(operand * random.random())
        elif operator == 'sinh':
            return math.sinh(operand)
        elif operator == 'cosh':
            return math.cosh(operand)
        elif operator == 'tanh':
            return math.tanh(operand)
        elif operator == 'asinh':
            return math.asinh(operand)
        elif operator == 'acosh':
            return math.acosh(operand)
        elif operator == 'atanh':
            return math.atanh(operand)
        else:
            messagebox.showerror("Error",
                                 f"Unknown 1operator {operator}.")
        return None

    def evaluate_zero(self, text):
        # {'Rand', '\u03c0', '\u03c4', 'e', '\u03c6}
        text = text[0]
        if text == '\u03c0':  # pi
            return math.pi
        elif text == '\u03c4':  # tau
            return 2 * math.pi
        elif text == 'e':
            return math.e
        elif text == '\u03c6':  # phi
            return (1 + math.sqrt(5))/2
        elif text == 'Rand':
            return random.random()
        else:
            messagebox.showerror("Error",
                                 f"Unknown 0operator {text}.")
        return None

    def process_operator(self, operator, operand_count, eval_function=None):
        """
        Helper function to handle the common tasks for processing operators.
        """
        # print("process_operator got operator ", operator)
        self.stack.append(operator)

        if eval_function:
            # This is where thing might take time
            result = eval_function(self.stack[-operand_count:])

            if result is not None:
                # Remove the operands from the stack if calculation is good
                self.stack = self.stack[:-operand_count]
                self.stack.append(result)
            else:
                # Remove failed operator from stack
                self.stack = self.stack[:-1]

    def process_number(self, text):
        """
        Helper function to handle the processing of a number.
        """
        # print("process_number got ", text)
        try:
            if "." not in text:
                value = int(text)
            else:
                value = float(text)
            self.stack.append(value)
        except ValueError:
            messagebox.showerror("ValueError",
                                 "Invalid input. \n"
                                 + f"I don't think '{text}' is a number.")

    def process_token(self, text):
        """Process token input to stack.

        Separate numbers from operators and call the evaluate function
        taking the correct number of operands for the current operator.
        Do some of the job previously done by CalculatorGUI.process_input()"""

        # print("process_token got ", text)
        if text in self.operator_2:
            # Operator takes two operands
            self.process_operator(text, 3, self.evaluate_two)
        elif text in self.operator_1:
            # Operator takes one operand
            self.process_operator(text, 2, self.evaluate_one)
        elif text in self.operator_0:
            # Operator takes no operands
            self.process_operator(text, 1, self.evaluate_zero)
        else:
            # Process a number
            self.process_number(text)


class CalculatorGUI(tk.Tk):
    def __init__(self, rpn):
        super().__init__()
        self.rpn = rpn
        self.title("RPN Calculator")
        self.geometry("330x360")
        self.history = []  # List of input

        self.operators = \
            self.rpn.operator_0 | self.rpn.operator_1 | self.rpn.operator_2

        # Regex magic to allow operators to be entered together with the
        # last number before the operator
        self.sorted_operators = sorted(self.operators, key=len, reverse=True)
        # Create a regex pattern to match the longest operator
        # at the end of the string
        pattern = '|'.join(re.escape(op) for op in self.sorted_operators)
        # Match the operator only at the end
        # and ensure there is something before it
        self.pattern = f"^(.*?)(?={pattern})({pattern})$"

        # Dictionary of help texts for each button
        self.help_texts = {  # keep in gui
            '.': "Decimal point. \n"
            + "Separates the whole number from the fraction.",
            '0': "0; Zero, \n"
            + "The first digit and the basis of positional notation.",
            '1': "1; One. First and foremost. Number one.",
            '2': "2; Two is never first, but close.",
            '3': "3; Three. First odd prime.",
            '4': "4; Four in a row.",
            '5': "5; Five is a handful.",
            '6': "6; Six. First rectangular number.",
            '7': "7; Seven. An excellent choise.",
            '8': "8; Eight. The first digit in alphabetical order.",
            '9': "9; Nine. First odd square.",
            'π': "Pi is the circumference of a circle \n"
            + "divided by its diameter.",
            '\u03c4': "Tau is the circumference of a circle \n"
            + "divided by its radius.",
            'e': "e is a mathematical constant, \n"
            + "the base of the natural logarithm and exponential function.\n"
            + "e is approximately equal to 2.718281828459045235360287471352.",
            '\u03c6': "Phi is the golden ratio. \n"
            + "1 / phi = phi - 1.",
            '+': "Addition operator. \n"
            + "Adds two numbers.",
            '-': "Subtraction operator. \n"
            + "Subtracts the second number from the first.",
            '\u00d7': "Multiplication operator. \n"
            + "Multiplies two numbers.",
            '/': "Division operator. \n"
            + "Divides the first number by the second.",
            '^': "Exponentiation operator. \n"
            + "Raises the first number to the power of the second.",
            '÷': "Integer division. \n"
            + "Returns the integer part after division.",
            '%': "Modulus operator. \n"
            + "Returns the remainder of the division of two numbers.",
            '√': "Square root operator. \n"
            + "Returns the square root of a number.",
            'sin': "Sine function. \n"
            + "Returns the sine of an angle.",
            'cos': "Cosine function. \n"
            + "Returns the cosine of an angle.",
            'tan': "Tangent function. \n"
            + "Returns the tangent of an angle.",
            'asin': "Inverse sine function. \n"
            + "Returns the inverse of sin.",
            'acos': "Inverse cosine function. \n"
            + "Returns the inverse of cos.",
            'atan': "Inverse tangent function. \n"
            + "Returns the inverse of tan",
            'sinh': "Hyperbolic sine function. \n"
            + "Returns the hyperbolic sine of an angle.",
            'cosh': "Hyperbolic cosine function. \n"
            + "Returns the hyperbolic cosine of an angle.",
            'tanh': "Hyperbolic tangent function. \n"
            + "Returns the hyperbolic tangent of an angle.",
            'asinh': "Inverse hyperbolic sine function. \n"
            + "Returns the inverse of sinh.",
            'acosh': "Inverse hyperbolic cosine function. \n"
            + "Returns the inverse of cosh.",
            'atanh': "Inverse hyperbolic tangent function. \n"
            + "Returns the inverse of tanh.",
            'ln': "Natural logarithm function. \n"
            + "Returns the natural logarithm of a number.",
            'lg2': "Base-2 logarithm function. \n"
            + "Returns the logarithm of a number with base 2.",
            'log': "Base-10 logarithm function. \n"
            + "Returns the logarithm of a number with base 10.",
            '1/x': "Reciprocal operator. \n"
            + "Returns the reciprocal (1 divided by the number).",
            '2^x': "Raise 2 to the power of x.",
            'x^2': "Square x.",
            '!': "Factorial function. \n"
            + "Returns the factorial of a integer. \n"
            + "For floats, it returns the \u0393(x+1), which is widely \n"
            + "accepted as the factorial of non-integer numbers.",
            '=': "'=' on an RPN? \n"
            + "Yeah, this truncates the number i.e. rounds towards zero.",
            'Rand': "Generates a random number between 0 and 1.",
            'n√': "Nth root operator. \n"
            + "Returns the nth root of the first number.",
            '\u2295': "Root Sum Square operator. \n"
            + "Returns the Euclidean norm (distance) between two numbers. \n"
            + "Equivalent to ['a', 'x^2', 'b', 'x^2', '+', '√']",
            'E': "Scientific notation. \n"
            + "x, y, E is x * 10^y.",
            'sci': "Toggle various scientific functions.",
            '?': "This is the help button. \n"
            + "Click '?' and another button to get help on that other button.",
            '(-)': "Negative symbol for entering negative numbers.",
            'hyp': "Toggle hyperbolic trigonometric functions.",
            'nCk': "How many ways you can choose k from n.",
            '\u2684': "Trow an n-sided dice. \n"
            + "If n is not integer, the last side of the \n"
            + "dice is a little smaller than the others. \n"
            + "A \u03c4-sided dice will sometimes give 7.",
            'Clear': "Clears the input, one character at a time. \n"
            + "If no input, clears the stack.\n"
            + "If no stack, clears history, \n"
            + "If no history, takes a nap.",
            'Enter': "Transfers your input number to the stack."
        }

        self.help_mode = False  # Initially not in help mode
        self.sci_mode = 0  # Initially not in scientific mode
        self.hyp_mode = 0  # Initailly not in hyperbola mode

        self.colors = {
            'digit': '#ade',  # close to 'lightblue',
            'number': '#69b',  # slightly darker blue
            'op1': '#9e9',  # 'lightgreen',
            'op2': '#6b6',  # slightly darker green
            'Clear': 'lightgray',
            'Enter': 'darkgray',
            'sci': ['#ffa', '#fd5', '#fa0'],  # yellows/orange
            'help': ['#a66', '#a00']  # reds
        }

        self.button_objs = {}
        self.main_buttons = []  # Trying to keep track of all buttons
        self.main_labels = []

        # settings
        self.settings_digits = 17
        self.settings_layout = 'small'  # 'small', 'wide', 'tall'

        # Set layout
        self.create_button_layout(self.settings_layout)

        # Menu
        menubar = tk.Menu()
        self.config(menu=menubar)
        # Create a 'Settings' menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Fairly square",
                                  command=lambda: self.create_button_layout
                                  ('small'))
        settings_menu.add_command(label="Wide and nerdy",
                                  command=lambda: self.create_button_layout
                                  ('wide'))
        settings_menu.add_command(label="A tall order",
                                  command=lambda: self.create_button_layout
                                  ('tall'))

        # Create the 'Digits' setting submenu
        digits_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Show digits in stack",
                                  menu=digits_menu)

        # Define the valid choices for digits
        valid_digits = [1, 2, 3, 5, 7, 11, 13, 17]

        # Add the valid digits as menu items
        for digit in valid_digits:
            digits_menu.add_command(label=str(digit),
                                    command=lambda digit=digit:
                                        self.set_digits(digit))

    def set_digits(self, digit: int = 17):
        self.settings_digits = digit
        self.update_display()

    def create_button_layout(self, settings_layout):
        """Set up button layout based on the selected layout
        ('small', 'wide', or 'tall')."""

        if settings_layout == 'small':
            self.geometry("330x360")

            self.buttons = [('\u221a', 3, 3, self.colors['op1']),  # root
                            ('sci', 3, 4, self.colors['sci'][0]),
                            ('7', 4, 0, self.colors['digit']),
                            ('8', 4, 1, self.colors['digit']),
                            ('9', 4, 2, self.colors['digit']),
                            ('/', 4, 3, self.colors['op2']),
                            ('\u03c0', 4, 4, self.colors['number']),  # pi
                            ('4', 5, 0, self.colors['digit']),
                            ('5', 5, 1, self.colors['digit']),
                            ('6', 5, 2, self.colors['digit']),
                            ('\u00d7', 5, 3, self.colors['op2']),  # x
                            ('^', 5, 4, self.colors['op2']),
                            ('1', 6, 0, self.colors['digit']),
                            ('2', 6, 1, self.colors['digit']),
                            ('3', 6, 2, self.colors['digit']),
                            ('-', 6, 3, self.colors['op2']),
                            ('%', 6, 4, self.colors['op2']),
                            ('(-)', 7, 0, self.colors['digit']),
                            ('0', 7, 1, self.colors['digit']),
                            ('.', 7, 2, self.colors['digit']),
                            ('+', 7, 3, self.colors['op2']),
                            ('\u00f7', 7, 4, self.colors['op2']),  # div
                            ]

            # Set position for special buttons and fields
            self.entry_grid = (0, 0, 5, '')
            self.entry_width = 25
            self.rpn.stack_label_grid = (1, 0, 5, '')
            self.rpn.stack_label_width = 30
            self.history_label_grid = (2, 0, 5, '')
            self.history_label_width = 30
            self.clear_button_grid = (3, 1, 2, 'e')
            self.clear_button_width = 6
            self.enter_button_grid = (3, 0, 2, 'w')
            self.enter_button_width = 6
            self.help_button_grid = (3, 1, 1, '')
            self.help_button_width = 2

        elif settings_layout == 'wide':
            self.geometry("650x330")

            # Wide layout (buttons rearranged for a wider view)
            self.buttons = [('Rand', 3, 0, self.colors['number']),
                            ('\u2684', 3, 1, self.colors['op1']),  # dice
                            ('!', 3, 2, self.colors['op1']),
                            ('1/x', 3, 3, self.colors['op1']),
                            # 3, 4, to 3, 8, is the Enter Clear and ? buttons
                            ('hyp', 3, 9, self.colors['sci'][0]),
                            ('\u03c6', 4, 0, self.colors['number']),  # phi
                            ('=', 4, 1, self.colors['op1']),
                            ('x^2', 4, 2, self.colors['op1']),
                            ('2^x', 4, 3, self.colors['op1']),
                            ('7', 4, 4, self.colors['digit']),
                            ('8', 4, 5, self.colors['digit']),
                            ('9', 4, 6, self.colors['digit']),
                            ('/', 4, 7, self.colors['op2']),
                            ('\u00f7', 4, 8, self.colors['op2']),  # div
                            ('\u221a', 4, 9, self.colors['op1']),  # root
                            ('e', 5, 0, self.colors['number']),
                            ('ln', 5, 1, self.colors['op1']),
                            ('log', 5, 2, self.colors['op1']),
                            ('lg2', 5, 3, self.colors['op1']),
                            ('4', 5, 4, self.colors['digit']),
                            ('5', 5, 5, self.colors['digit']),
                            ('6', 5, 6, self.colors['digit']),
                            ('\u00d7', 5, 7, self.colors['op2']),  # x
                            ('^', 5, 8, self.colors['op2']),
                            ('n\u221a', 5, 9, self.colors['op2']),  # nth root
                            ('\u03c0', 6, 0, self.colors['number']),  # pi(?)
                            ('sin', 6, 1, self.colors['op1']),
                            ('cos', 6, 2, self.colors['op1']),
                            ('tan', 6, 3, self.colors['op1']),
                            ('1', 6, 4, self.colors['digit']),
                            ('2', 6, 5, self.colors['digit']),
                            ('3', 6, 6, self.colors['digit']),
                            ('-', 6, 7, self.colors['op2']),
                            ('%', 6, 8, self.colors['op2']),
                            ('nCk', 6, 9, self.colors['op2']),
                            ('\u03c4', 7, 0, self.colors['number']),  # tau
                            ('asin', 7, 1, self.colors['op1']),
                            ('acos', 7, 2, self.colors['op1']),
                            ('atan', 7, 3, self.colors['op1']),
                            ('(-)', 7, 4, self.colors['digit']),
                            ('0', 7, 5, self.colors['digit']),
                            ('.', 7, 6, self.colors['digit']),
                            ('+', 7, 7, self.colors['op2']),
                            ('\u2295', 7, 8, self.colors['op2']),
                            ('E', 7, 9, self.colors['op2'])
                            ]

            # Set postion, size and shape for special buttons and fields
            self.entry_grid = (0, 0, 3, '')
            self.entry_width = 15
            self.rpn.stack_label_grid = (0, 3, 7, 'w')
            self.rpn.stack_label_width = 44
            self.history_label_grid = (2, 0, 10, 'e')
            self.history_label_width = 63
            self.enter_button_grid = (3, 4, 2, '')
            self.enter_button_width = 10
            self.clear_button_grid = (3, 6, 2, '')
            self.clear_button_width = 10
            self.help_button_grid = (3, 8, 1, '')
            self.help_button_width = 4

        elif settings_layout == 'tall':
            self.geometry("330x620")

            # Wide layout (buttons rearranged for a wider view)
            self.buttons = [('Rand', 3, 0, self.colors['number']),
                            ('\u2684', 3, 1, self.colors['op1']),  # dice
                            ('!', 3, 2, self.colors['op1']),
                            ('1/x', 3, 3, self.colors['op1']),
                            ('\u03c6', 4, 0, self.colors['number']),  # phi
                            ('=', 4, 1, self.colors['op1']),
                            ('x^2', 4, 2, self.colors['op1']),
                            ('2^x', 4, 3, self.colors['op1']),
                            ('\u221a', 4, 4, self.colors['op1']),  # root
                            ('e', 5, 0, self.colors['number']),
                            ('ln', 5, 1, self.colors['op1']),
                            ('log', 5, 2, self.colors['op1']),
                            ('lg2', 5, 3, self.colors['op1']),
                            ('n\u221a', 5, 4, self.colors['op2']),  # nth root
                            ('\u03c0', 6, 0, self.colors['number']),  # pi(?)
                            ('sin', 6, 1, self.colors['op1']),
                            ('cos', 6, 2, self.colors['op1']),
                            ('tan', 6, 3, self.colors['op1']),
                            ('nCk', 6, 4, self.colors['op2']),
                            ('\u03c4', 7, 0, self.colors['number']),  # tau
                            ('asin', 7, 1, self.colors['op1']),
                            ('acos', 7, 2, self.colors['op1']),
                            ('atan', 7, 3, self.colors['op1']),
                            ('E', 7, 4, self.colors['op2']),
                            ('hyp', 8, 4, self.colors['sci'][0]),
                            ('7', 9, 0, self.colors['digit']),
                            ('8', 9, 1, self.colors['digit']),
                            ('9', 9, 2, self.colors['digit']),
                            ('/', 9, 3, self.colors['op2']),
                            ('\u00f7', 9, 4, self.colors['op2']),  # div
                            ('4', 10, 0, self.colors['digit']),
                            ('5', 10, 1, self.colors['digit']),
                            ('6', 10, 2, self.colors['digit']),
                            ('\u00d7', 10, 3, self.colors['op2']),  # x
                            ('^', 10, 4, self.colors['op2']),
                            ('1', 11, 0, self.colors['digit']),
                            ('2', 11, 1, self.colors['digit']),
                            ('3', 11, 2, self.colors['digit']),
                            ('-', 11, 3, self.colors['op2']),
                            ('%', 11, 4, self.colors['op2']),
                            ('(-)', 12, 0, self.colors['digit']),
                            ('0', 12, 1, self.colors['digit']),
                            ('.', 12, 2, self.colors['digit']),
                            ('+', 12, 3, self.colors['op2']),
                            ('\u2295', 12, 4, self.colors['op2']),
                            ]

            self.entry_grid = (0, 0, 5, '')
            self.entry_width = 25
            self.rpn.stack_label_grid = (1, 0, 5, '')
            self.rpn.stack_label_width = 30
            self.history_label_grid = (2, 0, 5, '')
            self.history_label_width = 30

            self.enter_button_grid = (8, 0, 2, '')
            self.enter_button_width = 10
            self.clear_button_grid = (8, 2, 2, '')
            self.clear_button_width = 10
            self.help_button_grid = (3, 4, 1, '')
            self.help_button_width = 4

        else:
            print(f"Invalid layout {settings_layout}")
            return

        # Create the buttons for the number pad and operators with colors
        self.forget_grid()
        for (text, row, col, color) in self.buttons:
            button = tk.Button(self, text=text,
                               font=("Lucida Sans Unicode", 14),
                               width=4, height=1, bg=color,
                               command=self.create_button_handler(text))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.button_objs[text] = button

        # Set correct font and colors on buttons
        self.update_buttons()

        # Entry field for RPN expression
        self.entry = tk.Entry(self, font=("Lucida Sans Unicode", 14),
                              borderwidth=1, relief="solid")
        self.entry.grid(row=self.entry_grid[0], column=self.entry_grid[1],
                        columnspan=self.entry_grid[2],
                        pady=5,
                        sticky=self.entry_grid[3])
        self.entry.config(width=self.entry_width)
        self.main_labels.append(self.entry)

        # Show the stack
        self.rpn.stack_label = tk.Label(self, text="Stack: []",
                                        font=("Lucida Sans Unicode", 12),
                                        height=1, anchor="e")
        self.rpn.stack_label.grid(row=self.rpn.stack_label_grid[0],
                                  column=self.rpn.stack_label_grid[1],
                                  columnspan=self.rpn.stack_label_grid[2],
                                  pady=5,
                                  sticky=self.history_label_grid[3])
        self.rpn.stack_label.config(width=self.rpn.stack_label_width)
        self.main_labels.append(self.rpn.stack_label)

        # Show input history
        self.history_label = tk.Label(self, text="History: []",
                                      font=("Lucida Sans Unicode", 12),
                                      height=1, anchor="e")
        self.history_label.grid(row=self.history_label_grid[0],
                                column=self.history_label_grid[1],
                                columnspan=self.history_label_grid[2],
                                pady=5,
                                sticky=self.history_label_grid[3])
        self.history_label.config(width=self.history_label_width)
        self.main_labels.append(self.history_label)

        # "Clear" button to clear the input
        self.clear_button = tk.Button(self, text="Clear",
                                      font=("Lucida Sans Unicode", 14),
                                      height=1,
                                      bg=self.colors["Clear"],
                                      # command=self.clear,
                                      command=lambda: self.on_button_click
                                      ("Clear"),
                                      )
        self.clear_button.grid(row=self.clear_button_grid[0],
                               column=self.clear_button_grid[1],
                               columnspan=self.clear_button_grid[2],
                               pady=5,
                               sticky=self.clear_button_grid[3])
        self.clear_button.config(width=self.clear_button_width)
        self.main_buttons.append(self.clear_button)

        # "Enter" button to add current value to the stack
        self.enter_button = tk.Button(self, text="Enter",
                                      font=("Lucida Sans Unicode", 14),
                                      height=1,
                                      bg=self.colors["Enter"],
                                      # command=self.process_input,
                                      command=lambda: self.on_button_click
                                      ("Enter"),
                                      )
        self.enter_button.grid(row=self.enter_button_grid[0],
                               column=self.enter_button_grid[1],
                               columnspan=self.enter_button_grid[2],
                               pady=5,
                               sticky=self.enter_button_grid[3])
        self.enter_button.config(width=self.enter_button_width)
        self.main_buttons.append(self.enter_button)

        # "Help" button to activate help mode
        self.help_button = tk.Button(self, text="?",
                                     font=("Lucida Sans Unicode", 14),
                                     height=1,
                                     bg=self.colors['help'][0],
                                     command=self.activate_help)
        self.help_button.grid(row=self.help_button_grid[0],
                              column=self.help_button_grid[1],
                              pady=5)
        self.help_button.config(width=self.help_button_width)
        self.main_buttons.append(self.help_button)

        # Update idsplay to keep stack, history visible
        self.update_display()

    def forget_grid(self):  # keep in gui
        """Clear any previous buttons from the grid."""
        # print(f"{len(self.button_objs)=}")
        for key, button in self.button_objs.items():
            button.grid_forget()
        self.button_objs.clear()

        for button in self.main_buttons:
            button.grid_forget()

        for label in self.main_labels:
            label.grid_forget()

    def create_button_handler(self, text):  # keep in gui
        """Returns a function that calls
        self.on_button_click with the button text."""
        def handler():
            self.on_button_click(text)
        return handler

    def update_buttons(self):
        """ Update colors and fonts for the buttons. """
        for k, _ in self.button_objs.items():
            # Change the color of some of the buttons
            if self.button_objs[k].cget('text') in self.rpn.operator_2:
                self.button_objs[k].config(bg=self.colors['op2'])
            if self.button_objs[k].cget('text') in self.rpn.operator_1:
                self.button_objs[k].config(bg=self.colors['op1'])
            if self.button_objs[k].cget('text') in self.rpn.operator_0:
                self.button_objs[k].config(bg=self.colors['number'])
            # Change font
            if self.button_objs[k].cget('text') in {'\u03c0',
                                                    '\u03c4',
                                                    '\u03c6'}:
                # greek letters
                self.button_objs[k].config(font=("Symbol", 14))
            else:
                self.button_objs[k].config(font=("Lucida Sans Unicode", 14))

    def toggle_sci_mode(self):  # keep in gui
        """Toggle between scientific and normal mode."""
        # There are 3 modes.
        self.sci_mode = (self.sci_mode + 1) % 3  # Change to next mode

        sci_layouts = [{'√': '√',
                        '/': '/',
                        '\u00d7': '\u00d7',  # times
                        '-': '-',
                        '+': '+',
                        '\u03c0': '\u03c0',  # pi
                        '%': '%',
                        '÷': '÷',
                        '^': '^',
                        },
                       {'√': 'n\u221a',  # root
                        '/': '1/x',
                        '\u00d7': 'tan',
                        '-': 'cos',
                        '+': 'sin',
                        '\u03c0': '\u03c4',  # tau
                        '%': 'ln',  # ln, was e
                        '÷': 'log',  # log was ln
                        '^': 'e',  # e was log
                        },
                       {'√': '\u2295',  # circled pluss
                        '/': 'Rand',
                        '\u00d7': 'atan',
                        '-': 'acos',
                        '+': 'asin',
                        '\u03c0': '\u03c6',  # phi
                        '%': '!',
                        '÷': 'lg2',
                        '^': '=',
                        }
                       ]

        # Change button labels to scientific mode and update handlers
        for k, v in sci_layouts[self.sci_mode].items():
            self.button_objs[k].config(text=v)
            self.button_objs[k].config(command=self.create_button_handler(v))
        # Update colors and fonts
        self.update_buttons()

        # Update sci button bg color
        self.button_objs['sci'].config(bg=self.colors['sci'][self.sci_mode])

    def toggle_hyp_mode(self):
        """Toggle between scientific and normal mode."""
        # There are 2 modes.
        self.hyp_mode = (self.hyp_mode + 1) % 2  # Change to next mode

        hyp_layouts = [{'sin': 'sin',
                        'cos': 'cos',
                        'tan': 'tan',
                        'asin': 'asin',
                        'acos': 'acos',
                        'atan': 'atan',
                        },
                       {'sin': 'sinh',
                        'cos': 'cosh',
                        'tan': 'tanh',
                        'asin': 'asinh',
                        'acos': 'acosh',
                        'atan': 'atanh',
                        }
                       ]

        # Change button labels to scientific mode and update handlers
        for k, v in hyp_layouts[self.hyp_mode].items():
            self.button_objs[k].config(text=v)
            self.button_objs[k].config(command=self.create_button_handler(v))
        # Update colors and fonts
        self.update_buttons()

        # Update hyp button bg color
        self.button_objs['hyp'].config(bg=self.colors['sci'][self.hyp_mode])

    def on_button_click(self, button_text):
        """Handle button click."""
        # print(button_text)
        if self.help_mode:
            # Show help text for the clicked button
            help_text = self.help_texts.get(button_text,
                                            "Sorry, can't help you there.")
            messagebox.showinfo("Help", help_text)
            self.deactivate_help()
        elif button_text == 'sci':
            self.toggle_sci_mode()
        elif button_text == 'hyp':
            self.toggle_hyp_mode()
        elif button_text == "Enter":
            self.process_input()
        elif button_text == "Clear":
            self.clear()
        else:
            # For operators, we insert the operator and immediately calculate
            if button_text in self.operators:
                # print("op")
                # For operators like '+', '-', '\u00d7', '/', etc.
                self.entry.insert(tk.END, button_text)
                self.process_input()  # Automatically trigger calculation
            else:
                # print("num")
                # For numbers, just insert them into the entry field
                if button_text == '(-)':
                    # handle inputting negative numbers.
                    self.entry.insert(tk.END, '-')
                else:
                    self.entry.insert(tk.END, button_text)

    def process_input(self):
        """Add the current value (operand or operator) to the stack
        when Enter is pressed."""
        current_text = self.entry.get().strip()
        self.history.append(current_text)

        if current_text:
            match = re.search(self.pattern, current_text)
            # print(f"Yes, {current_text=}")
            # Number and operator entered together.
            if match and match.group(1) and match.group(2):
                # print("Yes, match")
                # print(f"{match.group(1)}, {match.group(2)}")
                self.rpn.process_token(match.group(1))
                self.rpn.process_token(match.group(2))
                self.entry.delete(0, tk.END)
            else:
                # print("No match", current_text)
                self.rpn.process_token(current_text)
            self.entry.delete(0, tk.END)

            # Always update the stack_label to show the current stack
            self.update_display()
        else:
            pass
            # messagebox.showerror("Error",
            #                      "Please enter a valid number or operator.")

    def clear(self):
        """Clear various variables when the Clear button is pressed."""
        text = self.entry.get().strip()
        if text:
            # There is something in the entry field; clear this piecewise
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text[:-1])
        elif self.rpn.stack:
            # Entry field is empty, stack has something in it
            self.rpn.stack.clear()
            self.update_display()
        elif self.history:
            # Stack is also empty, history has something in it
            self.history.clear()
            self.update_display()
        else:
            # Nothing more to clear
            pass

    def update_display(self):
        """Update the stack and history display labels."""
        # Update stack display
        # Pretty print stack
        stack_string = "Stack: ["
        for idx, token in enumerate(self.rpn.stack):
            if type(token) == float:
                stack_string += f"{token:.{self.settings_digits}g}"
            else:
                # token should be type int
                stack_string += str(token)
            if idx + 1 < len(self.rpn.stack):
                # Add the comma only for the entries which are not the last
                stack_string += ", "
        stack_string += "]"
        self.rpn.stack_label.config(text=stack_string)
        # Update stack display
        self.history_label.config(text=f"History: {self.history}")

    def activate_help(self):
        """Activate help mode and wait for user to click a button."""
        if self.help_mode:
            # Provide help on help button
            help_text = self.help_texts.get('?',
                                            "No help for this button.")
            messagebox.showinfo("Help", help_text)
            self.deactivate_help()
        else:
            self.help_mode = True
            self.help_button.config(bg=self.colors['help'][1])
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Click button for help.")

    def deactivate_help(self):
        self.help_button.config(bg=self.colors['help'][0])
        self.entry.delete(0, tk.END)
        self.help_mode = False


if __name__ == "__main__":
    rpn_calc = RPN()  # Create an instance of the Calculator class
    app = CalculatorGUI(rpn_calc)  # Pass the calculator object to the GUI
    app.mainloop()
