import random
import numpy as np
def generate_tspfile(vertnumber):

    minVer = 2
    maxVer = 100
    NumberOfvertices = vertnumber#random.randrange(int(minVer), int(maxVer))

    maxVal = 3000


    fName = 'test'+str(NumberOfvertices)

    print(NumberOfvertices)
    # generowanie do pliku txt:
    file = open(fName + ".txt", "w+")
    file.write(str(NumberOfvertices) + "\n")

    for i in range(1, NumberOfvertices + 1):
        coords = np.random.randint(1, maxVal, 2)
        print(str(i) + " " + str(coords[0]) + " " + str(coords[1]))
        file.write(str(i) + " " + str(coords[0]) + " " + str(coords[1]) + "\n")
