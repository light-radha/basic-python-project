import tkinter as tk
from tkinter import messagebox
import pyperclip

class BasicCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Calculator")
        self.root.geometry("420x690")
        self.root.resizable(False, False)

        self.first_operand = 0
        self.operator = ""
        self.is_new_input = True
        self.is_dark_theme = False
        self.is_history_visible = True
        self.history_log = []

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.input_field = tk.Entry(self.root, font=("Arial", 18), justify='right', bd=2)
        self.input_field.place(x=20, y=20, width=360, height=40)
        self.input_field.configure(state='readonly')

        self.result_field = tk.Entry(self.root, font=("Arial", 12, "italic"), justify='right', bd=0)
        self.result_field.place(x=20, y=65, width=360, height=30)
        self.result_field.configure(state='readonly', fg='gray')

        self.toggle_history_btn = tk.Button(self.root, text="Hide History", command=self.toggle_history)
        self.toggle_history_btn.place(x=20, y=100, width=170, height=30)

        self.theme_toggle_btn = tk.Button(self.root, text="Dark Theme", command=self.toggle_theme)
        self.theme_toggle_btn.place(x=210, y=100, width=170, height=30)

        self.history_area = tk.Text(self.root, font=("Courier", 12), state='disabled')
        self.history_area.place(x=20, y=140, width=360, height=100)

        self.create_buttons()

    def create_buttons(self):
        button_texts = [
            "C", "Back", "", "", "/",
            "7", "8", "9", "*", "-",
            "4", "5", "6", "+", "Copy",
            "1", "2", "3", "CH", "=",
            "0", ".", "", "", ""
        ]
        self.all_buttons = []
        x, y = 20, 260

        for i, text in enumerate(button_texts):
            if text == "":
                x += 70
                if (i + 1) % 5 == 0:
                    x = 20
                    y += 50
                continue

            btn = tk.Button(self.root, text=text, width=6, height=2,
                            font=("Arial", 14), command=lambda t=text: self.on_button_click(t))
            btn.place(x=x, y=y, width=60, height=40)
            self.all_buttons.append(btn)

            x += 70
            if (i + 1) % 5 == 0:
                x = 20
                y += 50

    def on_button_click(self, command):
        current_text = self.input_field.get()

        if command in "0123456789.":
            if self.is_new_input:
                self.set_input(command)
                self.is_new_input = False
            else:
                self.set_input(current_text + command)

        elif command in "+-*/":
            if current_text:
                self.first_operand = float(current_text)
                self.operator = command
                self.is_new_input = True

        elif command == "=":
            if current_text and self.operator:
                second_operand = float(current_text)
                try:
                    result = self.calculate_result(self.first_operand, second_operand, self.operator)
                    expression = f"{self.first_operand} {self.operator} {second_operand} = {result}"
                    self.set_input(str(result))
                    self.result_field.configure(state='normal')
                    self.result_field.delete(0, tk.END)
                    self.result_field.configure(state='readonly')

                    self.history_log.append(expression)
                    self.update_history()
                    self.operator = ""
                    self.is_new_input = True
                except ZeroDivisionError:
                    self.set_input("Error")

        elif command == "C":
            self.clear()

        elif command == "CH":
            self.history_log.clear()
            self.update_history()

        elif command == "Back":
            self.set_input(current_text[:-1])

        elif command == "Copy":
            pyperclip.copy(current_text)

    def calculate_result(self, a, b, op):
        if op == '+': return a + b
        elif op == '-': return a - b
        elif op == '*': return a * b
        elif op == '/': return a / b if b != 0 else float('inf')

    def set_input(self, text):
        self.input_field.configure(state='normal')
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, text)
        self.input_field.configure(state='readonly')

    def clear(self):
        self.set_input("")
        self.result_field.configure(state='normal')
        self.result_field.delete(0, tk.END)
        self.result_field.configure(state='readonly')
        self.operator = ""
        self.first_operand = 0
        self.is_new_input = True

    def update_history(self):
        self.history_area.configure(state='normal')
        self.history_area.delete('1.0', tk.END)
        for entry in self.history_log:
            self.history_area.insert(tk.END, entry + "\n")
        self.history_area.configure(state='disabled')

    def toggle_history(self):
        self.is_history_visible = not self.is_history_visible
        self.history_area.place_forget() if not self.is_history_visible else self.history_area.place(x=20, y=140, width=360, height=100)
        self.toggle_history_btn.config(text="Show History" if not self.is_history_visible else "Hide History")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.theme_toggle_btn.config(text="Light Theme" if self.is_dark_theme else "Dark Theme")
        self.apply_theme()

    def apply_theme(self):
        bg = "#2b2b2b" if self.is_dark_theme else "#ffffff"
        fg = "#ffffff" if self.is_dark_theme else "#000000"
        btn_bg = "#3c3f41" if self.is_dark_theme else "#dcdcdc"

        self.root.configure(bg=bg)
        self.input_field.configure(bg=btn_bg, fg=fg)
        self.result_field.configure(bg=bg, fg="#aaaaaa" if self.is_dark_theme else "gray")
        self.history_area.configure(bg=btn_bg, fg=fg)

        self.toggle_history_btn.configure(bg=btn_bg, fg=fg)
        self.theme_toggle_btn.configure(bg=btn_bg, fg=fg)

        for btn in self.all_buttons:
            btn.configure(bg=btn_bg, fg=fg)


# Run the application
if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        import os
        os.system('pip install pyperclip')
        import pyperclip

    root = tk.Tk()
    app = BasicCalculator(root)
    root.mainloop()