with open("input8.txt") as afile:
    data = [int(x) for x in list(afile.read())]

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = HEIGHT * WIDTH

BLACK, WHITE, TRANSPARENT = range(3)

img = []

for x in range(0, len(data), LAYER_SIZE):
    img.append(data[x : x + LAYER_SIZE])

raster = []

def part2():
    for p in range(LAYER_SIZE):
        for l in range(len(img)):
            pixel = img[l][p]

            if pixel == TRANSPARENT:
                continue
            else:
                raster.append(pixel)
                break

    for h in range(HEIGHT):
        for w in range(WIDTH):
            print(raster[h * WIDTH + w], end = '')

        print("")

part2()


def part1():
    res = []

    for layer in img:
        count = 0
        for pixel in layer:
            if pixel == BLACK:
                count += 1
        res.append((count, layer))

    m = (None, None)

    for (rc, rl) in res:
        mc, ml = m

        if mc == None or rc <= mc:
            m = (rc, rl)

    mc, ml = m
    count1 = 0
    count2 = 0

    for pixel in ml:
        if pixel == WHITE:
            count1 += 1
        elif pixel == TRANSPARENT:
            count2 += 1

    print(count1 * count2)

# part1()