import math

with open("input10.txt") as f:
    data = f.read().splitlines()

HEIGHT = len(data)
WIDTH = len(data[0])
TOTAL_SPACES = HEIGHT * WIDTH

ASTEROID = '#'
SPACE = '.'
N, NE, E, SE, S, SW, W, NW = range(8)

asteroids = set()

class DistanceInfo():
    def __init__(self, src, tar, vec, minVec, distance, direction, slope):
        self.src = src
        self.tar = tar
        self.vec = vec
        self.minVec = minVec
        self.distance = distance
        self.direction = direction
        self.slope = slope

    def __lt__(self, value):
        if self.direction != value.direction:
            return self.direction < value.direction

        if self.slope == value.slope:
            return self.distance < value.distance

        return self.slope < value.slope

    def __str__(self):
        return "src:{} tar:{} vec:{} mvec:{} dist:{} dir:{} slope:{}".format(self.src, self.tar, self.vec, self.minVec, self.distance, self.direction, self.slope)
        

def getDirection(xdiff, ydiff):
    if xdiff == 0:
        if ydiff == 0: 
            raise Exception("Somehow tried to compare to self")
        elif ydiff > 0:
            return S
        else:
            return N
    elif xdiff > 0:
        if ydiff == 0: 
            return E
        elif ydiff > 0:
            return SE
        else:
            return NE
    elif xdiff < 0:
        if ydiff == 0: 
            return W
        elif ydiff > 0:
            return SW
        else:
            return NW

    raise Exception("Could not determine direction somehow")

def distanceInfo(src, tar):
    xdiff = tar[0] - src[0]
    ydiff = tar[1] - src[1]
    direction = getDirection(xdiff, ydiff)
    distance = abs(ydiff) + abs(xdiff)

    gcd = math.gcd(xdiff, ydiff)

    xdiffmin = xdiff
    ydiffmin = ydiff 

    if (gcd > 1): 
        xdiffmin = xdiff / gcd
        ydiffmin = ydiff / gcd

    slope = None
    if xdiff != 0:
        slope = ydiff / xdiff
            
    return DistanceInfo(src, tar, (xdiff, ydiff), (xdiffmin, ydiffmin), distance, direction, slope)

# figure out gcd of diffs to determine the "root" blocking point, catalog instances by root blocking point for counting, then parse all asteroids PER asteroid to determine blocking trajectories

for h in range(HEIGHT):
    for w in range(WIDTH):
        if data[h][w] == ASTEROID:
            asteroids.add((w, h))

detections = {x:[] for x in asteroids}
all_infos = {x:[] for x in asteroids}

for src in asteroids:
    minDists = set()
    for tar in asteroids:
        if src == tar:
            continue
            
        distance = distanceInfo(src, tar)
        all_infos[src].append(distance)
        minDists.add(distance.minVec)

    detections[src] = minDists

m = None
for k, v in detections.items():
    if m == None or len(v) > len(m[1]):
        m = (k, v)

print(m[0], len(m[1]))

STATION = m[0]
INFO = sorted(all_infos[STATION])
minVecDict = {x:[] for x in detections[STATION]}

all_hits = []
hits_this_cycle = set()

while INFO != None and len(INFO) > 0:
    i = 0
    while i < len(INFO) and INFO[i].minVec in hits_this_cycle:
        i += 1

    if i == len(INFO): # made a full rotation of minVecs
        i = 0
        hits_this_cycle = set()
    else: 
        info = INFO.pop(i)
        print("Hit {:3} {}".format(len(all_hits), info))
        all_hits.append(info)
        hits_this_cycle.add(info.minVec)

print(len(all_hits))
print(all_hits[199].tar)
    

