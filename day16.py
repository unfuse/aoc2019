with open("input16.txt") as f:
    initnumbers = [int(x) for x in list(f.read())]

MODIFIERS = [0, 1, 0, -1]
modIdx = 1

ITERATIONS = 100

# part 1 extender is 1 (initinput == input)
# INPUT_EXTENDER = 1
INPUT_EXTENDER = 10000

def repeaterArray(arr, iter):
    array = []
    if iter <= 1:
        return arr

    for a in arr:
        for i in range(iter):
            array.append(a)

    return array


# testing example
# initnumbers = [int(x) for x in "03036732577212944063491565474664"]

numbers = []
for i in range(INPUT_EXTENDER):
    numbers.extend(initnumbers)

# part 1 offset is 0
# offset = 0
offset = int("".join([str(x) for x in initnumbers[:7]]))

for iter in range(ITERATIONS):
    print(iter)
    nextNumbers = []
    for p in range(len(numbers)):
        if p % 100 == 0:
            print("chugging on number", p)
        s = 0
        pos = p + 1
        modifiers = repeaterArray(MODIFIERS, pos)
        ds = []

        for i, n in enumerate(numbers):
            m = modifiers[(modIdx + i)%len(modifiers)]
            # ds.append("{:1}*{:2}".format(n, m))
            s += n * m
        
        # print(" + ".join(ds), "=", s)

        ns = abs(s) % 10
        nextNumbers.append(ns)

    numbers = nextNumbers
    # print(numbers)

# Part 1
print(numbers[offset:offset+8])