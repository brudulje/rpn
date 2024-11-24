import tkinter as tk
from tkinter import messagebox
import math
import random
import re
# import time


class RPN():
    stack = []  # Stack for RPN calculation
    operator_2 = {'+', '-', '\u00d7',  # times
                  '/', '^', '\u00f7',  # int div
                  '%', 'n\u221a',  # nth root
                  # 'E',
                  '\u2295',  # circled pluss
                  }
    operator_1 = {'\u221a',  # root
                  'sin', 'cos', 'tan',
                  'asin', 'acos', 'atan',
                  'ln', 'log', 'lg2',
                  '1/x', '!', '=', '2^x'}
    operator_0 = {'\u03c0', '\u03c4', '\u03c6', 'e', 'Rand'}  # pi, tau, phi, e

    def evaluate_two(self, expression):
        """Operate operators taking two operands."""
        try:
            operand1 = expression[0]
            operand2 = expression[1]
            operator = expression[2]  # Operator
            _ = float(operand1)
            _ = float(operand2)
        except (ValueError, TypeError, IndexError):
            messagebox.showerror("Error",
                                 f"Don't know what to do with {expression}.")
            return None
        # Perform the operation based on the operator
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '\u00d7':  # times
            result = operand1 * operand2
        elif operator == '/':
            if operand1 % operand2 == 0:
                # Keeps the result an int if possible
                result = operand1 // operand2
            else:
                try:
                    result = operand1 / operand2
                except ValueError:
                    messagebox.showerror("Error",
                                         "Division by zero is undefined.")
        elif operator == '^':
            result = operand1 ** operand2
        elif operator == '\u00f7':  # Division symbol for integer division
            result = operand1 // operand2
        elif operator == '%':
            result = operand1 % operand2
        elif operator == 'n\u221a':
            result = operand1 ** (1/operand2)
        elif operator == '\u2295':  # Circled pluss
            result = math.sqrt(operand1**2 + operand2**2)
        elif operator == 'E':
            return operand1 * 10 ** operand2
        else:
            messagebox.showerror("Error", f"Unknown 2operator {operator}.")

        return result

    def evaluate_one(self, expression):
        """Operate operators taking a single operand."""
        # {'\u221a', 'sin', 'cos', 'tan', 'ln', 'log', 'x^2', '1/x'}
        try:
            operand = expression[0]
            operator = expression[1]
        except IndexError:
            messagebox.showerror("Error",
                                 f"Too few arguments to {expression}.")
            return None

        if operator == '\u221a':
            if operand < 0:
                messagebox.showerror("Error",
                                     "Root of negative numbers not supported.")

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
            try:
                return math.factorial(operand)
            except ValueError:
                messagebox.showerror("Error",
                                     f"Cant run {operator} on {operand}.")

        elif operator == '=':  # Rounds last operand to an int
            return int(operand)
        # elif operator == 'x^2':  # Depricated
        #     return operand ** 2
        elif operator == '2^x':
            return 2 ** operand
        else:
            # raise ValueError(f"Unknown operator {operator}.")
            messagebox.showerror("Error",
                                 f"Unknown 1operator {operator}.")

    def evaluate_zero(self, text):
        # {'\u03c0', '\u03c4', 'e'}
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
            # raise ValueError(f"Unknown operator {operator}.")
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
            # Try to convert to integer or float
            if "." not in text:
                value = int(text)
            else:
                value = float(text)
            self.stack.append(value)
        except ValueError:
            messagebox.showerror("Error", f"Invalid number: {text}")

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
        self.title("RPN Calculator")
        self.geometry("330x360")
        self.rpn = rpn
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
            '.': "Decimal point. Separates the whole number from the \
                fraction.",
            '0': "0; Zero, the first digit and the basis of positional \
                notation.",
            '1': "1; First and foremost. Number one.",
            '2': "2; Never first, but close.",
            '3': "3; First odd prime.",
            '4': "4; Four in a row.",
            '5': "5; Five is a handful.",
            '6': "6; Six. First rectangular number.",
            '7': "7; Seven. An excellent choise.",
            '8': "8; Eight. The first digit in alphabetical order.",
            '9': "9; Nine. First odd square.",
            'π': "Pi is the circumference of a circle divided by its "
            + "diameter.",
            '\u03c4': "Tau is the circumference of a circle divided by its "
            + "radius.",
            'e': "Euler's number (e) is a mathematical constant approximately "
            + "equal to 2.71828.",
            '\u03c6': "Phi is the golden ratio. 1 / phi = phi - 1.",
            '+': "Addition operator. Adds two numbers.",
            '-': "Subtraction operator. Subtracts the second number from the "
            + "first.",
            '\u00d7': "Multiplication operator. Multiplies two numbers.",
            '/': "Division operator. Divides the first number by the second.",
            '^': "Exponentiation operator. Raises the first number to the "
            + "power of the second.",
            '÷': "Integer division. Returns the integer part after division.",
            '%': "Modulus operator. Returns the remainder of the division "
            + "of two numbers.",
            '√': "Square root operator. Returns the square root of a number.",
            'sin': "Sine function. Returns the sine of an angle.",
            'cos': "Cosine function. Returns the cosine of an angle.",
            'tan': "Tangent function. Returns the tangent of an angle.",
            'asin': "Inverse sine function. Returns the inverse of sin.",
            'acos': "Inverse cosine function. Returns the inverse of cos.",
            'atan': "Inverse tangent function. Returns the inverse of tan",
            'ln': "Natural logarithm function. Returns the natural logarithm "
            + "of a number.",
            'lg2': "Base-2 logarithm function. Returns the logarithm of a "
            + "number with base 2.",
            'log': "Base-10 logarithm function. Returns the logarithm of a "
            + "number with base 10.",
            '1/x': "Reciprocal operator. Returns the reciprocal (1 divided "
            + "by the number).",
            '2^x': "Raise 2 to the power of x.",
            '!': "Factorial function. Returns the factorial of a number.",
            '=': "'=' on an RPN? Yeah, this rounds the number to the nearest "
            + "integer.",
            'Rand': "Generates a random number between 0 and 1.",
            'n√': "Nth root operator. Returns the nth root of the first "
            + "number.",
            '\u2295': "Circled Plus operator. Returns the Euclidean norm "
            + "(distance) between two numbers. Equivalent to "
            + "['a', '2', '^', 'b', '2', '^', '+', '√']",
            'E': "Scientific notation. x, y, E is x * 10^y.",
            'sci': "Toggle various scientific functions.",
            '?': "This is the help button. Click this and another button "
            + "to get help on that other button.",
            '(-)': "Negative symbol for entering negative numbers.",
            'Clear': "Clears the input. \nIf no input, clears the stack."
            + "\nIf no stack, clears history.",
            'Enter': "Transfers your input number to the stack."
        }

        # To track if help mode is active
        self.help_mode = False

        self.sci_mode = 0  # Initially not in scientific mode
        self.colors = {
            'digit': '#ade',  # close to 'lightblue',
            'number': '#69b',  # slightly darker blue
            'op1': '#9e9',  # 'lightgreen',
            'op2': '#6b6',  # slightly darker green
            'Clear': 'lightgray',
            'Enter': 'darkgray',
            # '?': '#6b6',
            'sci': ['#ffa', '#fd5', '#fa0'],
            'help': ['#a66', '#a00']
        }

        self.button_objs = {}
        self.main_buttons = []  # Trying to keep track of all buttons
        self.main_labels = []
        # Entry field for RPN expression
        self.entry = tk.Entry(self, font=("Lucida Sans Unicode", 14),
                              width=25, borderwidth=1, relief="solid")
        self.main_labels.append(self.entry)
        # Show the stack
        self.rpn.stack_label = tk.Label(self, text="Stack: []",
                                        font=("Lucida Sans Unicode", 12),
                                        width=30, height=1, anchor="e")
        self.main_labels.append(self.rpn.stack_label)
        # Show input history
        self.history_label = tk.Label(self, text="History: []",
                                      font=("Lucida Sans Unicode", 12),
                                      width=30, height=1, anchor="e")
        self.main_labels.append(self.history_label)
        # "Clear" button to clear the input
        self.clear_button = tk.Button(self, text="Clear",
                                      font=("Lucida Sans Unicode", 14),
                                      width=6, height=1,
                                      bg=self.colors["Clear"],
                                      # command=self.clear,
                                       command=lambda: self.on_button_click("Clear"),
                                      )
        self.main_buttons.append(self.clear_button)
        # "Enter" button to add current value to the stack
        self.enter_button = tk.Button(self, text="Enter",
                                      font=("Lucida Sans Unicode", 14),
                                      width=6, height=1,
                                      bg=self.colors["Enter"],
                                      # command=self.process_input,
                                       command=lambda: self.on_button_click("Enter"),
                                      )
        self.main_buttons.append(self.enter_button)
        # "Help" button to clear the input
        self.help_button = tk.Button(self, text="?",
                                     font=("Lucida Sans Unicode", 14),
                                     width=2, height=1,
                                     bg=self.colors['help'][0],
                                     command=self.activate_help)
        self.main_buttons.append(self.help_button)
        # Set layout
        # self.layout = tk.StringVar()
        # self.layout.set("small")
        self.layout = 'small'  # 'small', 'wide'
        self.create_button_layout(self.layout)

        # Menu
        menubar = tk.Menu()
        self.config(menu=menubar)
        # Create a 'Settings' menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Fairly square", command=lambda: self.create_button_layout('small'))
        settings_menu.add_command(label="Wide and nerdy", command=lambda: self.create_button_layout('wide'))

    # def set_option(self, option):
    #     # Update the selected_option variable when a menu item is clicked
    #     self.selected_option.set(f"Selected: {option}")
    #     # Optionally, display a message box when an option is selected
    #     messagebox.showinfo("Option Selected", f"You selected {option}")

    # def update_geometry(self, layout):
    #     if layout == 'small':
    #         self.geometry("330x360")
    #     else:
    #         self.geometry("590x330")
    #     self.update_idletasks()
    #     # time.sleep(1)
    #     # self.after_idle(self.create_button_layout(layout))

    def create_button_layout(self, layout):
        """Set up button layout based on the selected layout
        ('small' or 'wide')."""
        self.layout = layout
        if layout == 'small':
            self.geometry("330x360")

            self.buttons = [('\u221a', 3, 3, self.colors['op1']),  # root
                            ('sci', 3, 4, '#ffa'),
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
            self.entry.config(width=25)
            self.rpn.stack_label_grid = (1, 0, 5, '')
            self.rpn.stack_label.config(width=30)
            self.history_label_grid = (2, 0, 5, '')
            self.history_label.config(width=30)
            self.clear_button_grid = (3, 0, 2, 'w')
            self.clear_button.config(width=6)
            self.enter_button_grid = (3, 1, 2, 'e')
            self.enter_button.config(width=6)
            self.help_button_grid = (3, 1, 1, '')
            self.help_button.config(width=2)

        elif layout == 'wide':
            self.geometry("590x330")

            # Wide layout (buttons rearranged for a wider view)
            self.buttons = [('7', 4, 4, self.colors['digit']),
                            ('8', 4, 5, self.colors['digit']),
                            ('9', 4, 6, self.colors['digit']),
                            ('/', 4, 7, self.colors['op2']),
                            ('\u03c0', 6, 0, self.colors['number']),  # pi(?)
                            ('4', 5, 4, self.colors['digit']),
                            ('5', 5, 5, self.colors['digit']),
                            ('6', 5, 6, self.colors['digit']),
                            ('\u00d7', 5, 7, self.colors['op2']),  # x
                            ('%', 6, 8, self.colors['op2']),
                            ('1', 6, 4, self.colors['digit']),
                            ('2', 6, 5, self.colors['digit']),
                            ('3', 6, 6, self.colors['digit']),
                            ('-', 6, 7, self.colors['op2']),
                            ('\u00f7', 7, 8, self.colors['op2']),  # div
                            ('0', 7, 5, self.colors['digit']),
                            ('(-)', 7, 4, self.colors['digit']),
                            ('.', 7, 6, self.colors['digit']),
                            ('+', 7, 7, self.colors['op2']),
                            ('^', 5, 8, self.colors['op2']),
                            ('\u221a', 4, 1, self.colors['op1']),  # root
                            # Adding more buttons in wide view
                            # ('n√', 4, 2, self.colors['op2']),
                            ('Rand', 3, 0, self.colors['number']),
                            ('=', 3, 1, self.colors['op1']),
                            ('!', 3, 2, self.colors['op1']),
                            ('1/x', 3, 3, self.colors['op1']),
                            ('\u03c6', 4, 0, self.colors['number']),  # phi
                            ('n\u221a', 4, 2, self.colors['op2']),  # nth root
                            ('2^x', 4, 3, self.colors['op1']),
                            ('e', 5, 0, self.colors['number']),
                            ('ln', 5, 1, self.colors['op1']),
                            ('log', 5, 2, self.colors['op1']),
                            ('lg2', 5, 3, self.colors['op1']),
                            ('sin', 6, 1, self.colors['op1']),
                            ('cos', 6, 2, self.colors['op1']),
                            ('tan', 6, 3, self.colors['op1']),
                            ('\u03c4', 7, 0, self.colors['number']),  # tau
                            ('asin', 7, 1, self.colors['op1']),
                            ('acos', 7, 2, self.colors['op1']),
                            ('atan', 7, 3, self.colors['op1']),
                            ('\u2295', 4, 8, self.colors['op2'])
                            ]

            # Set postion, size and shape for special buttons and fields
            self.clear_button_grid = (3, 6, 2, '')
            self.clear_button.config(width=10)
            self.enter_button_grid = (3, 4, 2, '')
            self.enter_button.config(width=10)
            self.help_button_grid = (3, 8, 1, '')
            self.help_button.config(width=4)
            self.entry_grid = (0, 0, 3, '')
            self.entry.config(width=15)
            self.rpn.stack_label_grid = (0, 3, 6, '')
            self.rpn.stack_label.config(width=36)
            self.history_label_grid = (2, 0, 9, 'e')
            self.history_label.config(width=55)

        else:
            print(f"Invalid layout {layout}")
            return

        # Update geometry etc
        # self.update_geometry(layout)
        self.update_idletasks()
        # time.sleep(1)

        # Create the buttons for the number pad and operators with colors
        self.forget_grid()
        self.update_idletasks()
        for (text, row, col, color) in self.buttons:
            button = tk.Button(self, text=text,
                               font=("Lucida Sans Unicode", 14),
                               width=4, height=1, bg=color,
                               command=self.create_button_handler(text))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.button_objs[text] = button

        # Change font on the greek letter buttons
        # self.button_objs['π'].config(font=("Symbol", 14))
        self.update_buttons()

        # Reposition Clear, Enter, and Help buttons
        self.clear_button.grid(row=self.clear_button_grid[0],
                               column=self.clear_button_grid[1],
                               columnspan=self.clear_button_grid[2],
                               pady=5,
                               sticky=self.clear_button_grid[3])
        self.enter_button.grid(row=self.enter_button_grid[0],
                               column=self.enter_button_grid[1],
                               columnspan=self.enter_button_grid[2],
                               pady=5,
                               sticky=self.enter_button_grid[3])
        self.help_button.grid(row=self.help_button_grid[0],
                              column=self.help_button_grid[1],
                              pady=5)

        # Reposition Entry, Stack and History labels
        self.entry.grid(row=self.entry_grid[0], column=self.entry_grid[1],
                        columnspan=self.entry_grid[2],
                        pady=5,
                        sticky=self.entry_grid[3])
        self.rpn.stack_label.grid(row=self.rpn.stack_label_grid[0],
                                  column=self.rpn.stack_label_grid[1],
                                  columnspan=self.rpn.stack_label_grid[2],
                                  pady=5,
                                  sticky=self.history_label_grid[3])
        self.history_label.grid(row=self.history_label_grid[0],
                                column=self.history_label_grid[1],
                                columnspan=self.history_label_grid[2],
                                pady=5,
                                sticky=self.history_label_grid[3])

    def forget_grid(self):  # keep in gui
        """Clear any previous buttons from the grid."""
        # print(f"{len(self.button_objs)=}")
        for key, button in self.button_objs.items():
            # print(f"Forgetting button obj {button}, {key} ")
            button.grid_forget()
        # for thing in [self.enter_button, self.clear_button, self.help_button]:
        #     thing.grid_forget()
        #     print(f"Forgetting thing {thing}")
        for button in self.main_buttons:
            # print(f"Forgetting main button {button}, {button.cget('text')}")
            button.grid_forget()
        # print(f"{len(self.button_objs)=}")

        self.button_objs.clear()
        # print(f"{len(self.button_objs)=}")
        for label in self.main_labels:
            # print(f"Forgetting label {label}")
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
            if self.button_objs[k].cget('text') in {'\u03c0', '\u03c4', '\u03c6'}:
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
            # Toggle the sci mode when the "sci" button is clicked
            self.toggle_sci_mode()
        elif button_text == "Enter":
            self.process_input()
        elif button_text == "Clear":
            self.clear()
        else:
            # print("not sci")
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
        if self.entry.get().strip():
            # There is something in the entry field; clear this
            self.entry.delete(0, tk.END)
        elif self.rpn.stack:
            # Entry field is empty, stack has something in it
            self.rpn.stack.clear()
            self.update_display()
        elif self.history:
            # Stack is also empty, history has something in it
            self.history.clear()
            self.update_display()
        else:
            pass

    def update_display(self):
        """Update the stack display label."""
        # Update stack display
        self.rpn.stack_label.config(text=f"Stack: {self.rpn.stack}")
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
            self.entry.insert(tk.END, "Click for help.")  # Display help mode

    def deactivate_help(self):
        self.help_button.config(bg=self.colors['help'][0])
        self.entry.delete(0, tk.END)
        self.help_mode = False


if __name__ == "__main__":
    rpn_calc = RPN()  # Create an instance of the Calculator class
    app = CalculatorGUI(rpn_calc)  # Pass the calculator object to the GUI
    app.mainloop()
