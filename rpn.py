import tkinter as tk
from tkinter import messagebox
import math
import random
import re


class RPNCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPN Calculator")
        self.geometry("330x360")
        self.stack = []  # Stack for RPN calculation
        self.history = []  # List of input

        self.operator_2 = {'+', '-', '\u00d7',  # times
                           '/', '^', '\u00f7',  # int div
                           '%', 'n\u221a',  # nth root
                           'E', '\u2295',  # circled pluss
                           }

        self.operator_1 = {'\u221a',  # root
                           'sin', 'cos', 'tan',
                           'asin', 'acos', 'atan',
                           'ln', 'log', 'lg2',
                           '1/x', '!', '=', '2^x'}
        self.operator_0 = {'\u03c0', '\u03c4', '\u03c6', 'e', 'Rand'}
        # pi, tau, phi, e
        self.operators = self.operator_0 | self.operator_1 | self.operator_2

        # Regex magic to allow operators to be entered together with the
        # last number before the operator
        self.sorted_operators = sorted(self.operators, key=len, reverse=True)
        # Create a regex pattern to match the longest operator at the end of the string
        pattern = '|'.join(re.escape(op) for op in self.sorted_operators)
        # Match the operator only at the end and ensure there is something before it
        self.pattern = f"^(.*?)(?={pattern})({pattern})$"

        # Dictionary of help texts for each button
        self.help_texts = {
            '.': "Decimal point. Separates the whole number from the fraction.",
            '0': "0; Zero, the first digit and the basis of positional notation.",
            '1': "1; First and foremost. Number one.",
            '2': "2; Never first, but close.",
            '3': "3; First odd prime.",
            '4': "4; Four in a row.",
            '5': "5; Five is a handful.",
            '6': "6; Six. First rectangular number.",
            '7': "7; Seven. An excellent choise.",
            '8': "8; Eight. The first digit in alphabetical order.",
            '9': "9; Nine. First odd square.",
            'π': "Pi is the circumference of a circle divided by its diameter.",
            '\u03c4': "Tau is the circumference of a circle divided by its radius.",
            'e': "Euler's number (e) is a mathematical constant approximately equal to 2.71828.",
            '\u03c6': "Phi is the golden ratio. 1 / phi = phi - 1.",
            '+': "Addition operator. Adds two numbers.",
            '-': "Subtraction operator. Subtracts the second number from the first.",
            '\u00d7': "Multiplication operator. Multiplies two numbers.",
            '/': "Division operator. Divides the first number by the second.",
            '^': "Exponentiation operator. Raises the first number to the power of the second.",
            '÷': "Integer division. Returns the integer part after division.",
            '%': "Modulus operator. Returns the remainder of the division of two numbers.",
            '√': "Square root operator. Returns the square root of a number.",
            'sin': "Sine function. Returns the sine of an angle (in radians).",
            'cos': "Cosine function. Returns the cosine of an angle (in radians).",
            'tan': "Tangent function. Returns the tangent of an angle (in radians).",
            'asin': "Inverse sine function. Returns the inverse of sin.",
            'acos': "Inverse cosine function. Returns the inverse of cos.",
            'atan': "Inverse tangent function. Returns the inverse of tan",
            'ln': "Natural logarithm function. Returns the natural logarithm of a number.",
            'lg2': "Base-2 logarithm function. Returns the logarithm of a number with base 2.",
            'log': "Base-10 logarithm function. Returns the logarithm of a number with base 10.",
            '1/x': "Reciprocal operator. Returns the reciprocal (1 divided by the number).",
            '2^x': "Raise 2 to the power of x.",
            '!': "Factorial function. Returns the factorial of a number.",
            '=': "Rounds the number to the nearest integer.",
            'Rand': "Generates a random number between 0 and 1.",
            'n√': "Nth root operator. Returns the nth root of the first number.",
            '\u2295': "Circled Plus operator. Returns the Euclidean norm (distance) between two numbers.",
            'E': "Scientific notation. x, y, E is x * 10^y.",
            'sci': "Toggle various scientific functions.",
            '?' : "This is the help button. Click this and another button to get help on that other button.",
            # 'Clear': "Clears the input. If no input, clears the stack. If no stack, clears history.",
            # 'Enter': "Transfers your input number to the stack."
        }

        # To track if help mode is active
        self.help_mode = False

        self.sci_mode = 0  # Initially not in scientific mode
        self.colors = {
            'num': 'lightblue',
            'op': 'lightgreen',
            'sci': '#ffa',
            'Clear': 'lightgray',
            'Enter': 'darkgray',
            '?': '#6b6'
            }

        # Entry field for RPN expression
        self.entry = tk.Entry(self, font=("Lucida Sans Unicode", 14),
                              width=25, borderwidth=1, relief="solid")
        self.entry.grid(row=0, column=0, columnspan=5, padx=0, pady=6)

        # Shoe the stack
        self.stack_label = tk.Label(self, text="Stack: []",
                                    font=("Lucida Sans Unicode", 12),
                                    width=30, height=1, anchor="e")
        self.stack_label.grid(row=1, column=0, columnspan=5, padx=1, pady=5)

        # Shoe input history
        self.history_label = tk.Label(self, text="History: []",
                                      font=("Lucida Sans Unicode", 12),
                                      width=30, height=1, anchor="e")
        self.history_label.grid(row=2, column=0, columnspan=5, padx=1, pady=2)

        # "Clear" button to clear the input
        self.clear_button = tk.Button(self, text="Clear",
                                      font=("Lucida Sans Unicode", 14),
                                      width=6, height=1, bg=self.colors["Clear"],
                                      command=self.clear)
        self.clear_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

        # "Enter" button to add current value to the stack
        self.enter_button = tk.Button(self, text="Enter",
                                      font=("Lucida Sans Unicode", 14),
                                      width=6, height=1, bg=self.colors["Enter"],
                                      command=self.process_input)
        self.enter_button.grid(row=3, column=1, columnspan=2, pady=5, sticky="e")

        # "Help" button to clear the input
        self.help_button = tk.Button(self, text="?",
                                     font=("Lucida Sans Unicode", 14),
                                     width=4, height=1, bg=self.colors["?"],#'#6b6',#bg='#5a5',
                                     command=self.activate_help)
        self.help_button.grid(row=7, column=2, pady=5)
###
        # Initially, set layout to 'small'
        self.layout = 'wide'  # Set the layout to 'small' initially ('wide')
        self.create_button_layout(self.layout)


    def create_button_layout(self, layout):
        """Set up button layout based on the selected layout ('small' or 'wide')."""
        if layout == 'small':
            # Small layout (as defined originally)
            self.buttons = [
                ('\u221a', 3, 3, self.colors['op']),
                ('sci', 3, 4, '#ffa'),
                ('7', 4, 0, self.colors['num']), ('8', 4, 1, self.colors['num']),
                ('9', 4, 2, self.colors['num']), ('/', 4, 3, self.colors['op']),
                ('\u03c0', 4, 4, self.colors['op']),
                ('4', 5, 0, self.colors['num']), ('5', 5, 1, self.colors['num']),
                ('6', 5, 2, self.colors['num']), ('\u00d7', 5, 3, self.colors['op']),
                ('%', 5, 4, self.colors['op']),
                ('1', 6, 0, self.colors['num']), ('2', 6, 1, self.colors['num']),
                ('3', 6, 2, self.colors['num']), ('-', 6, 3, self.colors['op']),
                ('\u00f7', 6, 4, self.colors['op']),
                ('0', 7, 0, self.colors['num']), ('.', 7, 1, self.colors['num']),
                ('+', 7, 3, self.colors['op']), ('^', 7, 4, self.colors['op'])
            ]

            self.clear_button_grid = (3, 0, 2, 'w')  # Position for the "Clear" button
            self.enter_button_grid = (3, 1, 2, 'e')  # Position for the "Enter" button
            self.help_button_grid = (7, 2, 1, '')   # Position for the "Help" button
            self.entry_grid = (0, 0, 5, '')
            self.stack_label_grid = (1, 0, 5, '')
            self.history_label_grid = (2, 0, 5, '')

        elif layout == 'wide':
            self.geometry("590x330")

            # Wide layout (buttons rearranged for a wider view)
            self.buttons = [
                ('7', 4, 2, self.colors['num']), ('8', 4, 3, self.colors['num']),
                ('9', 4, 4, self.colors['num']), ('/', 7, 1, self.colors['op']),
                ('\u03c0', 6, 5, self.colors['op']),
                ('4', 5, 2, self.colors['num']), ('5', 5, 3, self.colors['num']),
                ('6', 5, 4, self.colors['num']), ('\u00d7', 6, 1, self.colors['op']),
                ('%', 5, 0, self.colors['op']),
                ('1', 6, 2, self.colors['num']), ('2', 6, 3, self.colors['num']),
                ('3', 6, 4, self.colors['num']), ('-', 5, 1, self.colors['op']),
                ('\u00f7', 7, 0, self.colors['op']),
                ('0', 7, 3, self.colors['num']), ('.', 7, 4, self.colors['num']),
                ('+', 4, 1, self.colors['op']), ('^', 6, 0, self.colors['op']),
                ('\u221a', 4, 6, self.colors['op']), #('sci', 7, 1, '#ffa'),
                ('n√', 4, 7, self.colors['op'])
            ]

            # In wide layout, the Clear, Enter, and Help buttons are repositioned
            self.clear_button_grid = (3, 1, 2, '')  # Position for the "Clear" button
            self.clear_button.config(width=10)
            self.enter_button_grid = (3, 3, 2, '')  # Position for the "Enter" button
            self.enter_button.config(width=10)
            self.help_button_grid = (3, 0, 1, '')   # Position for the "Help" button
            self.entry_grid = (0, 0, 3, '')
            self.entry.config(width=15)
            self.stack_label_grid = (0, 3, 6, '')
            self.stack_label.config(width=36)
            self.history_label_grid = (2, 0, 9, 'e')
            self.history_label.config(width=55)

            # New buttons in the wide layout (just an example of adding buttons)
            self.additional_buttons = [
                ('Rand', 3, 5, self.colors['op']),
                ('=', 3, 6, self.colors['op']),
                ('!', 3, 7, self.colors['op']),
                ('1/x', 3, 8, self.colors['op']),
                ('\u03c6', 4, 5, self.colors['op']),  # phi
                # ('\u221a', 4, 6, self.colors['op']),  # root
                ('n\u221a', 4, 7, self.colors['op']),  # nth root
                ('2^x', 4, 8, self.colors['op']),  # TODO: implement
                ('e', 5, 5, self.colors['op']),
                ('ln', 5, 6, self.colors['op']),
                ('log', 5, 7, self.colors['op']),
                ('lg2', 5, 8, self.colors['op']),
                ('sin', 6, 6, self.colors['op']),
                ('cos', 6, 7, self.colors['op']),
                ('tan', 6, 8, self.colors['op']),
                ('\u03c4', 7, 5, self.colors['op']),  # tau
                ('asin', 7, 6, self.colors['op']),
                ('acos', 7, 7, self.colors['op']),
                ('atan', 7, 8, self.colors['op']),
                ('\u2295', 4, 0, self.colors['op']),
                ('E', 7, 2, self.colors['op']),
            ]

        else:
            print("Invalid layout")
            return
###
        # # Define button layout and colors
        # self.buttons = [
        #     ('\u221a', 3, 3, 'lightgreen'),
        #     ('sci', 3, 4, '#ffa'),
        #     ('7', 4, 0, 'lightblue'), ('8', 4, 1, 'lightblue'),
        #     ('9', 4, 2, 'lightblue'), ('/', 4, 3, 'lightgreen'),
        #     ('\u03c0', 4, 4, 'lightgreen'),
        #     ('4', 5, 0, 'lightblue'), ('5', 5, 1, 'lightblue'),
        #     ('6', 5, 2, 'lightblue'), ('\u00d7', 5, 3, 'lightgreen'),
        #     ('%', 5, 4, 'lightgreen'),
        #     ('1', 6, 0, 'lightblue'), ('2', 6, 1, 'lightblue'),
        #     ('3', 6, 2, 'lightblue'), ('-', 6, 3, 'lightgreen'),
        #     ('\u00f7', 6, 4, 'lightgreen'),
        #     ('0', 7, 0, 'lightblue'), ('.', 7, 1, 'lightblue'),
        #     ('+', 7, 3, 'lightgreen'), ('^', 7, 4, 'lightgreen')
        #     ]
       # Clear any previous buttons and re-create the new layout
        # self.clear_button_objs()

        # Create the buttons for the number pad and operators with colors
        self.button_objs = {}
        for (text, row, col, color) in self.buttons:
            button = tk.Button(self, text=text,
                               font=("Lucida Sans Unicode", 14),
                               width=4, height=1, bg=color,
                               command=self.create_button_handler(text))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.button_objs[text] = button

        # Change font on the pi button
        self.button_objs['π'].config(font=("Symbol", 14))

        # Create the additional buttons for the 'wide' layout
        if layout == 'wide':
            for (text, row, col, color) in self.additional_buttons:
                button = tk.Button(self, text=text,
                                   font=("Lucida Sans Unicode", 14),
                                   width=4, height=1, bg=color,
                                   command=self.create_button_handler(text))
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                self.button_objs[text] = button

        # Reposition Clear, Enter, and Help buttons
        self.clear_button.grid(row=self.clear_button_grid[0], column=self.clear_button_grid[1],
                               columnspan=self.clear_button_grid[2], pady=5, sticky=self.clear_button_grid[3])
        self.enter_button.grid(row=self.enter_button_grid[0], column=self.enter_button_grid[1],
                               columnspan=self.enter_button_grid[2], pady=5, sticky=self.enter_button_grid[3])
        self.help_button.grid(row=self.help_button_grid[0], column=self.help_button_grid[1],
                              pady=5)
        self.entry.grid(row=self.entry_grid[0], column=self.entry_grid[1],
                               columnspan=self.entry_grid[2], pady=5, sticky=self.entry_grid[3])
        self.stack_label.grid(row=self.stack_label_grid[0], column=self.stack_label_grid[1],
                               columnspan=self.stack_label_grid[2], pady=5, sticky=self.history_label_grid[3])
        self.history_label.grid(row=self.history_label_grid[0], column=self.history_label_grid[1],
                               columnspan=self.history_label_grid[2], pady=5, sticky=self.history_label_grid[3])


    def clear_button_objs(self):
        """Clear any previous buttons from the grid."""
        for button in self.button_objs.values():
            button.grid_forget()

        self.button_objs.clear()



    def create_button_handler(self, text):
        """Returns a function that calls
        self.on_button_click with the button text."""
        def handler():
            self.on_button_click(text)
        return handler

    def evaluate_two(self, expression):
        """Operate operators taking two operands."""
        try:
            operand1 = expression[0]
            operand2 = expression[1]
            operator = expression[2]  # Operator
        # except (ValueError, IndexError):
        #     messagebox.showerror("Error", f"Too few arguments to {expression}.")

        # try:
            _ = float(operand1)
            _ = float(operand2)
        except (ValueError, TypeError, IndexError):
            # messagebox.showerror("Error", f"{operand1} and {operand2} are not numbers.")
            messagebox.showerror("Error", f"Can't figure out how to handle {expression}.")
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
                # # raise ValueError("Division by zero is undefined.")
                # result = operand1 / operand2
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
            # raise ValueError(f"Unknown operator {operator}.")
            messagebox.showerror("Error", f"Unknown operator {operator}.")

        return result

    def evaluate_one(self, expression):
        """Operate operators taking a single operand."""
        # {'\u221a', 'sin', 'cos', 'tan', 'ln', 'log', 'x^2', '1/x'}
        try:
            operand = expression[0]
            operator = expression[1]
        except IndexError:
            messagebox.showerror("Error", f"Too few arguments to {expression}.")
            return None

        if operator == '\u221a':
            if operand < 0:
                # raise ValueError("Root of negative numbers not supported.")
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
                                 f"Unknown operator {operator}.")

    def evaluate_zero(self, text):
        # {'\u03c0', '\u03c4', 'e'}
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
                                 f"Unknown operator {text}.")

    def toggle_sci_mode(self):
        """Toggle between scientific and normal mode."""
        # There are 3 modes.
        self.sci_mode = (self.sci_mode + 1) % 3  # Change to next mode

        sci_button_colors = ['#ffa', '#fd6', '#fa0']
        # sci_button_texts = ['Sci', 'sCi', 'scI']  # No, looks ugly
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
                        '%': 'e',
                        '÷': 'ln',
                        '^': 'log',
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

        # Update sci button bg color
        self.button_objs['sci'].config(bg=sci_button_colors[self.sci_mode])

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
                self.entry.insert(tk.END, button_text)

    def process_operator(self, operator, operand_count, eval_function=None):
        """
        Helper function to handle the common tasks for processing operators.
        """
        self.stack.append(operator)
        # Clear the entry field after adding operator
        self.entry.delete(0, tk.END)

        if eval_function:
            result = eval_function(self.stack[-operand_count:])
            # # Remove the operands from the stack
            # self.stack = self.stack[:-operand_count]
            if result is not None:
            # Remove the operands from the stack only if calculation is good
                self.stack = self.stack[:-operand_count]
                self.stack.append(result)
            else:
                 # Remove faild operator from stack
                 self.stack = self.stack[:-1]

    def process_number(self, current_text):
        """
        Helper function to handle the processing of a number.
        """
        try:
            # Try to convert to integer or float
            # value = int(current_text) if "." not in current_text
            # else float(current_text)
            if "." not in current_text:
                value = int(current_text)
            else:
                value = float(current_text)
            self.stack.append(value)
            # Clear the entry field after adding to stack
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", f"Invalid number: {current_text}")

    def process_input(self):
        """Add the current value (operand or operator) to the stack
        when Enter is pressed."""
        current_text = self.entry.get().strip()
        self.history.append(current_text)

        if current_text:

            match = re.search(self.pattern, current_text)
            # Number and operator entered together.
            if match and match.group(1) and match.group(2):
                number = match.group(1)
                # Add number to stack
                self.process_number(number)
                # operator = match.group(2)  # Send operator on to be sorted
                current_text = match.group(2)

            if current_text in self.operator_2:
                # Add operator to stack and evaluate immediately
                self.process_operator(current_text, 3, self.evaluate_two)
            elif current_text in self.operator_1:
                # Add single operand operator to stack and evaluate
                self.process_operator(current_text, 2, self.evaluate_one)
            elif current_text in self.operator_0:
                # Zero-operand operator, just evaluate
                result = self.evaluate_zero(current_text)
                self.stack.append(result)
                # Clear the entry field after adding to stack
                self.entry.delete(0, tk.END)
            else:
                # Process a number
                self.process_number(current_text)

            # Always update the stack_label to show the current stack
            self.update_display()

        else:
            messagebox.showerror("Error",
                                 "Please enter a valid number or operator.")

    def clear(self):
        """Clear various variables when the Clear button is pressed."""
        # print(bool(self.stack), bool(self.history))
        if self.entry.get().strip():
            # There is something in the entry field; clear this
            self.entry.delete(0, tk.END)
        elif self.stack:
            # Entry field is empty, stack has something in it
            self.stack.clear()
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
        self.stack_label.config(text=f"Stack: {self.stack}")
        # Update stack display
        self.history_label.config(text=f"History: {self.history}")

    def activate_help(self):
        """Activate help mode and wait for user to click a button."""
        if self.help_mode:
            # Provide help on help button
            help_text = self.help_texts.get('?', "No help available for this button.")
            messagebox.showinfo("Help", help_text)
            self.deactivate_help()
        else:
            self.help_mode = True
            # set color '#0a6'
            self.help_button.config(bg='#080')  # 'lightgreen #9e9
            self.entry.delete(0, tk.END)  # Clear the entry field to indicate help mode
            self.entry.insert(tk.END, "Click a button for help.")  # Display help mode message

    def deactivate_help(self):
        self.help_button.config(bg='#6b6')
        self.entry.delete(0, tk.END)
        self.help_mode = False

# Create the GUI application
if __name__ == "__main__":
    app = RPNCalculator()
    app.mainloop()
