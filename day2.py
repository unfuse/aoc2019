import csv

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def calc(data, idx, fn):
    cell1 = data[idx+1]
    cell2 = data[idx+2]
    target = data[idx+3]

    data[target] = fn(data[cell1], data[cell2])

def fn(data, noun, verb):
    data[1] = noun
    data[2] = verb

    i = 0
    while True:
        op = data[i]

        if op == 99:
            break
        elif op == 1:
            calc(data, i, add)
        elif op == 2:
            calc(data, i, mul)
        else:
            print("ENCOUNTERED AN INVALID OPCODE")
            break
        i+=4

    return data[0]

with open("input2.txt") as csvfile:
    data = [int(x) for x in list(csv.reader(csvfile))[0]]

# part 1 noun/verb
# print(fn(data, 12, 2))

# part 2 noun/verb
target = 19690720

for n in range(10001) :
    for v in range(10001):
        d = data[:]
        try:
            cur = fn(d, n, v)
        except:
            None
        if cur == target:
            print( (100*n) + v )