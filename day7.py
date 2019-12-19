import csv, intcodecomputer, itertools

with open("input7.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

outputs = []

def part2():
    for phaseSettings in itertools.permutations(list(range(5, 10))):

        programs = [data[:] for x in range(5)]

        output = [[phaseSettings]]

        # Part 2 wire
        inp0 = intcodecomputer.StreamInput()
        inp0.storeValue(phaseSettings[0])
        inp0.storeValue(0)

        inp1 = intcodecomputer.StreamInput()
        inp1.storeValue(phaseSettings[1])

        inp2 = intcodecomputer.StreamInput()
        inp2.storeValue(phaseSettings[2])

        inp3 = intcodecomputer.StreamInput()
        inp3.storeValue(phaseSettings[3])

        inp4 = intcodecomputer.StreamInput()
        inp4.storeValue(phaseSettings[4])

        out0 = intcodecomputer.StreamOutput(inp1)
        out1 = intcodecomputer.StreamOutput(inp2)
        out2 = intcodecomputer.StreamOutput(inp3)
        out3 = intcodecomputer.StreamOutput(inp4)
        out4 = intcodecomputer.StreamOutput(inp0)

        comp0 = intcodecomputer.defaultComputerWithSources(programs[0], inp0, out0)
        comp1 = intcodecomputer.defaultComputerWithSources(programs[1], inp1, out1)
        comp2 = intcodecomputer.defaultComputerWithSources(programs[2], inp2, out2)
        comp3 = intcodecomputer.defaultComputerWithSources(programs[3], inp3, out3)
        comp4 = intcodecomputer.defaultComputerWithSources(programs[4], inp4, out4)

        while True:
            res0 = comp0.run()
            res1 = comp1.run()
            res2 = comp2.run()
            res3 = comp3.run()
            res4 = comp4.run()

            if res4 == intcodecomputer.TERMINATE:
                output.append(inp0.values[-1])
                break

        outputs.append(output)

def part1():
    for phaseSettings in itertools.permutations(list(range(5))):

        programs = [data[:] for x in range(5)]

        output = [[phaseSettings]]

        # part 1 Wire
        inp4 = [phaseSettings[4]]
        out4 = intcodecomputer.ArrayOutput(output)
        comp4 = intcodecomputer.defaultComputerWithSources(programs[4], intcodecomputer.ArrayInput(inp4), out4)

        inp3 = [phaseSettings[3]]
        out3 = intcodecomputer.ArrayOutput(inp4)
        comp3 = intcodecomputer.defaultComputerWithSources(programs[3], intcodecomputer.ArrayInput(inp3), out3)

        inp2 = [phaseSettings[2]]
        out2 = intcodecomputer.ArrayOutput(inp3)
        comp2 = intcodecomputer.defaultComputerWithSources(programs[2], intcodecomputer.ArrayInput(inp2), out2)

        inp1 = [phaseSettings[1]]
        out1 = intcodecomputer.ArrayOutput(inp2)
        comp1 = intcodecomputer.defaultComputerWithSources(programs[1], intcodecomputer.ArrayInput(inp1), out1)

        inp0 = intcodecomputer.ArrayInput([phaseSettings[0], 0])
        out0 = intcodecomputer.ArrayOutput(inp1)
        comp0 = intcodecomputer.defaultComputerWithSources(programs[0], inp0, out0)

        # Run
        comp0.run()
        comp1.run()
        comp2.run()
        comp3.run()
        comp4.run()

        outputs.append(output)

# part1()
part2()

m = (None, None)

for o in outputs:
    p, v = m

    if (v == None):
        m = (o[0], o[1])
    elif(o[1] > v):
        m = (o[0], o[1])

print(m)

