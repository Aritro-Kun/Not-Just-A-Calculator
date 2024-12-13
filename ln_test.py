import sympy
from sympy import sqrt, log
import re

# Handle factorials and ensure we can evaluate them
def handle_factorial(exp):
    exp = re.sub(r'(\d+)!', r'sympy.factorial(\1)', exp)
    exp = re.sub(r'\((.*?)\)!', r'sympy.factorial(\1)', exp)
    return exp

# Main function to simplify the expression
def simplify_expression(exp):
    try:
        # Replace common mathematical expressions
        exp = exp.replace("x", "*")  # Replace x with *
        exp = exp.replace("^", "**")  # Replace ^ with **
        exp = exp.replace("√(", "sqrt(")  # Handle square roots
        exp = exp.replace("%", "/100")  # Handle percentages
        exp = exp.replace("ln(", "log(")  # Replace ln with log for natural log
        exp = handle_factorial(exp)  # Handle factorials
        
        # Now safely evaluate the expression with SymPy functions and factorial handling
        sympy_exp = eval(exp, {"sqrt": sqrt, "log": log, "sympy": sympy})  # Use eval with SymPy functions
        
        # Evaluate numerically if it's not already
        if isinstance(sympy_exp, sympy.Basic):
            sympy_exp = sympy_exp.evalf()

        return sympy_exp  # Return the evaluated result
    except Exception as e:
        return f"Error: {str(e)}"  # Return any error message if there's an issue

# Test the function with some example expressions
exp1 = "ln(9)"  # Should give the result of log(9), which is the natural log
exp2 = "3!"     # Should give the factorial of 3 (3!)
exp3 = "√(16) + ln(10)"  # Should compute sqrt(16) and log(10)

# Print results of testing
print(simplify_expression(exp1))  # Result of ln(9)
print(simplify_expression(exp2))  # Result of 3!
print(simplify_expression(exp3))  # Result of √(16) + ln(10)
