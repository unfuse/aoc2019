from time import time

with open("input16.txt") as f:
    initnumbers = [int(x) for x in list(f.read())]

MODIFIERS = [0, 1, 0, -1]
modIdx = 1

ITERATIONS = 100

# part 1 extender is 1 (initinput == input)
# INPUT_EXTENDER = 1
INPUT_EXTENDER = 10000

# worked for part 1, but too slow for part 2
def repeaterArray(arr, iter):
    array = []
    if iter <= 1:
        return arr

    for a in arr:
        for i in range(iter):
            array.append(a)

    return array

# testing example
# initnumbers = [int(x) for x in "03081770884921959731165446850517"]

rawnumbers = []
for i in range(INPUT_EXTENDER):
    rawnumbers.extend(initnumbers)

# part 1 offset is 0
# offset = 0
offset = int("".join([str(x) for x in initnumbers[:7]]))

# optimization - if we only care about the final [offset:] numbers in the final sequence, we can care only about the [offset:] numbers in every sequence
numbers = rawnumbers[offset:]

print("oldLen:", len(rawnumbers))
print("offset:", offset)
print("len:   ", len(numbers))
assert (len(rawnumbers) - offset == len(numbers)), "number array lengths and offset do not match"

# will work for any problem eg
def smallestBrainSolution(numbers, ITERATIONS, modifiers):
    pass # reimplement this just for giggles, use the repeaterArray impl to prebuild all modifers then zip the two arrays together (see pt. 1 commit)

# will work for any problem eg
def smallBrainSolution(numbers, ITERATIONS, modifiers):
    lenn = len(numbers)
    st = int(time())
    for iter in range(ITERATIONS):
        nextNumbers = []
        print("iter:{:2} at:{:4}s".format(iter, int(time()) - st))
        for p in range(lenn):
            s = 0

            for i, n in enumerate(numbers):
                m = MODIFIERS[((i+modIdx+offset)//(p+1+offset)) % 4]
                s += n * m

            ns = abs(s) % 10
            nextNumbers.append(ns)

        numbers = nextNumbers

    print(numbers[:8])

# OFFSET must be larger than the remaining list of numbers for this to work
def mediumBrainSolution(numbers, ITERATIONS):
    lenn = len(numbers)
    st = int(time())
    for iter in range(ITERATIONS):
        nextNumbers = []
        print("iter:{:2} at:{:4}s".format(iter, int(time()) - st))
        for p in range(lenn):
            s = sum(numbers[p:])
            ns = s % 10
            nextNumbers.append(ns)

        numbers = nextNumbers

    print(numbers[:8])

# OFFSET must be larger than the remaining list of numbers for this to work
def bigBrainSolution(numbers, ITERATIONS):
    lenn = len(numbers)
    st = int(time())

    revnum = list(reversed(numbers))
    for iter in range(ITERATIONS):
        nextNumbers = []
        print("iter:{:2} at:{:4}s".format(iter, int(time()) - st))
        rollingSum = 0
        for p in range(lenn):
            rollingSum += revnum[p]
            ns = rollingSum % 10
            nextNumbers.append(ns)

        revnum = nextNumbers

    output = list(reversed(revnum))
    print(output[:8])

# mediumBrainSolution(numbers, ITERATIONS)
bigBrainSolution(numbers, ITERATIONS)