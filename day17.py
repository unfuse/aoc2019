import intcodecomputer, csv

with open("input17.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

inp = intcodecomputer.StreamInput()
out = []
outp = intcodecomputer.ArrayOutput(out)

comp = intcodecomputer.defaultComputerWithSources(data.copy(), inp, outp)

comp.run()

rawWorld = out.copy()
out.clear()

world = []
row = []
for a in rawWorld:
    if a == 10:
        world.append(row)
        row = []
    else: 
        row.append(chr(a))

intersections = {}

for ir, r in enumerate(world):
    row = ""
    for ic, c in enumerate(r):
        row += c
        row += " "
        count = 0
        if (c == "#"):
            try:
                count += int(world[ir][ic-1] == "#")
                count += int(world[ir][ic+1] == "#")
                count += int(world[ir-1][ic] == "#")
                count += int(world[ir+1][ic] == "#")
            except IndexError:
                continue

            if (count >= 3):
                intersections[(ir, ic)] = True

    print(row)

print(intersections)

print(sum(map(lambda c: c[0] * c[1], intersections.keys())))

def toAscii(string):
    a = []
    for c in string:
        a.append(ord(c))
    a.append(ord("\n"))
    return a

# L,12,R,8,L,6,R,8,L,6,R,8,L,12,L,12,R,8,L,12,R,8,L,6,R,8,L,6,L,12,R,8,L,6,R,8,L,6,R,8,L,12,L,12,R,8,L,6,R,6,L,12,R,8,L,12,L,12,R,8,L,6,R,6,L,12,L,6,R,6,L,12,R,8,L,12,L,12,R,8
# A,B,A,A,B,C,B,C,C,B
# A = L,12,R,8,L,6,R,8,L,6
# B = R,8,L,12,L,12,R,8
# C = L,6,R,6,L,12
path = toAscii("A,B,A,A,B,C,B,C,C,B")

A = toAscii("L,12,R,8,L,6,R,8,L,6")
B = toAscii("R,8,L,12,L,12,R,8")
C = toAscii("L,6,R,6,L,12")

# can also be y
liveFeed = toAscii("n")

inp = intcodecomputer.StreamInput()
out = []
outp = intcodecomputer.ArrayOutput(out)

# part 2, change mem 0 to 2
data[0] = 2

print(path)
print(A)
print(B)
print(C)

# feed inputs
for d in path:
    inp.storeValue(d)

for d in A:
    inp.storeValue(d)

for d in B:
    inp.storeValue(d)

for d in C:
    inp.storeValue(d)

for d in liveFeed:
    inp.storeValue(d)

comp = intcodecomputer.defaultComputerWithSources(data, inp, outp)

comp.run()

# idk why out isn't clear by this point, maybe the program always outputs the map? 
print(out[-1])