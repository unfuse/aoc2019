with open("input4.txt") as file:
    data = [int(x) for x in file.read().split("-")]

def isPasscode(x):
    strCode = str(x)
    codes = {x:0 for x in range(0, 10)}

    for i in range(1, len(strCode)):
        code = int(strCode[i-1])
        nextCode = int(strCode[i])
        codes[code] += 1

        if (i == (len(strCode) - 1)):
            codes[nextCode] += 1

        if code > nextCode:
            return False
    
    codeList = list(codes.values())
    try:
        codeList.index(2)
        return True
    except:
        return False

validPasscodes = []
for x in range(data[0], data[1]+1):
    if isPasscode(x):
        validPasscodes.append(x)

print(len(validPasscodes))