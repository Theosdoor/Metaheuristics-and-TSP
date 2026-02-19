import random
import time
from tqdm import tqdm

algorithm_code = "GA"

def run(num_cities, dist_matrix, time_limit=None):
    start_time = time.time()
    # Genetic algorithm ENHANCED
    timed = time_limit is not None
    added_note = ""
    if timed:
        added_note += "Time limit = " + str(time_limit) + " seconds.\n"

    # for added NOTE
    first_best_update = 0 # iteration of first best tour update
    last_best_update = 0 # iteration of last best tour update

    # define core parameters
    max_it = 2000 # max number of generations
    pop_size = 250 # |P|
    # p_mutation - small probability of mutation
    # change dynamically if certain conditions met (see MAIN LOOP)
    # REQUIRE p1 < p2 < p3 < p4
    p1 = 0.2
    p_mutation = p1 # same as AlgAbasic
    p2 = 0.3
    p2_thresh = 0.15*max_it
    p3 = 0.4
    p3_thresh = 0.25*max_it
    p4 = 0.5
    p4_thresh = 0.5*max_it
    # homogeneity
    hom_thresh = 0.9 * pop_size # num individuals with same fitness to classify P as homogeneous
    homogeneous = False

    added_note += "Starting p_mutation = " + str(p_mutation) + ".\n"

    # uninitialised variables
    sat_tour_length = 0 # tour length at which to stop and return best tour so far

    # define function for getting tour length
    def get_tour_length(tour):
        '''
        Returns length of given partial/complete tour.

        O(n), n = cities in tour (= num_cities if tour complete)
        '''
        # sum distances between each city in tour
        length = 0
        for i in range(len(tour) - 1):
            length += dist_matrix[tour[i]][tour[i + 1]]
        # if tour is complete, add dist back to start city
        if len(tour) == num_cities:
            length += dist_matrix[tour[num_cities - 1]][tour[0]]
        return length

    # define f_min function to use GA to minimise tour length
    def get_f_mins(P, tau=1):
        '''
        Fitness function to maximise.
        Returns fitness of individuals in P.

        Strategy: f_min = tau - tour length
        Note: tau must be strictly greater than any individual tour length.
            Default tau = 1 is arbitrary initial value.

        Shorter tour ==> greater f_min
        Tau too large ==> P's fitness values 'pushed together'
        Different tau b/t populations ==> cannot reliably compare b/t populations
            ==> must update f_min(best) if tau changes
        '''
        tour_lengths = [get_tour_length(i) for i in P]
        # update tau to be larger than any individual length
        tau = max(tour_lengths) + 1
        return [(tau - l) for l in tour_lengths], tau

    def roulette_wheel(P, probs):
        '''
        Select parent from P according to given probabilities
            using roulette wheel approach.
        '''
        # divide wheel into proportional sectors
        sector_angles = [p * 360 for p in probs]
        # spin wheel!
        spin_angle = random.uniform(0, 360)

        # find sector the wheel lands on
        sector = 0
        while spin_angle > sector_angles[sector]:
            spin_angle -= sector_angles[sector]
            sector += 1

        return P[sector]

    # define crossover
    def crossover(X, Y):
        '''
        Sequential constructive crossover (SCX) operator.

        Given two parents from P, return child Z1
            which inherits 'traits' from both parents
            while introducing some new edges which supports diversity.

        Note: easily adaptable to produce two children Z1, Z2
            where Z2 has same start city as Y.
            (MAIN LOOP will also have to be slightly adjusted)

        O(n), n = num_cities

        REFERENCE (pseudocode)
        ---------
        Ahmed, Zakir (2010)
        Genetic Algorithm for the Traveling Salesman Problem using Sequential Constructive Crossover Operator.
        International Journal of Biometric and Bioinformatics. 3. 10.14569/IJACSA.2020.0110275.
        https://www.researchgate.net/publication/41847011_Genetic_Algorithm_for_the_Traveling_Salesman_Problem_using_Sequential_Constructive_Crossover_Operator
        '''
        # init children
        Z1 = [X[0]]
        # Z2 = [Y[0]] # can repeat loop below with Z2 to get two offspring

        # while Z1 not complete
        while len(Z1) < num_cities:
            current = Z1[-1] # current city, p

            # get next city in X, c_X
            X_next_pos = (X.index(current) + 1) % num_cities
            X_next = X[X_next_pos]
            # if already visited, get next unvisited city in X
            # Note: this step introduces new edges
            while X_next in Z1:
                X_next_pos = (X_next_pos + 1) % num_cities
                X_next = X[X_next_pos]

            # get next city in Y, c_Y
            Y_next_pos = (Y.index(current) + 1) % num_cities
            Y_next = Y[Y_next_pos]
            # if already visited, get next unvisited city in Y
            while Y_next in Z1:
                Y_next_pos = (Y_next_pos + 1) % num_cities
                Y_next = Y[Y_next_pos]

            # compare distances c_X < c_Y
            if dist_matrix[current][X_next] < dist_matrix[current][Y_next]:
                Z1.append(X_next)
            else:
                Z1.append(Y_next)

        return Z1

    # define mutation
    def mutate(Z):
        '''
        Mutate the given individual Z by
            randomly swapping two cities in the tour.

        Note: modifies Z inplace

        O(1) - constant time
        '''
        # pick two random indices i, j
        # (may have i = j)
        i = random.randint(0, num_cities - 1)
        j = random.randint(0, num_cities - 1)

        # swap cities
        Z[i], Z[j] = Z[j], Z[i]

    # function for nearest neighbour tour & length
    def nearest_neighbours(start_city=None):
        '''
        Basic greedy search for shortest tour, 
            starting from random or specified city.

        Complexity: O(n^2), n = num_cities
        '''
        # pick start city
        if start_city is None:
            nn_tour = [random.randint(0, num_cities - 1)]
        else:
            nn_tour = [start_city]

        # maintain list of unvisited cities
        unvisited = list(range(num_cities))
        unvisited.remove(nn_tour[0])

        # while tour not complete
        nn_length = 0
        while len(nn_tour) < num_cities:
            # get distances from current city
            current = nn_tour[-1]
            distances = dist_matrix[current]

            # get nearest unvisited city
            nearest = unvisited[0]
            for city in unvisited[1:]:
                if distances[city] < distances[nearest]:
                    nearest = city
        
            # add nearest to tour and remove from univisted list
            nn_tour.append(nearest)
            nn_length += distances[nearest]
            unvisited.remove(nearest)

        # add distance back to start
        nn_length += dist_matrix[nn_tour[-1]][nn_tour[0]]

        return nn_tour, nn_length

    # generate initial population as follows:
    m = 0.95 # proportion of P to be nn tours, 0 < m < 1
    num_nn = round(m * pop_size)

    # get list of unique start cities
    # get sample if too many possible start cities for nn tours
    if num_cities > num_nn:
        start_cities = random.sample(list(range(num_cities)), num_nn)
    else:
        start_cities = list(range(num_cities)) # get all possible start cities
        start_cities += random.choices(start_cities, k=num_nn - num_cities) # repeat some if necessary

    # init P
    P = []
    # fill with available nn tours in order from shortest to longest
    for i in range(num_nn):
        individual, _ = nearest_neighbours(start_cities[i])
        P.append(individual)
    # then fill remaining space with randomised tours
    for i in range(pop_size - num_nn):
        individual = list(range(num_cities)) # init tour: [0, 1, 2, ..., num_cities - 1]
        random.shuffle(individual) # shuffle cities visited in each tour
        P.append(individual)

    # init tau, fitness list, best individuals
    f_mins, tau = get_f_mins(P)
    best_fitness = max(f_mins)
    best_tour = P[f_mins.index(best_fitness)]
    best_tour_tau = tau

    # tour good enough if it is less than half the length of best tour in initial population
    # (incl NN tours)
    sat_tour_length = 0.5 * get_tour_length(best_tour)

    # MAIN LOOP until:
    # certain number of iterations done or
    # some individual is fit enough or
    # time limit reached
    with tqdm(total=max_it, desc="GA Enhanced", unit="iter") as pbar:
        for it in range(max_it):
            new_P = []

            # get probabilities for parent selection
            F = sum(f_mins) # total fitness
            probs = [f/F for f in f_mins] # probability of selection proportional to fitness

            for i in range(pop_size):
                # randomly choose two parents from P with
                # probability proportional to fitness
                # (X may = Y)
                X = roulette_wheel(P, probs)
                Y = roulette_wheel(P, probs)

                # crossover X, Y
                Z1 = crossover(X, Y)

                # with small fixed probablity mutate Z1
                if random.random() <= p_mutation:
                  mutate(Z1)
                # if random.random() <= p_mutation:
                #   mutate(Z2)

                new_P.append(Z1)
                # new_P.append(Z2)

            # update P & f_mins
            P = new_P
            f_mins, tau = get_f_mins(P, tau)

            # if tau different from that used to calulate best_fitness, recalculate f_min(best)
            if tau != best_tour_tau:
                best_fitness = tau - get_tour_length(best_tour)
                best_tour_tau = tau

            # update best with fitter individual
            temp_best_fitness = max(f_mins)
            # print("temp best tour length:", tau - temp_best_fitness)
            if temp_best_fitness > best_fitness:
                best_fitness = temp_best_fitness
                best_tour = P[f_mins.index(best_fitness)] # keep best individual in memory
                pbar.set_postfix(best_length=f'{(best_tour_tau - best_fitness):.2f}', p_mutation=f'{p_mutation:.2f}')

                # keep track of iterations where best is updated
                last_best_update = it
                if first_best_update == 0:
                    first_best_update = it

                # break if fit enough
                sat_fitness = tau - sat_tour_length
                if best_fitness >= sat_fitness:
                    break

            # check if P homogeneous
            f_min_counts = {} # dict to keep count of how often each f_min occurs
            for f in f_mins:
                if f in f_min_counts:
                    # increase count
                    f_min_counts[f] += 1
                else:
                    # add to dict, count = 1
                    f_min_counts[f] = 1
            max_count = max(f_min_counts.values()) # how often the mode of f_mins occurs

            if max_count >= hom_thresh:
                homogeneous = True
            else:
                homogeneous = False

            # update p_mutation if GA stagnates or P sufficiently homogeneous
            it_since_last_best = it - last_best_update # iterations since last update to best tour
            # increase to next p_mutation [p2, p3, ..]
            if (it_since_last_best > p2_thresh or homogeneous) and p_mutation < p2:
                # print("Increasing p_mutation to", p2, "...")
                p_mutation = p2
            elif (it_since_last_best > p3_thresh) and p_mutation < p3:
                # print("Increasing p_mutation to", p3, "...")
                p_mutation = p3
            elif (it_since_last_best > p4_thresh) and p_mutation < p4:
                # print("Increasing p_mutation to", p4, "...")
                p_mutation = p4
            else:
                # reduce p_mutation if rate of improvement increases and P sufficiently diverse
                if p_mutation > p1 and (it_since_last_best < p2_thresh) and not homogeneous:
                    # print("Reducing p_mutation...")
                    p_mutation = p1

            # break if time limit reached
            if timed and (time.time() - start_time > time_limit):
                break
            
            pbar.update(1)

    added_note += "First best tour update at it = " + str(first_best_update) + ".\n"
    added_note += "Last best tour update at it = " + str(last_best_update) + ".\n"

    # output
    tour = best_tour
    tour_length = best_tour_tau - best_fitness # tour length = tau - f_min

    try:
        param_note = f"The parameter values are 'max_it' = {max_it} and 'pop_size' = {pop_size}."
        if added_note:
            added_note += "\n" + param_note
        else:
            added_note = param_note
    except NameError:
        pass
        
    return tour, tour_length, added_note
