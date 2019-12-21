import csv, intcodecomputer

with open("input11.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

BLACK, WHITE = range(2)
ELEMENTS = {BLACK:".", WHITE:"#"}

N, E, S, W = range(4)
DIRECTIONS = {N:"N", E:"E", S:"S", W:"W"}

LEFT, RIGHT = range(2)
LR = {LEFT:"LEFT", RIGHT:"RIGHT"}

# part1
# WORLD = {(0,0): BLACK}

# part2
WORLD = {(0,0): WHITE}
ROBOT = ((0,0), N)

def drawWorld(world):
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

    for y in range(height-1, -1, -1):
        st = ""
        for x in range(width):
            cell = None
            try:
                cell = world[(x + minx, y + miny)]
            except KeyError:
                cell = BLACK
            st += ELEMENTS[cell]
            st += " "
        print(st)
    print("")


def changeDir(num, change):
    term = None
    if change == 0:
        term = -1
    else:
        term = 1

    return (num + term) % len(DIRECTIONS)

def moveRobot(start, d):
    x, y = start

    if d == N:
        y += 1
    elif d == S:
        y -= 1
    elif d == W:
        x -= 1
    elif d == E:
        x += 1

    return (x, y)

    raise Exception("Unknown dir", d)
    

# data = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
inp = intcodecomputer.StreamInput()
output = []
out = intcodecomputer.ArrayOutput(output)
comp = intcodecomputer.defaultComputerWithSources(data, inp, out)

while True:
    curPos, curDir = ROBOT[0], ROBOT[1]
    inp.storeValue(WORLD[curPos])
    status = comp.run()

    paint, direction = output[0], output[1]
    output.clear()

    WORLD[curPos] = paint
    newDir = changeDir(curDir, direction)
    newPos = moveRobot(curPos, newDir)
    print("moving robot from", curPos, "facing", DIRECTIONS[curDir], "rotating {:5}".format(LR[direction]), "to new pos", newPos, "and dir", DIRECTIONS[newDir])
    ROBOT = (newPos, newDir)

    if newPos not in WORLD.keys():
        WORLD[newPos] = BLACK

    # part 2
    drawWorld(WORLD)

    if status == intcodecomputer.TERMINATE:
        break
# part 1 
# print(len(WORLD))