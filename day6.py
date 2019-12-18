with open("input6.txt") as file:
    data = file.read().splitlines()
COM = 'COM'
YOU = 'YOU'
SAN = 'SAN'
bodySet = set()
orbiting = {COM:None}

for d in data:
    bodies = d.split(')')
    bodySet.update(bodies)
    orbiting[bodies[1]] = bodies[0]

if COM not in bodySet or SAN not in bodySet or YOU not in bodySet:
    raise Exception("something not in the input set")

# this can be memoized to improve performance
def getDistance(body, target, orbits):
    indirects = 0

    if body == target:
        return 0
    elif orbits[body] != target:
        indirects = getDistance(orbits[body], target, orbits)

    return 1 + indirects

def getOrbitChain(body, orbits):
    chain = []

    if body == COM:
        return chain

    parent = orbits[body]
    chain.append(parent)
    chain += getOrbitChain(parent, orbits)

    return chain

def part1():
    total = 0
    for body in bodySet:
        result = getDistance(body, COM, orbiting)
        total += result

    print(total)

youChain = getOrbitChain(YOU, orbiting)
santaChain = getOrbitChain(SAN, orbiting)

print(youChain)
print(santaChain)

path = set()

for y in youChain:
    try:
        if santaChain.index(y):
            continue
    except ValueError:
        path.add(y)

for s in santaChain:
    try:
        if youChain.index(s):
            continue
    except ValueError:
        path.add(s)

print(path)
print(len(path))