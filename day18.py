
with open("input18.txt") as f:
    data = f.read().splitlines()

WIDTH = len(data[0])
HEIGHT = len(data)

maze = {}
reverseMaze = {}

normies = set([".", "#"])
specials = {}

for y, rows in enumerate(data):
    rowStr = ""
    for x, cell in enumerate(rows):
        rowStr += cell
        rowStr += " "

        maze[(x, y)] = cell
        if cell not in normies:
            specials[cell] = (x, y)
    print(rowStr)

def valInRange(c1, c2, c3):
    return c1 >= c2 and c1 <= c3

keys = { (key if valInRange(key, "a", "z") else None):(value if valInRange(key, "a", "z") else None) for key, value in specials.items()}
keys.pop(None, 0)

doors = { (key if valInRange(key, "A", "Z") else None):(value if valInRange(key, "A", "Z") else None) for key, value in specials.items()}
doors.pop(None, 0)

cursorStart = specials.get("@", None)

# print(keys)
# print(doors)
# print(actor)
