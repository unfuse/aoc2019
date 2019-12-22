
with open("input12.txt") as f:
    data = f.read().splitlines()

# data = """<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>
# """.splitlines()

X, Y, Z = "x", "y", "z"
COORDS = [X, Y, Z]

def printMoons(moons):
    for m in moons:
        print(m)
    print("")

def calculateEnergy(vec):
    return abs(vec[X]) + abs(vec[Y]) + abs(vec[Z])

def calculateSingleGravity(a, b):
    if a == b:
        return 0
    if a < b:
        return 1
    return -1

def addDicts(a, b):
    return {c:a[c] + b[c] for c in COORDS}

class Moon():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.vel = {X:0, Y:0, Z:0}
        self.pe = calculateEnergy(self.pos)
        self.ke = 0
    
    def totalEnergy(self):
        return self.pe * self.ke

    def calculateGravityVelocity(self, otherMoon):
        return {c:calculateSingleGravity(self.pos[c], otherMoon.pos[c]) for c in COORDS}

    def updateMoon(self, gravities):
        newVel = self.vel
        for g in gravities:
            newVel = addDicts(newVel, g)

        newPos = addDicts(self.pos, newVel)
        self.pos = newPos
        self.vel = newVel
        self.pe = calculateEnergy(newPos)
        self.ke = calculateEnergy(newVel)

    def __str__(self):
        posStr = "<x: {:3}, y: {:3}, z: {:3}>".format(self.pos[X], self.pos[Y], self.pos[Z])
        velStr = "<x: {:3}, y: {:3}, z: {:3}>".format(self.vel[X], self.vel[Y], self.vel[Z])
        return "{:8} - pos:{} vel:{} pe: {:3} ke: {:3} te: {:5}".format(self.name, posStr, velStr, self.pe, self.ke, self.totalEnergy())
        
def parseInput(name, moon):
    return Moon(name, {m.strip()[0]:int(m.strip()[2:]) for m in moon.strip("<>").split(",")})

IO = parseInput("Io", data[0])
EUROPA = parseInput("Europa", data[1])
GANYMEDE = parseInput("Ganymede", data[2])
CALLISTO = parseInput("Callisto", data[3])

MOONS = [IO, EUROPA, GANYMEDE, CALLISTO]

TIME = 1000

for t in range(TIME):
    # print("Time", t)
    # print("-----------")
    # printMoons(MOONS)

    updates = {moon:[] for moon in MOONS}

    for m in MOONS:
        update = []
        for om in MOONS:
            if m == om:
                continue
            update.append(m.calculateGravityVelocity(om))
        updates[m] = update

    for m in MOONS:
        m.updateMoon(updates[m])

# print("Final")
# print("-----------")
# printMoons(MOONS)

# part 1
totalEnergy = 0

for m in MOONS:
    totalEnergy += m.totalEnergy()

print(totalEnergy)
