import managerTSP as tsp
import math
import random
import time
import matplotlib.pyplot as plt
import datetime

class GeneticAlgorithmTSP:
    def __init__(self, file):
        self.file = file

    # Main method.
    def GeneticMetaheuristicsTSP(self, generations_number, population_size, elite_rate, mutation_rate,
                                 greedynumber_start, endtime_seconds):
        start_time = time.perf_counter()
        numlisty, start_list = self.create_initlist_usingManagerTSP()
        # print(start_list)
        # For every 100th generation we put the best result into a special list in order to create a chart
        fkcja_celu_list = []
        best_tour_list = []

        # Choice to start: either from random or greedy. in the second one you can see that the genetic perform better
        # population = self.first_population(start_list, population_size)
        population = self.first_populationWithGreedy(start_list, population_size, greedynumber_start)

        population.sort(key=self.calc_distance)
        bestSoFar = self.calc_distance(population[0])
        best_tour_list = population[0]
        print('First generation')
        print(bestSoFar)
        fkcja_celu_list.append(bestSoFar)
        generations_completed = 1
        stop_counter = 0

        # Create new generations
        for i in range(1, generations_number):

            # Calculation of the metaherustics time.
            time_counter = time.perf_counter() - start_time  # time in seconds

            self.new_generation(population, population_size, elite_rate, mutation_rate)
            population.sort(key=self.calc_distance)

            if i % 100 == 0:
                'print("Generation " + str(i))'
                'print(best_tour_list)'
                tempodl = self.calc_distance(population[0])
                fkcja_celu_list.append(tempodl)
                generations_completed = i

            if self.calc_distance(population[0]) < bestSoFar:
                bestSoFar = self.calc_distance(population[0])
                best_tour_list = population[0]
                print("Generation " + str(i))
                print(best_tour_list)
                print(bestSoFar)
                print("_____________________________")
                stop_counter = 0
            else:
                stop_counter += 1

            # Section: Stop conditions for metaheuristic
            if int(time_counter) >= endtime_seconds or stop_counter == 1500:
                # 15 minutes or 2000 generations without progress
                print('The stop condition has terminated the metaherustics.')
                return bestSoFar, fkcja_celu_list, generations_completed, best_tour_list



        return bestSoFar, fkcja_celu_list, generations_completed, best_tour_list

    def euclidean_dist(self, p1, p2):
        p1[0] = int(p1[0])
        p1[1] = int(p1[1])
        p2[0] = int(p2[0])
        p2[1] = int(p2[1])
        return math.sqrt(((p1[0] - p2[0]) * (p1[0] - p2[0])) + ((p1[1] - p2[1]) * (p1[1] - p2[1])))

    def calc_distance(self, tour):
        fkcja_celu = 0
        for i in range(1, len(tour)):
            fkcja_celu += self.euclidean_dist(tour[i - 1], tour[i])
        fkcja_celu += self.euclidean_dist(tour[-1], tour[0])

        return fkcja_celu

    def create_initlist_usingManagerTSP(self):
        x = tsp.ManagerTSP(self.file)
        num = []  # 1 element only
        listnum = []
        x.read_tspfile(num, listnum)

        city_list = []  # init the list of city coordinates
        for i in range(0, len(listnum)):
            city_list.append([listnum[i][1], listnum[i][2]])
        return (listnum, city_list)

    def first_population(self, start_list, pop_size):
        population = []
        for i in range(pop_size):
            population.append(start_list[:])
            random.shuffle(population[i])
        return population

    def first_populationWithGreedy(self, start_list, pop_size, greedynumber):

        population = []
        x = tsp.ManagerTSP(self.file)
        num = []  # 1 element only
        list_num = []

        x.read_tspfile(num, list_num)
        greedy_results = []
        for g in range(0, greedynumber):
            greedy = x.greedy_forGA(g + 1)
            greedy_results.append(greedy)

        for i in range(pop_size - greedynumber):
            population.append(start_list[:])
            random.shuffle(population[i])

        for i in range(0, greedynumber):
            m = greedy_results[i]
            # print(m)
            city_list = []
            for j in range(0, len(m)):
                x = list_num[int(m[j]) - 1][1]
                y = list_num[int(m[j]) - 1][2]
                city_list.append([int(x), int(y)])

            population.append(city_list)
        return population

    # Crossovers section
    def clipping_crossover(self, father, mother):

        flen = len(father)
        mlen = len(mother)

        father_sizeofcut = random.randrange(1, flen - 1)
        father_cutpoint = flen - father_sizeofcut
        father_cutstart = random.randrange(0, father_cutpoint)
        father_cutstartend = father_cutstart + father_sizeofcut
        father_cut = father[father_cutstart:father_cutstartend]

        mother_sizeofcut = random.randrange(1, mlen - 1)
        mother_cutpoint = mlen - mother_sizeofcut
        mother_cutstart = random.randrange(0, mother_cutpoint)
        mother_cutstartend = mother_cutstart + mother_sizeofcut
        mother_cut = mother[mother_cutstart:mother_cutstartend]

        # Tworzymy dzieci:
        child1 = [city for city in mother if city not in father_cut]  # Tworzymy dziecko poczatkowo jako wycinek
        bestlength = self.calc_distance(father)
        usechild = []
        usechild.extend(father)
        for j in range(len(child1)):
            temp_child = []
            temp_child.extend(child1)
            for i in range(len(father_cut)):
                temp_child.insert(j + i, father_cut[i])
            testlength = self.calc_distance(temp_child)
            if testlength < bestlength:
                usechild = []
                usechild.extend(temp_child)
                bestlength = testlength

        child1 = []
        child1.extend(usechild)

        child2 = [city for city in father if city not in mother_cut]

        bestlength = self.calc_distance(mother)
        usechild = []
        usechild.extend(mother)
        for j in range(len(child2)):
            temp_child = []
            temp_child.extend(child2)
            for i in range(len(mother_cut)):
                temp_child.insert(j + i, mother_cut[i])
            testlength = self.calc_distance(temp_child)
            if testlength < bestlength:
                usechild = []
                usechild.extend(temp_child)
                bestlength = testlength

        child2 = []
        child2.extend(usechild)

        return (child1, child2)  # return the two children

    def IGX_crossover(self, fatherlist, motherlist):
        stepcounter = len(fatherlist)
        childlist = []
        fatherdll = tsp.DCLL()
        for i in range(0, len(fatherlist)):
            fatherdll.append(fatherlist[i])

        motherdll = tsp.DCLL()
        for i in range(0, len(fatherlist)):
            motherdll.append(motherlist[i])

        for i in range(0, len(motherlist) - 1):
            if i == 0:
                first = random.choice(fatherlist)
                ind = fatherdll.getindex(stepcounter, first)
                indm = motherdll.getindex(stepcounter, first)

                t = []
                fneighs = fatherdll.getleftright(stepcounter, first)
                mneighs = motherdll.getleftright(stepcounter, first)

                t.append(fneighs)
                t.append(mneighs)
                candidateslist = [item for sublist in t for item in sublist]
                for i in range(0, len(candidateslist)):
                    val = self.euclidean_dist(first, candidateslist[i])
                    if i == 0:
                        mindistance = val
                        vertice = candidateslist[i]
                    else:
                        if val < mindistance:
                            mindistance = val
                            vertice = candidateslist[i]

                childlist.append(first)
                stepcounter = stepcounter - 1
                fatherdll.remove(ind)
                motherdll.remove(indm)

                childlist.append(vertice)
            else:
                ind = fatherdll.getindex(stepcounter, vertice)
                indm = motherdll.getindex(stepcounter, vertice)
                t = []
                fneighs = fatherdll.getleftright(stepcounter, vertice)
                mneighs = motherdll.getleftright(stepcounter, vertice)
                t.append(fneighs)
                t.append(mneighs)
                candidateslist = [item for sublist in t for item in sublist]
                verttemp = vertice
                for i in range(0, len(candidateslist)):
                    val = self.euclidean_dist(verttemp, candidateslist[i])
                    if i == 0:
                        mindistance = val
                        vertice = candidateslist[i]
                    else:
                        if val < mindistance:
                            mindistance = val
                            vertice = candidateslist[i]
                childlist.append(vertice)
                stepcounter = stepcounter - 1
                fatherdll.remove(ind)
                motherdll.remove(indm)

        return childlist

    def simpleCrossover(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)
        for i in range(startGene, endGene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]
        child = childP1 + childP2
        return child

    def mutate(self, individual):
        i = random.randrange(0, len(individual))
        j = random.randrange(0, len(individual))

        temp = individual[i]
        individual[i] = individual[j]
        individual[j] = temp

    def greedy_mutations(self, list):

        mut_list = []
        mut_list.extend(list)
        rng = random.randrange(0, len(list))
        city = list[rng]

        fkcja_celu = self.calc_distance(list)
        for i in range(len(list)):

            if i == 0:
                list.pop(rng)
            else:
                list.pop(i - 1)

            list.insert(i, city)
            tmpfkcja_celu = self.calc_distance(list)
            if tmpfkcja_celu < fkcja_celu:
                return list
        return mut_list

    def new_generation(self, population, populationSize, eliteRate, mutationRate):

        fraction_point = (random.randrange(50, 950)) / 1000
        fraction_point = eliteRate

        father = random.choice(population[:int(populationSize * fraction_point)])
        mother = random.choice(population[:int(populationSize * fraction_point)])

        # CROSSOVER METHODS AFFECTING THE RESULT
        # 1 crossover: clipping method
        # (child1, child2) = self.clipping_crossover (father, mother)

        # 2 metoda crossover: IGX - better one
        father2 = random.choice(population[:int(populationSize * fraction_point)])
        mother2 = random.choice(population[:int(populationSize * fraction_point)])
        child1 = self.IGX_crossover(father, mother)
        child2 = self.IGX_crossover(father2, mother2)

        self.greedy_mutations(child1)
        self.greedy_mutations(child2)

        if self.calc_distance(child1) < self.calc_distance(population[populationSize - 2]):
            population[populationSize - 2] = child1
        if self.calc_distance(child2) < self.calc_distance(population[populationSize - 1]):
            population[populationSize - 1] = child2

        # To prevent local optima, randomly mutate a city on occasion
        if random.random() < mutationRate:
            tour = random.randrange(1, len(population))
            self.mutate(population[tour])

start_time = datetime.datetime.now()
def simple_plot(lista, instance_name, tourlist):
    length = len(lista)



    fig, ax = plt.subplots()
    last = len(tourlist) - 1
    for i in range(1, len(tourlist)):
        temp_listx = [tourlist[i - 1][0], tourlist[i][0]]
        temp_listy = [tourlist[i - 1][1], tourlist[i][1]]
        ax.plot(temp_listx, temp_listy, 'g')
        ax.scatter(temp_listx[0], temp_listy[0], s=10, c='red')
        ax.scatter(temp_listx[1], temp_listy[1], s=10, c='red')
    temp_listx = [tourlist[last][0], tourlist[0][0]]
    temp_listy = [tourlist[last][1], tourlist[0][1]]
    ax.plot(temp_listx, temp_listy, 'g')
    ax.scatter(temp_listx[0], temp_listy[0], s=10, c='red')
    ax.scatter(temp_listx[1], temp_listy[1], s=10, c='red')


    end_time=datetime.datetime.now()- start_time;
    print("--- %s seconds ---" % (end_time.total_seconds()))

    ax.set_title("Best founded route for the " + str(instance_name).replace('.txt', '').replace('instances/','')+" instance.")
    print(tourlist)
    plt.show()



def main():
    folder ="instances/"
    instance_name = folder+"test8.txt"
    w = GeneticAlgorithmTSP(instance_name)

    #Tuning parameters
    generations_number = 10001
    population_size = 20
    elite_rate = 0.3  # values between <0;1>
    mutation_rate = 0.80  # values between  <0;1>
    greedyatstart = 1  # 0 if you dont want to have any greedy solution at the start.
    endafter = 90  # time in seconds

    # Initialization
    numlisty, start_list = w.create_initlist_usingManagerTSP()
    # Genetic Algorithm
    (best, lista, gen_compl, tourlist) = w.GeneticMetaheuristicsTSP(generations_number, population_size, elite_rate,
                                                                    mutation_rate,
                                                                    greedyatstart, endafter)
    # Plot drawing + bonus for most common instance

    simple_plot(lista, instance_name, tourlist)


if __name__ == "__main__":
    main()
