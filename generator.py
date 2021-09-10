import random
import numpy as np

#Very simple instance generator
def generate_tspfile(vertnumber):
    # Pod tymi zmiennymi edytuj zakres do wylosowanej ilosci wierzcholkow lub po prostu zmien wartosc NumberOfvertices
    minVer = 2
    maxVer = 100
    NumberOfvertices = vertnumber#random.randrange(int(minVer), int(maxVer))

    # Pod ta zmienna mozesz zmienic najwieksza mozliwa wartosc do wylosowania dla wspolrzednych x i y
    maxVal = 3000

    ## podanie nazwy rodzaju generacji [jesli tak wolimy]
    #print("Podaj podtytul dla wygenerowanego pliku:")
    fName = 'in'+str(NumberOfvertices)

    print(NumberOfvertices)
    # generowanie do pliku txt:
    file = open(fName + ".txt", "w+")
    file.write(str(NumberOfvertices) + "\n")

    for i in range(1, NumberOfvertices + 1):
        coords = np.random.randint(1, maxVal, 2)
        print(str(i) + " " + str(coords[0]) + " " + str(coords[1]))
        file.write(str(i) + " " + str(coords[0]) + " " + str(coords[1]) + "\n")
