import math

def repeaterArray(arr, iter):
    array = []
    if iter <= 1:
        return arr

    for a in arr:
        for i in range(iter):
            array.append(a)

    return array

MODS = ['a', 'b', 'c', 'd']

for R in range(1, 1000):
    rrange = R*7 + 17
    print("R", R,"range", rrange)
    trueMods = repeaterArray(MODS, R)
    for i in range(rrange):
        exp = trueMods[(i+1)%len(trueMods)]
        act = MODS[(i+1)//R % 4]

        assert exp == act, "exp:{} vs act:{} for R:{} i:{}".format(exp, act, R, i)