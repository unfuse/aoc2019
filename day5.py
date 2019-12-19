import csv, intcodecomputer

with open("input5.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]


# 1 for 5.1, and 5 for 5.2
intcodecomputer.defaultInteractiveComputer(data).run()


