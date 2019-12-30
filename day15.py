import intcodecomputer, csv

with open("input15.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

debug = False

class State():
    def __init__(self, availMoves, path, priorState):
        self.availMoves = availMoves
        self.path = path
        self.priorState = priorState

NORTH, SOUTH, WEST, EAST = range(1, 5)
ALL_DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
PRINT_DIR = {NORTH:"NORTH", SOUTH:"SOUTH", EAST:"EAST", WEST:"WEST"}
DIR_MODS = {NORTH:(0, 1), SOUTH:(0, -1), EAST:(1, 0), WEST:(-1, 0)}
OPPOSITE_DIR = {NORTH:SOUTH, SOUTH:NORTH, EAST:WEST, WEST:EAST}

BOUNCE, MOVED, EXIT = range(3)
RESPONSES = [BOUNCE, MOVED, EXIT]

EMPTY, WALL, SPACE, ROBOT, EXIT = range(5)
ELEMENTS = {EMPTY: " ", WALL: "#", SPACE: ".", ROBOT: "D", EXIT: "%"}

WORLD = {(0,0): SPACE}

def moveRobot(robc, direction):
    x, y = robc
    mx, my = DIR_MODS[direction]
    return (x+mx, y+my)

def drawWorld(world, elements, default, ovr = None, ovrEle = None):
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
                pt = (x + minx, y + miny)
                if ovr != None and ovrEle != None and pt == ovr:
                    cell = ovrEle
                else:
                    cell = world[(x + minx, y + miny)]
            except KeyError:
                cell = default
            st += elements[cell]
            st += " "
        print(st)
    print("")

inp = intcodecomputer.StreamInput()
out = []
outp = intcodecomputer.ArrayOutput(out)

comp = intcodecomputer.defaultComputerWithSources(data, inp, outp)

resp = comp.run()

curState = State(set(ALL_DIRECTIONS), [], None)
robc = (0,0)
end = None

endStates = []

while resp != intcodecomputer.TERMINATE:
    nextState = None
    backtrack = False
    nextDir = 0
    foundExit = False

    # Decide next input
    if len(curState.availMoves) == 0: # gotta go back
        if curState.priorState == None: # can't go nowhere
            break
        else:
            nextDir = OPPOSITE_DIR[curState.path[-1]] # go opposite direction of last move
            nextState = curState.priorState
            backtrack = True
    else:
        nextDir = curState.availMoves.pop()

    nextCoord = moveRobot(robc, nextDir)

    if debug:
        print("ROBOT at", robc, "moving", PRINT_DIR[nextDir])

    inp.storeValue(nextDir)

    # Run on input
    resp = comp.run()

    # Decode output
    if len(out) != 1: 
        raise Exception("output did not contain a single value", out)

    outCode = out[0]
    out.clear()

    if outCode == BOUNCE:
        WORLD[nextCoord] = WALL
        nextState = curState
    else:
        if outCode >= MOVED:
            robc = nextCoord
        
        if outCode == MOVED:
            WORLD[nextCoord] = SPACE
        else:
            WORLD[nextCoord] = EXIT
            end = nextCoord
            foundExit = True

        if not backtrack:
            nextDirSet = set(ALL_DIRECTIONS)
            nextDirSet.remove(OPPOSITE_DIR[nextDir])

            nextPath = list(curState.path)
            nextPath.append(nextDir)

            nextState = State(nextDirSet, nextPath, curState)

            if foundExit:
                endStates.append(nextState)

    curState = nextState

    if debug:
        drawWorld(WORLD, ELEMENTS, EMPTY, robc, ROBOT)
        input("Continue?")
        print("\n\n\n\n")

drawWorld(WORLD, ELEMENTS, EMPTY, robc, ROBOT)

# Part 1
for e in endStates:
    print(len(e.path), "\n")

# Part 2
debug = True
OXY_WORLD = WORLD.copy()

fringeCells = set([end])
minutes = 0

while len(fringeCells) > 0:
    oxygenSpread = False
    nextFringeCells = set()

    for f in fringeCells:
        for d in ALL_DIRECTIONS:
            fd = moveRobot(f, d)

            if OXY_WORLD[fd] == SPACE:
                oxygenSpread = True
                OXY_WORLD[fd] = EXIT
                nextFringeCells.add(fd)

    if oxygenSpread:
        minutes += 1

    if debug:
        drawWorld(OXY_WORLD, ELEMENTS, EMPTY)

    fringeCells = nextFringeCells

print("Oxygen spread everywhere in ", minutes, "minutes")
