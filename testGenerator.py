import random

# Script for generation new instances + some greedy solution test.
import managerTSP as tsp
import generator

generator.generate_tspfile(12)

filename = "instances/test12.txt"

x = tsp.ManagerTSP(filename)
num = []  # 1 element only
listnum = []
x.read_tspfile(num, listnum)

# print(listnum)

a = x.calc_distances()
for i in a:
    print(i)

# print(num[0])
# print(listnum)

# x.print_tspfile()
x.greedy_tsp(1)

tt = x.greedy_forGA(1)
print(tt)
