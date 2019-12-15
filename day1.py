import math

# part 1
def fuel(parm):
    calc = math.floor(parm/3) - 2
    return calc

# part 2
def fuel_recursive(parm):
    calc = fuel(parm)
    if calc <= 0:
        return 0
    return calc + fuel_recursive(calc)

f = open("input1.txt", "r").readlines()

total = 0
for l in f:
    total += fuel_recursive(int(l))

print(total)