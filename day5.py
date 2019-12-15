import csv, intcodecomputer

with open("input5.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

intcodecomputer.defaultComputer(data).run()


