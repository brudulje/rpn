import tkinter as tk
from tkinter import messagebox
import math


class RPNCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPN Calculator")
        self.geometry("320x380")
        self.stack = []       # Stack for RPN calculation
        self.history = []        # List of input

        self.operator_2 = {'+', '-', '*', '/', '^', '\u00f7', '%','n\u221a'}
        # ÷ \u00f7 pi \u03c0 tau \u03c4 √ \u221a
        self.operator_1 = {'\u221a', 'sin', 'cos', 'tan',
                           'ln', 'log', '1/x'}
        self.operator_0 = {'\u03c0', '\u03c4', 'e'}
        self.operators = self.operator_0 | self.operator_1 | self.operator_2

        self.sci_mode = False  # Initially not in scientific mode

        # Entry field for RPN expression
        self.entry = tk.Entry(self, font=("Arial", 14),
                              width=10, borderwidth=1, relief="solid")
        self.entry.grid(row=0, column=0, columnspan=2, padx=0, pady=6)

        # Define button layout and colors
        self.buttons = [
            ('\u221a', 2, 3, 'lightgreen'),
            ('sci', 2, 4, 'lightyellow'),
            ('7', 3, 0, 'lightblue'), ('8', 3, 1, 'lightblue'),
            ('9', 3, 2, 'lightblue'), ('/', 3, 3, 'lightgreen'),
            ('\u03c0', 3, 4, 'lightgreen'),
            ('4', 4, 0, 'lightblue'), ('5', 4, 1, 'lightblue'),
            ('6', 4, 2, 'lightblue'), ('*', 4, 3, 'lightgreen'),
            ('%', 4, 4, 'lightgreen'),
            ('1', 5, 0, 'lightblue'), ('2', 5, 1, 'lightblue'),
            ('3', 5, 2, 'lightblue'), ('-', 5, 3, 'lightgreen'),
            ('\u00f7', 5, 4, 'lightgreen'),
            ('0', 6, 0, 'lightblue'), ('.', 6, 1, 'lightblue'),
            ('+', 6, 3, 'lightgreen'), ('^', 6, 4, 'lightgreen')
            ]

        # Create the buttons for the number pad and operators with colors
        self.button_objs = {}
        for (text, row, col, color) in self.buttons:
            button = tk.Button(self, text=text, font=("Arial", 14),
                               width=4, height=1, bg=color,
                               command=self.create_button_handler(text))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.button_objs[text] = button

        # "Enter" button to add current value to the stack
        self.enter_button = tk.Button(self, text="Enter", font=("Arial", 14),
                                      width=4, height=1, bg='darkgray',
                                      command=self.add_to_stack)
        self.enter_button.grid(row=6, column=2, pady=5)

        # "Clear" button to clear the input
        self.clear_button = tk.Button(self, text="Clear", font=("Arial", 14),
                                      width=4, height=1, bg='lightgray',
                                      command=self.clear)
        self.clear_button.grid(row=2, column=0, pady=5)

        self.stack_label = tk.Label(self, text="[]", font=("Arial", 12),
                                    width=15, height=2, anchor="w")
        self.stack_label.grid(row=0, column=2, columnspan=3, padx=1, pady=5)

        self.history_label = tk.Label(self, text="[]", font=("Arial", 12),
                                      width=32, height=2, anchor="e")
        self.history_label.grid(row=1, column=0, columnspan=5,
                                padx=1, pady=2)

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
        elif operator == '*':
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
        elif operator == 'log':
            return math.log10(operand)
        elif operator == '1/x':
            return 1 / operand
        # elif operator == 'x^2':
        #     return operand ** 2

        else:
            raise ValueError(f"Unknown operator {operator}.")

    def evaluate_zero(self, text):
        # {'\u03c0', '\u03c4', 'e'}
        if text == '\u03c0':
            return math.pi
        elif text == '\u03c4':
            return 2 * math.pi
        elif text == 'e':
            return math.e
        else:
            raise ValueError(f"Unknown operator {text}.")

    def toggle_sci_mode(self):
        """Toggle between scientific and normal mode."""
        self.sci_mode = not self.sci_mode

        if self.sci_mode:
            # Change button labels to scientific mode
            # and update handlers
            self.button_objs['sci'].config(bg='orange')
            self.button_objs['√'].config(text='n\u221a')
            self.button_objs['√'].config(command=self.create_button_handler('n\u221a'))
            self.button_objs['/'].config(text='1/x')
            self.button_objs['/'].config(command=self.create_button_handler('1/x'))
            self.button_objs['*'].config(text='tan')
            self.button_objs['*'].config(command=self.create_button_handler('tan'))
            self.button_objs['-'].config(text='cos')
            self.button_objs['-'].config(command=self.create_button_handler('cos'))
            self.button_objs['+'].config(text='sin')
            self.button_objs['+'].config(command=self.create_button_handler('sin'))
            self.button_objs['π'].config(text='\u03c4')
            self.button_objs['π'].config(command=self.create_button_handler('\u03c4'))
            self.button_objs['%'].config(text='e')
            self.button_objs['%'].config(command=self.create_button_handler('e'))
            self.button_objs['÷'].config(text='ln')
            self.button_objs['÷'].config(command=self.create_button_handler('ln'))
            self.button_objs['^'].config(text='log')
            self.button_objs['^'].config(command=self.create_button_handler('log'))
        else:
            # Revert back to normal mode
            self.button_objs['sci'].config(bg='lightyellow')
            self.button_objs['√'].config(text='√')
            self.button_objs['√'].config(command=self.create_button_handler('√'))
            self.button_objs['/'].config(text='/')
            self.button_objs['/'].config(command=self.create_button_handler('/'))
            self.button_objs['*'].config(text='*')
            self.button_objs['*'].config(command=self.create_button_handler('*'))
            self.button_objs['-'].config(text='-')
            self.button_objs['-'].config(command=self.create_button_handler('-'))
            self.button_objs['+'].config(text='+')
            self.button_objs['+'].config(command=self.create_button_handler('+'))
            self.button_objs['π'].config(text='\u03c0')
            self.button_objs['π'].config(command=self.create_button_handler('π'))
            self.button_objs['%'].config(text='%')
            self.button_objs['%'].config(command=self.create_button_handler('%'))
            self.button_objs['÷'].config(text='÷')
            self.button_objs['÷'].config(command=self.create_button_handler('÷'))
            self.button_objs['^'].config(text='^')
            self.button_objs['^'].config(command=self.create_button_handler('^'))

    def on_button_click(self, value):
        """Handle button click: add value to the input field
        and trigger calculation."""
        if value == 'sci':
            # Toggle the sci mode when the "sci" button is clicked
            self.toggle_sci_mode()
        else:
            # For operators, we insert the operator and immediately calculate
            if value in self.operators:
                # For 2-operand operators like '+', '-', '*', '/', etc.
                self.entry.insert(tk.END, value)
                self.add_to_stack()  # Automatically trigger calculation
            else:
                # For numbers, just insert them into the entry field
                self.entry.insert(tk.END, value)

    def add_to_stack(self):
        """Add the current value (operand or operator) to the stack
        when Enter is pressed."""
        current_text = self.entry.get().strip()
        self.history.append(current_text)
        if current_text:
            if current_text in self.operator_2:
                # {'+', '-', '*', '/', '^', '\u00f7', '%'}:
                # Add operator to stack
                self.stack.append(current_text)
                # Clear entry field after adding operator
                self.entry.delete(0, tk.END)
                # Evaluate immediately after adding an operator
                result = self.evaluate_two(self.stack[-3:])
                # self.stack= self.stack[:-3].append(result)  # Nope!
                self.stack = self.stack[:-3]
                self.stack.append(result)
            elif current_text in self.operator_1:
                # {'\u221a', 'sin', 'cos', 'tan',
                # 'ln', 'log', 'x^2', '1/x'}
                # Single operand operators
                self.stack.append(current_text)
                # Clear entry field after adding operator
                self.entry.delete(0, tk.END)
                result = self.evaluate_one(self.stack[-2:])
                self.stack = self.stack[:-2]
                self.stack.append(result)
            elif current_text in self.operator_0:
                # {'\u03c0', '\u03c4', 'e'}
                result = self.evaluate_zero(current_text)
                # Clear the entry field after adding to stack
                self.entry.delete(0, tk.END)
                # self.stack = self.stack[:-1]
                self.stack.append(result)
            else:  # Should be a number
                try:
                    if "." not in current_text:
                        # Should be an int
                        value = int(current_text)
                    else:
                        # Try to convert the text to a float
                        value = float(current_text)
                    #  and add it to the stack
                    self.stack.append(value)
                    # Clear the entry field after adding to stack
                    self.entry.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid number: {current_text}")

            # Always update the stack_label to show the current stack
            self.update_display()
        else:
            messagebox.showerror("Error", "Please enter a valid number or operator.")

    def clear(self):
        """Clear various variables when the Clear button is pressed."""
        # print("Clearing...", self.stack, type(self.stack), self.history, type(self.history))
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
        self.stack_label.config(text=f"{self.stack}")  # Update stack display
        self.history_label.config(text=f"{self.history}")  # Update stack display


# Create the GUI application
if __name__ == "__main__":
    app = RPNCalculator()
    app.mainloop()
