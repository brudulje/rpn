import tkinter as tk
from tkinter import messagebox
import math
import random
import re

class RPNCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPN Calculator")
        self.geometry("330x400")
        self.stack = []       # Stack for RPN calculation
        self.history = []        # List of input

                        # '^': '=',  # Joke
        self.operator_2 = {'+', '-', '\u00d7',  # times
                           '/', '^', '\u00f7',  # int div
                           '%','n\u221a',  # nth root
                           '\u2295',  # circled pluss
                           }

        # ÷ \u00f7 pi \u03c0 tau \u03c4 √ \u221a
        self.operator_1 = {'\u221a',  # root
                           'sin', 'cos', 'tan',
                           'asin', 'acos', 'atan',
                           'ln', 'log', 'lg2',
                           '1/x', '!', '='}
        self.operator_0 = {'\u03c0', '\u03c4', '\u03c6', 'e', 'Rand'}
        # pi, tau, phi, e
        self.operators = self.operator_0 | self.operator_1 | self.operator_2

        # Regex magic to allow operators to be entered together with the
        # last number before the operator
        self.operator_pattern = r'^[+-]?\d*\.?\d+([' + '|'\
            .join(map(re.escape, self.operators)) + r'])'

        self.sci_mode = 0  # Initially not in scientific mode

        # Entry field for RPN expression
        self.entry = tk.Entry(self, font=("Lucida Sans Unicode", 14),
                              width=25, borderwidth=1, relief="solid")
        self.entry.grid(row=0, column=0, columnspan=5, padx=0, pady=6)

        # Shoe the stack
        self.stack_label = tk.Label(self, text="Stack: []",
                                    font=("Lucida Sans Unicode", 12),
                                    width=30, height=2, anchor="e")
        self.stack_label.grid(row=1, column=0, columnspan=5, padx=1, pady=5)

        # Shoe input history
        self.history_label = tk.Label(self, text="History: []",
                                      font=("Lucida Sans Unicode", 12),
                                      width=30, height=2, anchor="e")
        self.history_label.grid(row=2, column=0, columnspan=5,
                                padx=1, pady=2)

        # "Clear" button to clear the input
        self.clear_button = tk.Button(self, text="Clear",
                                      font=("Lucida Sans Unicode", 14),
                                      width=4, height=1, bg='lightgray',
                                      command=self.clear)
        self.clear_button.grid(row=3, column=0, pady=5)

        # Define button layout and colors
        self.buttons = [
            ('\u221a', 3, 3, 'lightgreen'),
            ('sci', 3, 4, '#ffa'),
            ('7', 4, 0, 'lightblue'), ('8', 4, 1, 'lightblue'),
            ('9', 4, 2, 'lightblue'), ('/', 4, 3, 'lightgreen'),
            ('\u03c0', 4, 4, 'lightgreen'),
            ('4', 5, 0, 'lightblue'), ('5', 5, 1, 'lightblue'),
            ('6', 5, 2, 'lightblue'), ('\u00d7', 5, 3, 'lightgreen'),
            ('%', 5, 4, 'lightgreen'),
            ('1', 6, 0, 'lightblue'), ('2', 6, 1, 'lightblue'),
            ('3', 6, 2, 'lightblue'), ('-', 6, 3, 'lightgreen'),
            ('\u00f7', 6, 4, 'lightgreen'),
            ('0', 7, 0, 'lightblue'), ('.', 7, 1, 'lightblue'),
            ('+', 7, 3, 'lightgreen'), ('^', 7, 4, 'lightgreen')
            ]

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

        # "Enter" button to add current value to the stack
        self.enter_button = tk.Button(self, text="Enter",
                                      font=("Lucida Sans Unicode", 14),
                                      width=4, height=1, bg='darkgray',
                                      command=self.process_input)
        self.enter_button.grid(row=7, column=2, pady=5)

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
        except IndexError:
            raise ValueError("Insufficient operands for the operator.")

        # Perform the operation based on the operator
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '\u00d7':  # times
            result = operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ValueError("Division by zero is undefined.")
            result = operand1 / operand2
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
        else:
            raise ValueError(f"Unknown operator {operator}.")

        return result

    def evaluate_one(self, expression):
        """Operate operators taking a single operand."""
        # {'\u221a', 'sin', 'cos', 'tan', 'ln', 'log', 'x^2', '1/x'}
        operand = expression[0]
        operator = expression[1]
        if operator == '\u221a':
            if operand < 0:
                raise ValueError("Root of negative numbers not supported.")
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
            return 1 / operand
        elif operator == 'asin':
            return math.asin(operand)
        elif operator == 'acos':
            return math.acos(operand)
        elif operator == 'atan':
            return math.atan(operand)
        elif operator == '!':
            return math.factorial(operand)
        elif operator == '=':  # Rounds last operand to an int
            return int(operand)
        # elif operator == 'x^2':  # Depricated
        #     return operand ** 2

        else:
            raise ValueError(f"Unknown operator {operator}.")

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
            raise ValueError(f"Unknown operator {text}.")

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
                        '^': '=',  # Joke
                        }
                       ]

        # Change button labels to scientific mode and update handlers
        for k, v in sci_layouts[self.sci_mode].items():
            self.button_objs[k].config(text=v)
            self.button_objs[k].config(command=self.create_button_handler(v))

        # Update sci button bg color
        self.button_objs['sci'].config(bg=sci_button_colors[self.sci_mode])

    def on_button_click(self, value):
        """Handle button click: add value to the input field
        and trigger calculation."""
        if value == 'sci':
            # Toggle the sci mode when the "sci" button is clicked
            self.toggle_sci_mode()
        else:
            # For operators, we insert the operator and immediately calculate
            if value in self.operators:
                # For operators like '+', '-', '\u00d7', '/', etc.
                self.entry.insert(tk.END, value)
                self.process_input()  # Automatically trigger calculation
            else:
                # For numbers, just insert them into the entry field
                self.entry.insert(tk.END, value)


    def process_operator(self, operator, operand_count, eval_function=None):
        """
        Helper function to handle the common tasks for processing operators.
        """
        self.stack.append(operator)
        self.entry.delete(0, tk.END)  # Clear the entry field after adding operator

        if eval_function:
            result = eval_function(self.stack[-operand_count:])
            self.stack = self.stack[:-operand_count]  # Remove the operands from the stack
            self.stack.append(result)


    def process_number(self, current_text):
        """
        Helper function to handle the processing of a number.
        """
        try:
            # Try to convert to integer or float
            value = int(current_text) if "." not in current_text else float(current_text)
            self.stack.append(value)
            self.entry.delete(0, tk.END)  # Clear the entry field after adding to stack
        except ValueError:
            messagebox.showerror("Error", f"Invalid number: {current_text}")

    def process_input(self):
        """Add the current value (operand or operator) to the stack when Enter is pressed."""
        current_text = self.entry.get().strip()
        self.history.append(current_text)

        if current_text:

            # Check if the current_text matches the operator pattern (number + operator)
            match = re.match(self.operator_pattern, current_text)

            if match:
                # Extract the number and operator from the matched string
                number = match.group(0)[:-len(match.group(1))]  # Everything except the operator
                operator = match.group(1)  # The operator part

                # Add number to stack
                self.process_number(number)

                # Add operator to stack and evaluate
                if operator in self.operator_2:
                    self.process_operator(operator, 3, self.evaluate_two)
                elif operator in self.operator_1:
                    self.process_operator(operator, 2, self.evaluate_one)
                elif operator in self.operator_0:
                    result = self.evaluate_zero(operator)
                    self.stack.append(result)
                    self.entry.delete(0, tk.END)  # Clear the entry field after adding to stack

            elif current_text in self.operator_2:
                # Add operator to stack and evaluate immediately
                self.process_operator(current_text, 3, self.evaluate_two)
            elif current_text in self.operator_1:
                # Add single operand operator to stack and evaluate
                self.process_operator(current_text, 2, self.evaluate_one)
            elif current_text in self.operator_0:
                # Zero-operand operator, just evaluate
                result = self.evaluate_zero(current_text)
                self.stack.append(result)
                self.entry.delete(0, tk.END)  # Clear the entry field after adding to stack
            else:
                # Process a number
                self.process_number(current_text)

            # Always update the stack_label to show the current stack
            self.update_display()

        else:
            messagebox.showerror("Error", "Please enter a valid number or operator.")

    # def process_input(self):#, current_text):
    # # def add_to_stack(self):
    #     """Add the current value (operand or operator) to the stack
    #     when Enter is pressed."""
    #     current_text = self.entry.get().strip()
    #     print(current_text)
    #     self.history.append(current_text)
    #     if current_text:
    #         print("Yes, ", current_text)
    #         if current_text in self.operator_2:
    #             # Add operator to stack and evaluate immediately
    #             self.process_operator(current_text, 3, self.evaluate_two)
    #         elif current_text in self.operator_1:
    #             # Add single operand operator to stack and evaluate
    #             self.process_operator(current_text, 2, self.evaluate_one)
    #         elif current_text in self.operator_0:
    #             # Zero-operand operator, just evaluate
    #             result = self.evaluate_zero(current_text)
    #             self.stack.append(result)
    #             self.entry.delete(0, tk.END)  # Clear the entry field after adding to stack
    #         else:
    #             print("Number")
    #             # Process a number
    #             self.process_number(current_text)
    #         # Always update the stack_label to show the current stack
    #         self.update_display()
    #     else:
    #         messagebox.showerror("Error", "Please enter a valid number or operator.")


        # if current_text:
        #     if current_text in self.operator_2:
        #         # Add operator to stack
        #         self.stack.append(current_text)
        #         # Clear entry field after adding operator
        #         self.entry.delete(0, tk.END)
        #         # Evaluate immediately after adding an operator
        #         result = self.evaluate_two(self.stack[-3:])
        #         # self.stack= self.stack[:-3].append(result)  # Nope!
        #         self.stack = self.stack[:-3]
        #         self.stack.append(result)
        #     elif current_text in self.operator_1:
        #         # Single operand operators
        #         self.stack.append(current_text)
        #         # Clear entry field after adding operator
        #         self.entry.delete(0, tk.END)
        #         result = self.evaluate_one(self.stack[-2:])
        #         self.stack = self.stack[:-2]
        #         self.stack.append(result)
        #     elif current_text in self.operator_0:
        #         result = self.evaluate_zero(current_text)
        #         # Clear the entry field after adding to stack
        #         self.entry.delete(0, tk.END)
        #         # self.stack = self.stack[:-1]
        #         self.stack.append(result)
        #     else:  # Should be a number
        #         try:
        #             if "." not in current_text:
        #                 # Should be an int
        #                 value = int(current_text)
        #             else:
        #                 # Try to convert the text to a float
        #                 value = float(current_text)
        #             #  and add it to the stack
        #             self.stack.append(value)
        #             # Clear the entry field after adding to stack
        #             self.entry.delete(0, tk.END)
        #         except ValueError:
        #             messagebox.showerror("Error", f"Invalid number: {current_text}")


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


# Create the GUI application
if __name__ == "__main__":
    app = RPNCalculator()
    app.mainloop()
