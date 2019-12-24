import math

with open("input14.txt") as f:
    data = f.read().splitlines()

ORE = "ORE"
FUEL = "FUEL"

FUEL_RECIPE = None
ORE_RECIPES = set()
ALL_RECIPES = set()
NON_ORE_RECIPES = set()

class Component():
    def __init__(self, st):
        st = st.strip().split(" ")
        self.ele = st[1]
        self.num = int(st[0])
    
    def __str__(self):
        return "{}x {}".format(self.num, self.ele)

    def __repr__(self):
        return self.__str__()

class Recipe():
    def __init__(self, st):
        i, o = st.strip().split("=>", 1)
        ins = set()
        for s in i.strip().split(","):
            s = s.strip()
            ins.add(Component(s))

        self.out = Component(o)
        self.ins = ins
        self.inEles = set([x.ele for x in ins])

    def __str__(self):
        inStr = ""
        for i in self.ins:
            inStr += (str(i))
            inStr += " "
        return "{:8} <= {}".format(str(self.out), inStr)

    def __repr__(self):
        return self.__str__()

def findRecipeByOutputEle(recipes, out):
    for r in recipes:
        if r.out.ele == out:
            return r

    raise Exception("could not find a recipe outputting", out)

def componentMultiplier(req, prov):
    if req <= prov:
        return (1, prov-req)
    numNeeded = math.ceil(req/prov)
    return (numNeeded, (prov * numNeeded) - req)

def reduceComponents(needs, recipes, terminals, extras):
    stop = False
    while not stop:
        nextNeeds = {}
        for k, v in needs.items():
            if k in terminals:
                if k in nextNeeds.keys():
                    nextNeeds[k] = nextNeeds[k] + v
                else:
                    nextNeeds[k] = v
                continue
            nRecipe = findRecipeByOutputEle(recipes, k)

            if k in extras.keys() and extras[k] > 0: # we have extra of the current material
                extra = extras[k]
                if v <= extra: # we have more extra than this recipe needs
                    extras[k] = extra - v
                else: # we need more than the extras we have
                    newV = v - extra

                    mul, ext = componentMultiplier(newV, nRecipe.out.num)
                    extras[k] = ext

                    for i in nRecipe.ins:
                        if i.ele in nextNeeds.keys():
                            nextNeeds[i.ele] = nextNeeds[i.ele] + i.num * mul
                        else:
                            nextNeeds[i.ele] = i.num * mul
            else: # no extras, generate the max, store any leftovers
                mul, ext = componentMultiplier(v, nRecipe.out.num)
                extras[k] = ext

                for i in nRecipe.ins:
                    if i.ele in nextNeeds.keys():
                        nextNeeds[i.ele] = nextNeeds[i.ele] + i.num * mul
                    else:
                        nextNeeds[i.ele] = i.num * mul

        needs = nextNeeds
        
        nextStop = True
        for k in needs.keys():
            nextStop = nextStop and k in terminals

        stop = nextStop

    return needs, extras

for d in data:
    recipe = Recipe(d)

    if ORE in recipe.inEles:
        ORE_RECIPES.add(recipe)
    else:
        NON_ORE_RECIPES.add(recipe)

    if FUEL == recipe.out.ele:
        if FUEL_RECIPE == None:
            FUEL_RECIPE = recipe
        else:
            raise Exception("Wasn't expecting a second fuel recipe")

    ALL_RECIPES.add(recipe)

if FUEL_RECIPE == None:
    raise Exception("Did not find fuel recipe within data")

ONE_FUEL_NEEDS = {c.ele:c.num for c in FUEL_RECIPE.ins}
DONES = [x.out.ele for x in ORE_RECIPES]

# part 1
needs, ext = reduceComponents(ONE_FUEL_NEEDS, ALL_RECIPES, set([ORE]), {})
print(needs[ORE])

# part 2
TOTAL_ORE = 1000000000000

numOreUsed = 0
numFuelMade = 0
incrementalExtras = {}
numFuelPerRound = 1000000

def multiplyNeeds(needs, factor):
    if factor <= 0:
        raise Exception("why would you do this, dingus")
    elif factor == 1:
        return needs
    
    return {x[0]:x[1]*factor for x in needs.items()}

while True:
    factoredNeeds = multiplyNeeds(ONE_FUEL_NEEDS, numFuelPerRound)
    requires, extras = reduceComponents(factoredNeeds, ALL_RECIPES, set([ORE]), incrementalExtras.copy())

    if numOreUsed + requires[ORE] > TOTAL_ORE:
        if numFuelPerRound == 1:
            break
        else:
            numFuelPerRound = numFuelPerRound // 2

    else:
        incrementalExtras = extras
        numOreUsed += requires[ORE]
        numFuelMade += numFuelPerRound
        print("made fuel! total =", numFuelMade)

print(numFuelMade)