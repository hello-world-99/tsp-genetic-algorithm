import csv
import numpy as np
from operator import itemgetter
import math


# klasa wykorzystywana do rozwiazania zachlannego
# zawiera:
# odczyt instancji metodą. Argumenty to plik, i moze zmienne pod ktorymi maja byc zapisane dane z pliku

# toString czyli wypisanie wczytanej instancji

# proste greedy rozwiazanie

class ManagerTSP:

    def __init__(self, file):  # demo konstruktor. ewentualnie zmienic
        self.file = file

    def read_tspfile(self, vert_number, vert_list):

        with open(self.file) as csvfile:
            for i, line in enumerate(csvfile):
                if i == 0:
                    vert_number.append(int(line.rstrip()))

                else:
                    vert_list.append(line.rstrip().split())

        """* przyklad uzycia    read_tspfile
        x = tsp.ManagerTSP("1_instance.txt")
        num = []  # 1 element only
        listnum = []
        x.read_tspfile(num, listnum)
        print(num[0])
        print(listnum)
        """

    def print_tspfile(self):
        print("-------------Odczytany plik zawiera ponizsze informacje: ---------------")
        with open(self.file) as csvfile:
            for i, line in enumerate(csvfile):
                print(line)
        print("------------Plik zostal odczytany--------------------")
        # TODO dodac tu tez printowanie punktow w ukladzie wspolrzednych dla wizualizacji otrzymanej instancji

    def euclidean_dist(self, x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))

    def euclidean_distint(self, x1, y1, x2, y2):  # dla wiekszych odleglosci lepiej po prostu int chyba
        return int(math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1))))

    def calc_distlist(self, all_distances,
                      vert_list):  # jako argumenty nowa lista w ktorej dostaniesz odleglosci oraz koniecznie vert_list

        for pktnr in range(0, len(vert_list)):
            xp = int(vert_list[pktnr][1])
            yp = int(vert_list[pktnr][2])
            odleglosci = []
            for i in range(0, len(vert_list)):
                nr = i + 1
                # liczba = int(greedy_list[pktnr][0])  # dla 10 pierwszy arg to od 0 do 9

                # if nr != liczba:
                x_temp = int(vert_list[i][1])
                y_temp = int(vert_list[i][2])
                odleglosci.append(self.euclidean_dist(xp, yp, x_temp, y_temp))

            all_distances.append(odleglosci)
        # print(all_distances)

    def calc_distances(self):  # jako argumenty nowa lista w ktorej dostaniesz odleglosci oraz koniecznie vert_list
        vert_list = []
        all_distances = []
        self.read_tspfile(all_distances, vert_list)
        for pktnr in range(0, len(vert_list)):
            xp = int(vert_list[pktnr][1])
            yp = int(vert_list[pktnr][2])
            distances = []
            for i in range(0, len(vert_list)):
                nr = i + 1
                # if nr != liczba:
                x_temp = int(vert_list[i][1])
                y_temp = int(vert_list[i][2])
                distances.append(self.euclidean_dist(xp, yp, x_temp, y_temp))

            all_distances.append(distances)
        return all_distances

    def distance_between(self, from_point, to_point):
        distance_list = self.calc_distances()[1:]
        from_point = from_point - 1
        to_point = to_point - 1
        return distance_list[from_point][to_point]

    def turbo_greedy(
            self):  # wykonanie greedy tyle razy ile liczba wierzcholkow szukajac od ktorego najkorzystniej zaczac i podajacy taka najmniejsza fkcje celu
        num = []
        listT = []
        self.read_tspfile(num, listT)  # dla zdobycia info o l. wierzcholkow

        vert_amount = int(num[0])
        # print(vert_amount)

        # dla wszystkich punktow
        for i in range(1, vert_amount + 1):
            if i == 1:
                wynik = self.greedy_cleaned(i)
                best_tour = wynik[1]
                best_fkcja_celu = wynik[0]
                vert_best = 1
            else:
                wynik = self.greedy_cleaned(i)
                # print(wynik) #sprawdzanie dla dociekliwych
                if wynik[0] < best_fkcja_celu:
                    best_fkcja_celu = wynik[0]
                    best_tour = wynik[1]
                    vert_best = i

        print(best_tour)
        print(round(best_fkcja_celu,2))
        # print(vert_best) # wierzcholek dla ktorego jest najlepszy wynik

    def greedy_tsp(self, startV):  # implementacja wlasna + dodatkowy argument okreslajacy wierzcholek startowy
        '''
            (wybierz jako arg. wierzcholek startowy) lub
             startuj z punktu 1
            za kazdym razem poki zostal jakis wierzcholek odwiedz najblizszy wierzcholek ktory jest jeszcze
             nieodwiedzony
        '''
        greedy_num = []
        greedy_list = []
        self.read_tspfile(greedy_num,
                          greedy_list)  # num[0] to liczba wierzcholkow, list  zaczyna sie od zera i zawiera wspolrzedne
        # dla kazdego pktu stworz liste odleglosci do wierzcholkow:
        # taka lista nie zawiera siebie samego

        all_distances = []
        self.calc_distlist(all_distances, greedy_list)
        print(all_distances)
        vert_amount = int(greedy_num[0])

        # Walidacja argumentu: czy obiekt z wczytana daną zawiera punkt o takim numerze
        if startV > vert_amount or startV < 1:
            print(
                "Podano bledna wartosc dla startowego wierzcholka. Sprawdz czy twoj plik zawiera wierzcholek o podanym numerze")
        else:
            # wlasciwa czesc algorytmu:
            # wybieramy wierzcholek startowy

            # Wazna linijka wplywajaca na jakosc wyniku zachlannego = wierzcholek startowy
            start_vert = startV  # numeracja od 1 do num

            # lista czy odwiedzony
            is_visited_list = [0] * int(greedy_num[0])
            is_visited_list[start_vert - 1] = 99
            print(is_visited_list)

            fkcja_celu = 0
            # dopoki wszystkie nie  sa odwiedzone odwiedz najblizszy jeszcze nieodwiedzony + sumuj do odleglosci calkowitej
            tour = [start_vert]  # tu beda pkty w kolejnosci przechodzenia
            # indeksy is_visited maja byc w takiej samej notacji jak indeksy odleglosc w podliscie listy all_distances
            # print("////////////////////")
            verts = start_vert - 1  # startowy

            for krok in range(0, vert_amount):  # liczba punktow to liczba krokow zawsze, w ostatnim powraca

                # print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
                if krok == vert_amount - 1:  # ostatni krok wraca do punktu startu
                    # tu dodaj wartosc z listy odleglosc wskazujaca na odleglosc z ostatniego punktu do punktu poczatkowego
                    print(all_distances[verts][start_vert-1])
                    fkcja_celu += all_distances[verts][start_vert - 1]
                    tour.append(start_vert)

                else:

                    if not is_visited_list[verts] == 0:
                        print((all_distances[verts]))
                        val, idx = max((val, idx) for (idx, val) in enumerate(all_distances[verts]))
                        print(val)  #dane kontrolne
                        print(idx)
                        for i in range(0, len(all_distances[verts])):
                            if all_distances[verts][i] < val and all_distances[verts][i] != 0 and is_visited_list[i] == 0:
                                val = all_distances[verts][i]
                                idx = i
                        print(val)  # najm odleglosc  dane kontrolne
                        print(idx)
                        tour.append(idx + 1)
                        fkcja_celu += val
                        is_visited_list[idx] = 1

                        print(is_visited_list)
                    print(fkcja_celu)
                    print(tour)
                    # old=verts
                    verts = idx
                print("Funkcja celu wynosi: "+str(fkcja_celu))
                print("kolejnosc wierzcholkow:" + str(tour))
            print("........................................")
            print("Dla algorytmu zachlannego Funkcja celu wynosi: " + str(fkcja_celu))
            print("Ostateczna kolejnosc wierzcholkow:" + str(tour))
            print("........................................")

    def greedy_cleaned(self,
                       startV):  # do uzywana wersji turbo albo jak z jakiegos powodu nie potrzebujesz printa + ogolne zwiekszenie przejrzystosci i zwracanie wartosci
        greedy_num = []
        greedy_list = []
        self.read_tspfile(greedy_num,
                          greedy_list)  # num[0] to liczba wierzcholkow, list  zaczyna sie od zera i zawiera wspolrzedne
        # dla kazdego pktu stworz liste odleglosci do wierzcholkow:
        # taka lista nie zawiera siebie samego
        all_distances = []
        self.calc_distlist(all_distances, greedy_list)
        # print(all_distances)
        vert_amount = int(greedy_num[0])
        # Walidacja argumentu: czy obiekt z wczytana daną zawiera punkt o takim numerze
        if startV > vert_amount or startV < 1:
            print(
                "Podano bledna wartosc dla startowego wierzcholka. Sprawdz czy twoj plik zawiera wierzcholek o podanym numerze")
        else:
            # wlasciwa czesc algorytmu:
            # wybieramy wierzcholek startowy
            # Wazna linijka wplywajaca na jakosc wyniku zachlannego = wierzcholek startowy
            start_vert = startV  # numeracja od 1 do num
            # lista czy odwiedzony
            is_visited_list = [0] * int(greedy_num[0])
            is_visited_list[start_vert - 1] = 99
            fkcja_celu = 0
            # dopoki wszystkie nie  sa odwiedzone odwiedz najblizszy jeszcze nieodwiedzony + sumuj do odleglosci calkowitej
            tour = [start_vert]  # tu beda pkty w kolejnosci przechodzenia
            # indeksy is_visited maja byc w takiej samej notacji jak indeksy odleglosc w podliscie listy all_distances
            verts = start_vert - 1  # startowy
            for krok in range(0, vert_amount):  # liczba punktow to liczba krokow zawsze, w ostatnim powraca
                if krok == vert_amount - 1:  # ostatni krok wraca do punktu startu
                    fkcja_celu += all_distances[verts][start_vert - 1]
                    tour.append(start_vert)
                else:
                    if not is_visited_list[verts] == 0:
                        val, idx = max((val, idx) for (idx, val) in enumerate(all_distances[verts]))
                        for i in range(0, len(all_distances[verts])):
                            if all_distances[verts][i] < val and all_distances[verts][i] != 0 and is_visited_list[i] == 0:
                                val = all_distances[verts][i]
                                idx = i
                        tour.append(idx + 1)
                        fkcja_celu += val
                        is_visited_list[idx] = 1
                    verts = idx
            return [fkcja_celu, tour]

    def greedy_forGA(self,startV):  # do uzywana wersji turbo albo jak z jakiegos powodu nie potrzebujesz printa + ogolne zwiekszenie przejrzystosci i zwracanie wartosci
            greedy_num = []
            greedy_list = []
            self.read_tspfile(greedy_num,
                              greedy_list)  # num[0] to liczba wierzcholkow, list  zaczyna sie od zera i zawiera wspolrzedne
            # dla kazdego pktu stworz liste odleglosci do wierzcholkow:
            # taka lista nie zawiera siebie samego
            all_distances = []
            self.calc_distlist(all_distances, greedy_list)
            # print(all_distances)
            vert_amount = int(greedy_num[0])
            # Walidacja argumentu: czy obiekt z wczytana daną zawiera punkt o takim numerze
            if startV > vert_amount or startV < 1:
                print(
                    "Podano bledna wartosc dla startowego wierzcholka. Sprawdz czy twoj plik zawiera wierzcholek o podanym numerze")
            else:
                # wlasciwa czesc algorytmu:
                # wybieramy wierzcholek startowy
                # Wazna linijka wplywajaca na jakosc wyniku zachlannego = wierzcholek startowy
                start_vert = startV  # numeracja od 1 do num
                # lista czy odwiedzony
                is_visited_list = [0] * int(greedy_num[0])
                is_visited_list[start_vert - 1] = 99
                fkcja_celu = 0
                # dopoki wszystkie nie  sa odwiedzone odwiedz najblizszy jeszcze nieodwiedzony + sumuj do odleglosci calkowitej
                tour = [start_vert]  # tu beda pkty w kolejnosci przechodzenia
                # indeksy is_visited maja byc w takiej samej notacji jak indeksy odleglosc w podliscie listy all_distances
                verts = start_vert - 1  # startowy
                for krok in range(0, vert_amount):  # liczba punktow to liczba krokow zawsze, w ostatnim powraca
                    if krok == vert_amount - 1:  # ostatni krok wraca do punktu startu
                        fkcja_celu += all_distances[verts][start_vert - 1]
                        #tour.append(start_vert)
                    else:
                        if not is_visited_list[verts] == 0:
                            val, idx = max((val, idx) for (idx, val) in enumerate(all_distances[verts]))
                            for i in range(0, len(all_distances[verts])):
                                if all_distances[verts][i] < val and all_distances[verts][i] != 0 and is_visited_list[
                                    i] == 0:
                                    val = all_distances[verts][i]
                                    idx = i
                            tour.append(idx + 1)
                            fkcja_celu += val
                            is_visited_list[idx] = 1
                        verts = idx
                return tour



#Sekcja Double Linked List i Crossover Algorithm
class Node:
    def __init__(self, data = None):
        self.data = data
        self.previous = self
        self.next = self


class DCLL:
    def __init__(self):
        self.head = None
        self.count = 0

    def __repr__(self):
        string = ""

        if (self.head == None):
            string += "Doubly Circular Linked List Empty"
            return string

        string += f"Doubly Circular Linked List:\n{self.head.data}"
        temp = self.head.next
        while (temp != self.head):
            string += f" -> {temp.data}"
            temp = temp.next
        return string

    def append(self, data):
        self.insert(data, self.count)
        return

    def insert(self, data, index):
        if (index > self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.head == None:
            self.head = Node(data)
            self.count = 1
            return

        temp = self.head
        if (index == 0):
            temp = temp.previous
        else:
            for _ in range(index - 1):
                temp = temp.next

        temp.next.previous = Node(data)
        temp.next.previous.next, temp.next.previous.previous = temp.next, temp
        temp.next = temp.next.previous
        if (index == 0):
            self.head = self.head.previous
        self.count += 1
        return

    def remove(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.count == 1:
            self.head = None
            self.count = 0
            return

        target = self.head
        for _ in range(index):
            target = target.next

        if target is self.head:
            self.head = self.head.next

        target.previous.next, target.next.previous = target.next, target.previous
        self.count -= 1

    def index(self, data):
        temp = self.head
        for i in range(self.count):
            if (temp.data == data):
                return i
            temp = temp.next
        return None

    def get(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp.data

    def size(self):
        return self.count

    def display(self):
        print(self)

#Methods prepared for the project
# get prev i next
    def getp(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        temp = self.head
        for _ in range(index):
            temp = temp.next
        print("liczba: "+str(temp.data))
        print("prev: " + str(temp.previous.data))
        print("next: " + str(temp.next.data))

# get index
    def getindex(self, rangelist,value):

        for index in range(0,rangelist):

            if (index >= self.count) | (index < 0):
                raise ValueError(f"Index out of range: {index}, size: {self.count}")

            temp = self.head
            for _ in range(index):
                temp = temp.next
            if(temp.data==value):
                return index

#Get neighbours of element for IGX crossover.
    def getleftright(self, rangelist, value):
        list = []
        for index in range(0, rangelist):

            if (index >= self.count) | (index < 0):
                raise ValueError(f"Index out of range: {index}, size: {self.count}")

            temp = self.head
            for _ in range(index):
                temp = temp.next
            if (temp.data == value):
                list.append(temp.previous.data)
                list.append(temp.next.data)
                return list

