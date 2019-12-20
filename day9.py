import csv, intcodecomputer, sys

with open("input9.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

# data = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

intcodecomputer.defaultInteractiveComputer(data).run()