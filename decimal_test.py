exp = "34 + 69 - 47/71.1756"
operand_list = ["+", "-", "*", "/", "ln(", "^", "√"]

i = -1
while (exp[i] not in operand_list):
    i-=1
print(i)
print(exp[i])
for a in range(i, 0, 1):
    if (exp[a] == "."):
        print(a)
