import tkinter as tk
import sympy
from sympy import sympify, log, sqrt
import math
import re #regex-expression, is used only in the case of a special edge-case, pertaining to factorials.

root = tk.Tk()

root.title("Calculator")
root.geometry("400x550")
root.resizable(False, False)
root.config(bg="#000000")

#colours-paddle
top_bg = "#000000"
mid_bg = "#424242"
bottom_bg = "#191919"
neon_button = "#c1ff72"

simple_buttons = ["%", "/", "7", "8", "9", "x", "4", "5", "6", "+", "1", "2", "3", "-", "00", "0", ".", "(", ")"]
special_buttons = ["√(", "^", "!", "ln("]

current_input_state = ""

def valid_to_input(value):
    global current_input_state
    invalid_first_operands = ["+", "-", "x", "/", "%", ".", ")", "^", "!"]
    if not current_input_state:
        if value in invalid_first_operands:
            return False
        if not (value.isdigit() or value in ["(", "ln(", "√("]):
            return False
    else:
        if (value.isdigit() and current_input_state[-1] in ["%", ")", "!"]):
            return False
        if (current_input_state[-1].isdigit()) and value in ["(", "√(", "ln("]:
            return False
        invalid_running_operands = ["/", "x", "+", "-", ".", "^", "!"]
        if value in invalid_running_operands and current_input_state[-1] in invalid_running_operands:
            return False
        if value == "(" and current_input_state[-1].isdigit():
            return False
        if current_input_state[-1] == "(" and not ((value.isdigit()) or value in ["(", "√(", "ln("]):
            return False
        if value == ")" and not (current_input_state[-1].isdigit() or current_input_state[-1] in ["!", ")"]):
            return False
        operand_list = ["+", "-", "*", "/", "ln(", "^", "√(", "("]
        if value == "." and not (current_input_state[-1].isdigit()):
            return False
        if value == "." and (current_input_state[-1].isdigit()):
            i = -1
            while(current_input_state[i] not in operand_list):
                i-=1
            for a in range(i, 0, 1):
                if(current_input_state[a]=="."):
                    return False
        if(current_input_state[-1] == "." and not value.isdigit()):
            return False
        if (current_input_state[-1]=="ln("):
            if value in ["%", "/", "*", "^", "x", "+", "-", ")"]:
                return False
        if value=="!" and current_input_state[-1] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "00", ")"]:
            return False
        if current_input_state[-1]=="!" and not (value in ["+", "-", "x", "/", "!", ")"]):
            return False
        if value == "ln(" and not (current_input_state[-1] in ["+", "-", "x", "/", "^", "√(", "ln(", "("]):
            return False
        if current_input_state[-1] == "ln(" and not (value.isdigit() or value in ["(", "√("]):
            return False
        if value == "^" and not (current_input_state[-1].isdigit() or current_input_state[-1] in [")"]):
            return False
        if current_input_state[-1]=="^" and not (value.isdigit() or value in ["ln(", "√(", "-", "+"]):
            return False
    return True
    
def update_display(value):
    input_output_canvas.config(state=tk.NORMAL)
    input_output_canvas.insert(tk.END, value)
    input_output_canvas.config(state=tk.DISABLED)

def basic_button_press(value):
    global current_input_state
    if valid_to_input(value):
        current_input_state+=value
        update_display(value)

def special_button_press(value):
    global current_input_state
    if valid_to_input(value):
        current_input_state+=value
        update_display(value)

def handle_factorial(exp):
    exp = re.sub(r'(\d+)!', r'sympy.factorial(\1)', exp)
    exp = re.sub(r'\((.*?)\)!', r'sympy.factorial(\1)', exp)
    return exp

def simpify_expression(exp):
    try:
        exp = exp.replace("x", "*")
        exp = exp.replace("^", "**")
        exp = exp.replace("√(", "sqrt(")
        exp = exp.replace("ln(", "log(")
        exp = exp.replace("%", "/100")
        exp = handle_factorial(exp)
        result = eval(exp, {"sqrt": sqrt, "log": log, "sympy": sympy})
        if isinstance(result, sympy.Basic):
            result = result.evalf()
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def button_press(value):
    global current_input_state
    if value == "=":
        try:
            evaluated_val = simpify_expression(current_input_state)
            input_output_canvas.config(state=tk.NORMAL)
            input_after_output_canvas.config(state=tk.NORMAL)
            input_output_canvas.delete(0, tk.END)
            input_after_output_canvas.insert(0, current_input_state)
            input_output_canvas.insert(0, evaluated_val)
            input_output_canvas.config(state=tk.DISABLED)
            input_after_output_canvas.config(state=tk.DISABLED)
            current_input_state = "" #here we delete the whole expression, but in future, don't delete this, rather make a way such that further calculation can be done with this exp, by clicking some button, say like = or smth
        except Exception as e:
            input_output_canvas.config(state=tk.NORMAL)
            input_after_output_canvas.config(state=tk.NORMAL)
            input_after_output_canvas.insert(0, current_input_state)
            input_output_canvas.delete(0, tk.END)
            input_output_canvas.insert(0, "Error")
            input_output_canvas.config(state=tk.DISABLED)
            input_after_output_canvas.config(state=tk.DISABLED)
            current_input_state = ""
    elif value in simple_buttons:
        basic_button_press(value)
    elif value in special_buttons:
        special_button_press(value)
    elif value=="<---":
        current_input_state = current_input_state[:-1]
        input_output_canvas.config(state = tk.NORMAL)
        input_output_canvas.delete(0, tk.END)
        input_output_canvas.insert(0, current_input_state)
        input_output_canvas.config(state=tk.DISABLED)
    elif value=="C":
        current_input_state = ""
        input_output_canvas.config(state=tk.NORMAL)
        input_after_output_canvas.config(state=tk.NORMAL)
        input_output_canvas.delete(0, tk.END)
        input_after_output_canvas.delete(0, tk.END)
        input_output_canvas.config(state=tk.DISABLED)
        input_after_output_canvas.config(state=tk.DISABLED)


#Top Frame for navigation
top_frame = tk.Frame(root, bg=top_bg, height = 52)
top_frame.pack(fill="x")
top_frame.grid_propagate(False)

top_frame_text = tk.Label(top_frame, text="Calculator", font=("Calibri", 16, "bold"), fg=neon_button, bg=top_bg)
top_frame_text.grid(row=0, column=0, padx=20, pady=10, sticky="w")

#Canvas where inputs and results are shown
canvas_frame = tk.Frame(root, bg=top_bg, height=160)
canvas_frame.pack(fill="x")
canvas_frame.grid_propagate(False)

input_after_output_canvas = tk.Entry(canvas_frame,  font=("Calibri", 16), fg="#ffffff", bg=top_bg, bd=0, insertbackground="white", state=tk.DISABLED, disabledbackground=top_bg, disabledforeground="#ffffff")
input_after_output_canvas.pack(fill="x", padx=20, pady=10)

input_output_canvas = tk.Entry(canvas_frame, font=("Calibri", 24, "bold"), fg = "#ffffff", bg = top_bg, bd = 0, insertbackground="white", state=tk.DISABLED, disabledbackground=top_bg, disabledforeground="#ffffff")
input_output_canvas.pack(fill="x", padx=20, pady=36)

#Additional keypad region
patti_frame = tk.Frame(root, bg=mid_bg, height=60)
patti_frame.pack(fill="x")
patti_frame.grid_propagate(False)

patti_buttons_list = ["√(", "(", ")", "^", "!", "ln("]
for i, value in enumerate(patti_buttons_list):
    patti_button = tk.Button(
        patti_frame,
        text=value,
        font=("Calibri", 18),
        fg="#ffffff",
        bg = mid_bg,
        bd=0,
        activebackground="#5a5a5a",
        activeforeground="#ffffff",
        padx=10, pady=7,
        command = lambda val=value: button_press(val)
    )
    patti_button.grid(row=0, column=i, padx=10)

#Main keypad region
keypad_frame = tk.Frame(root, bg=bottom_bg, height=278)
keypad_frame.pack(fill="x")
keypad_frame.grid_propagate(False)

for i in range(0, 4):
    keypad_frame.grid_columnconfigure(i, weight=1, uniform="equal")

keypad_buttons_list = [["C", "%", "<---", "/"], ["7", "8", "9", "x"], ["4", "5", "6", "+"], ["1", "2", "3", "-"], ["00", "0", ".", "="]]
for row_number, row in enumerate(keypad_buttons_list):
    for column_number, value in enumerate(row):
        if row_number == 0 or column_number == len(row)-1:
            button_fg = neon_button
        else:
            button_fg = "#ffffff"
        keypad_button = tk.Button(
            keypad_frame,
            text = value,
            font = ("Calibri", 18),
            fg = button_fg,
            bg = bottom_bg,
            bd = 0,
            activebackground = "#5a5a5a",
            activeforeground = "#ffffff",
            padx = 10, pady=5,
            command = lambda val=value:button_press(val)
        )
        keypad_button.grid(row=row_number, column = column_number, padx=10)

root.mainloop()