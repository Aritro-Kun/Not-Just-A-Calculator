import sympy
from sympy import sympify
import re

def handle_factorial(exp):
    exp = re.sub(r'(\d+)!', r'sympy.factorial(\1)', exp)
    exp = re.sub(r'\((.*?)\)!', r'sympy.factorial(\1)', exp)
    print(exp)
    return exp

def simpify_expression(exp):
    try:
        exp = exp.replace("x", "*")
        exp = exp.replace("^", "**")
        exp = exp.replace("√(", "sqrt(")
        exp = exp.replace("ln(", "log(")
        exp = exp.replace("%", "/100")
        exp = handle_factorial(exp)
        sympy_exp = sympy.sympify(exp)
        print(sympy_exp)
        result = sympy_exp.evalf()
        print(result)
        return result
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"

exp = "3!"
answer = simpify_expression(exp)
