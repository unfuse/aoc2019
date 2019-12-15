import csv

with open("input3.txt") as csvfile:
    data = list(csv.reader(csvfile))

def move(pair, code):
    (x, y, d) = pair
    dir = code[0]
    val = int(code[1:])

    if dir == 'U':
        y += val
    elif dir == 'D':
        y -= val
    elif dir == 'R':
        x += val
    elif dir == 'L':
        x -= val

    d += val

    return (x, y, d)

def intersect(a, b, c, d):
    ax, ay, ad = a
    bx, by, bd = b
    cx, cy, cd = c
    dx, dy, dd = d

    if parallel(a, b, c, d): #parallel
        return [False, None]
    
    if ax == bx: # vertical line
        crossleft = cx <= ax and dx >= bx
        crossright = dx <= ax and cx >= bx
        if crossleft or crossright: # horizontal line crosses
            if ay <= cy and cy <= by or by <= cy and cy <= ay: # and at right y
                coord = cx if crossleft else dx
                firstd = ad + abs(ay - cy)
                second = cd + abs(ax - coord)
                return [True, (ax, cy, firstd, second)]
    
    if ay == by: #horizontal line
        crossup = cy <= ay and dy >= by
        crossdown = dy <= ay and cy >= by
        if crossup or crossdown: # vertical line crosses
            if ax <= cx and cx <= bx or bx <= cx and cx <= ax: # and at right x
                coord = cy if crossup else dy
                firstd = ad + abs(ax - cx)
                second = cd + abs(ay - coord)
                return [True, (cx, ay, firstd, second)]
                
    return [False, None]


def parallel(a, b, c ,d): 
    ax, ay, ad = a
    bx, by, bd = b
    cx, cy, cd = c
    dx, dy, dd = d

    fx, fy = (bx-ax, by-ay)
    sx, sy = (dx-cx, dy-cy)

    return (fx == 0 and sx == 0) or (fy == 0 and sy == 0)

def dist(pair):
    x, y, _, _ = pair
    return abs(x) + abs(y)

coords =[[(0,0,0)], [(0,0,0)]]
for i, d in enumerate(data):
    c = coords[i]
    point = c[0]
    for code in d:
        np = move(point, code)
        c.append(np)
        point = np

intersections = []

for i in range(len(coords[0]) - 1):
    for j in range(len(coords[1]) - 1):
        a = coords[0][i]
        b = coords[0][i+1]
        c = coords[1][j]
        d = coords[1][j+1]

        res = intersect(a, b, c, d)

        if res[0] == True:
            intersections.append(res[1])

dists = [dist(x) for x in intersections]
travels = [d1 + d2 for x, y, d1, d2 in intersections]

mindist = min(dists)
mintravel = min(travels)

print(mindist) # part 1
print(mintravel) # part 2
