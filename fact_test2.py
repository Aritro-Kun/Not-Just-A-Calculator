import sympy
import re

# Function to handle factorials explicitly
def handle_factorial(exp):
    # Replace factorials like 3! or (3+2)!
    exp = re.sub(r'(\d+)!', r'sympy.factorial(\1)', exp)
    exp = re.sub(r'\((.*?)\)!', r'sympy.factorial(\1)', exp)
    return exp

# Function to simplify the expression
def simplify_expression(exp):
    try:
        # Replace common symbols with Python equivalents
        exp = exp.replace("x", "*")
        exp = exp.replace("^", "**")
        exp = exp.replace("√(", "sqrt(")
        exp = exp.replace("ln(", "log(")
        exp = exp.replace("%", "/100")
        
        # Handle factorials explicitly
        exp = handle_factorial(exp)
        
        # Now evaluate the expression using eval(), which will properly handle the factorial calls
        result = eval(exp)
        
        # Return the evaluated result
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Test cases
exp = "3!"  # Factorial of 3
answer = simplify_expression(exp)
print(answer)  # Expected output: 6


