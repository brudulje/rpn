import tkinter as tk
from tkinter import messagebox
import math

# GUI setup
class RPNCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPN Calculator")
        self.geometry("320x350")

        # Entry field for RPN expression
        self.entry = tk.Entry(self, font=("Arial", 14),
                              width=20, borderwidth=2, relief="solid")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Stack for RPN calculation
        self.stack = []

        self.sci_mode = False  # Initially not in scientific mode

        # Define button layout and colors
        self.buttons = [
                    # ('Clear', 1, 0),
                       ('\u221a', 1, 3, 'lightgreen'), ('sci', 1, 4, 'lightyellow'),
                    # ('log', 2, 0), ('sin', 2, 1), ('cos', 2, 2), ('tan', 2, 3), ('sqrt', 2, 4),
                    ('7', 3, 0, 'lightblue'), ('8', 3, 1, 'lightblue'), ('9', 3, 2, 'lightblue'), ('/', 3, 3, 'lightgreen'),   ('\u03c0', 3, 4, 'lightblue'),
                    ('4', 4, 0, 'lightblue'), ('5', 4, 1, 'lightblue'), ('6', 4, 2, 'lightblue'), ('*', 4, 3, 'lightgreen'),   ('%', 4, 4, 'lightgreen'),
                    ('1', 5, 0, 'lightblue'), ('2', 5, 1, 'lightblue'), ('3', 5, 2, 'lightblue'), ('-', 5, 3, 'lightgreen'),   ('\u00f7', 5, 4, 'lightgreen'),
                    ('0', 6, 0, 'lightblue'), ('.', 6, 1, 'lightblue'),               ('+', 6, 3, 'lightgreen'),   ('^', 6, 4, 'lightgreen')
                    ]

        # Create the buttons for the number pad and operators with colors
        self.button_objs = {}
        for (text, row, col, color) in self.buttons:
            button = tk.Button(self, text=text, font=("Arial", 14),
                               width=4, height=1, bg=color,
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.button_objs[text] = button

        # "Enter" button to add current value to the stack
        self.enter_button = tk.Button(self, text="Enter", font=("Arial", 14),
                                      width=4, height=1, bg='darkgray', command=self.add_to_stack)
        self.enter_button.grid(row=6, column=2, pady=5)

        # "Clear" button to clear the input
        self.clear_button = tk.Button(self, text="Clear", font=("Arial", 14),
                                      width=4, height=1, bg='lightgray',
                                      command=lambda: self.entry.delete(0, tk.END))
        self.clear_button.grid(row=1, column=0, pady=5)

        # "Clear Stack" button to manually clear the stack
        self.clear_stack_button = tk.Button(self, text="Clear Stack",
                                            font=("Arial", 14),
                                            width=10, height=1, bg='lightgray',
                                            command=self.clear_stack)
        self.clear_stack_button.grid(row=1, column=1, columnspan=2, pady=5)

        self.stack_label = tk.Label(self, text="[]", font=("Arial", 12),
                                    width=25, height=2)
        self.stack_label.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    # Core of the rpn calculator
    def evaluate_rpn(self, expression):
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
        else:
            raise ValueError(f"Unknown operator {operator}.")

        return result

    def single_operand(self, expression):
        """Operate operators taking a single operand."""
        operand = expression[0]
        operator = expression[1]
        if operator == '\u221a':
            return math.sqrt(operand)
        else:
            raise ValueError(f"Unknown operator {operator}.")

    def toggle_sci_mode(self):
        """Toggle between scientific and normal mode."""
        self.sci_mode = not self.sci_mode

        if self.sci_mode:
            # Change button labels to scientific mode
            self.button_objs['√'].config(text='x^2')
            self.button_objs['/'].config(text='1/x')
            self.button_objs['*'].config(text='tan')
            self.button_objs['-'].config(text='cos')
            self.button_objs['+'].config(text='sin')
            self.button_objs['π'].config(text='\u03c4')
            self.button_objs['%'].config(text='e')
            self.button_objs['÷'].config(text='ln')
            self.button_objs['^'].config(text='lg')
        else:
            # Revert back to normal mode
            self.button_objs['√'].config(text='√')
            self.button_objs['/'].config(text='/')
            self.button_objs['*'].config(text='*')
            self.button_objs['-'].config(text='-')
            self.button_objs['+'].config(text='+')
            self.button_objs['π'].config(text='\u03c0')
            self.button_objs['%'].config(text='%')
            self.button_objs['÷'].config(text='÷')
            self.button_objs['^'].config(text='^')

    def on_button_click(self, value):
        """Handle button click: add value to the input field."""
        current_text = self.entry.get()
        if value == 'sci':
            self.toggle_sci_mode()  # Toggle the sci mode when the "sci" button is clicked
        else:
            self.entry.insert(tk.END, value)

    def add_to_stack(self):
        """Add the current value (operand or operator) to the stack when Enter is pressed."""
        current_text = self.entry.get().strip()
        if current_text:
            if current_text in {'+', '-', '*', '/', '^', '\u00f7', '%'}:
                # Add operator to stack
                self.stack.append(current_text)
                self.entry.delete(0, tk.END)  # Clear entry field after adding operator
                result = self.evaluate_rpn(self.stack[-3:])  # Evaluate immediately after adding an operator
                # self.stack= self.stack[:-3].append(result)  # Nope!
                self.stack = self.stack[:-3]
                self.stack.append(result)
            elif current_text in {'\u221a'}:  # Single operand operators
                self.stack.append(current_text)
                self.entry.delete(0, tk.END)  # Clear entry field after adding operator
                result = self.single_operand(self.stack[-2:])
                self.stack = self.stack[:-2]
                self.stack.append(result)
            elif current_text == '\u03c0':
                self.stack.append(3.1415)
                self.entry.delete(0, tk.END)  # Clear the entry field after adding to stack
            else:  # Should be a number
                try:
                    if not "." in current_text:
                        # Should be an int
                        value = int(current_text)
                    else:
                        # Try to convert the text to a float
                        value = float(current_text)
                    #  and add it to the stack
                    self.stack.append(value)
                    self.entry.delete(0, tk.END)  # Clear the entry field after adding to stack
                except ValueError:
                    messagebox.showerror("Error", f"Invalid number: {current_text}")

            # Always update the stack_label to show the current stack
            self.update_display()
        else:
            messagebox.showerror("Error", "Please enter a valid number or operator.")

    def clear_stack(self):
        """Clear the entire stack when the 'Clear Stack' button is pressed."""
        self.stack.clear()  # Clear the stack
        self.update_display()  # Update the display to reflect the cleared stack

    def update_display(self):
        """Update the stack display label."""
        self.stack_label.config(text=f"{self.stack}")  # Update stack display

# Create the GUI application
if __name__ == "__main__":
    app = RPNCalculator()
    app.mainloop()
