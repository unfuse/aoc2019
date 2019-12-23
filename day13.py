import intcodecomputer, csv

with open("input13.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

EMPTY, WALL, BLOCK, PADDLE, BALL = range(5)
ELEMENTS = {EMPTY: " ", WALL: "#", BLOCK: "B", PADDLE: "-", BALL: "@"}

DIRS = {"a": -1, "": 0, "s": 0, "d": 1}

def drawWorld(world, elements, default):
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0

    for x, y in world.keys():
        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x, maxx)
        maxy = max(y, maxy)

    width = maxx - minx + 1
    height = maxy - miny + 1

    for y in range(height):
        st = ""
        for x in range(width):
            cell = None
            try:
                cell = world[(x + minx, y + miny)]
            except KeyError:
                cell = default
            st += elements[cell]
            st += " "
        print(st)
    print("")

def deriveWorld(out):
    world = {}
    score = 0
    i = 0
    for i in range(0, len(out), 3):
        x, y, e = out[i:i+3]
        if x == -1 and y == 0:
            score = e
        else:
            world[(x, y)] = e
    
    return (world, score)

# part 2
data[0] = 2

inp = intcodecomputer.StreamInput()
out = []
outp = intcodecomputer.ArrayOutput(out)

comp = intcodecomputer.defaultComputerWithSources(data, inp, outp)

resp = intcodecomputer.CONTINUE

while resp != intcodecomputer.TERMINATE:
    resp = comp.run()
    world, score = deriveWorld(out)
    drawWorld(world, ELEMENTS, EMPTY)
    # part 2
    print("SCORE =", score)
    
    ballc = ()
    paddlec = ()
    for k, v in world.items():
        if v == BALL:
            ballc = k
        elif v == PADDLE:
            paddlec = k

    if resp == intcodecomputer.PAUSE:
        d = 0
        if ballc[0] < paddlec[0]:
            d = -1
        elif ballc[0] > paddlec[0]:
            d = 1
        inp.storeValue(d)
        # input("> ")


# part 1
# count = 0
# for k, v in world.items():
#     if v == ELEMENTS[BLOCK]:
#         count += 1

# print(count)