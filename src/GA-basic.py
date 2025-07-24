import random
import time

algorithm_code = "GA"

def run(num_cities, dist_matrix, time_limit=None):
    start_time = time.time()
    # Genetic algorithm BASIC
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
    p_mutation = 0.2 # small and fixed probability of mutation

    added_note += "p_mutation = " + str(p_mutation) + ".\n"

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

    # function for nearest neighbour tour & length
    def nearest_neighbours(start_city=None):
        '''
        Basic nearest neighbour search for shortest tour, 
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
            unvisited.remove(nearest)

        return nn_tour

    # If num_cities is small, try all start cities for shortest nn tour
    # otherwise use random start city for nn tour
    # NOTE n < 200 takes less than 1 second to iterate all
    if num_cities < 200:
        nn_tour = None
        nn_tour_length = float('inf')
        for i in range(num_cities):
            ith_tour = nearest_neighbours(start_city=i)
            ith_tour_length = get_tour_length(ith_tour)
            if ith_tour_length < nn_tour_length:
                nn_tour_length = ith_tour_length
                nn_tour = ith_tour
    else:
        nn_tour = nearest_neighbours()
        nn_tour_length = get_tour_length(nn_tour)

    # tour good enough if it is less than half the length of a nn tour
    sat_tour_length = 0.5 * nn_tour_length

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
        # split X, Y at random point
        split = random.randint(0, num_cities - 1)
        X_prefix, X_suffix = X[:split], X[split:]
        Y_prefix, Y_suffix = Y[:split], Y[split:]

        # create 2 children that are valid tours
        Z1 = X_prefix + Y_suffix
        Z2 = Y_prefix + X_suffix

        # if X_prefix and Y_suffix are disjoint ==> no repeat cities in Z1, Z2
        # since Y_prefix and X_suffix must also be disjoint
        if len(set(X_prefix) & set(Y_suffix)) > 0: # Z1 has repeats (so Z2 does too)
            # make Z1 a valid tour by replacing repeated cities
            replace_with = [city for city in Y_prefix if city not in X_prefix]
            for i in range(len(Y_suffix)): # work through Z1 suffix
                if Y_suffix[i] in X_prefix: # if repeated city
                    Z1[split + i] = replace_with.pop(0)
                
            # make Z2 a valid tour by replacing repeated cities
            replace_with = [city for city in X_prefix if city not in Y_prefix]
            for i in range(len(X_suffix)): # work through Z2 suffix
                if X_suffix[i] in Y_prefix: # if repeated city
                    Z2[split + i] = replace_with.pop(0)

        # return fittest child
        child_f_mins, _ = get_f_mins([Z1, Z2])
        if child_f_mins[0] > child_f_mins[1]:
            return Z1
        else:
            return Z2

    # define mutation
    def mutate(Z):
        '''
        Mutation strategy: randomly swap two elements of Z.
        NOTE may be same two elements (i = j)

        Note: modifies Z inplace
        '''
        # pick two random indices i, j
        i = random.randint(0, num_cities - 1)
        j = random.randint(0, num_cities - 1)

        # swap cities
        Z[i], Z[j] = Z[j], Z[i]

    # randomly generate initial population
    P = []
    for i in range(pop_size):
        individual = list(range(num_cities)) # init tour: [0, 1, 2, ..., num_cities - 1]
        random.shuffle(individual) # shuffle cities visited in each tour
        P.append(individual) # add tour to population

    # init tau, fitness list, best individual
    f_mins, tau = get_f_mins(P)
    best_fitness = max(f_mins)
    best_tour = P[f_mins.index(best_fitness)]
    best_tour_tau = tau

    # MAIN LOOP until:
    # certain number of iterations done or
    # some individual is fit enough or
    # time limit reached
    for it in range(max_it):
        new_P = []

        # get probabilities for parent selection
        F = sum(f_mins) # total fitness
        probs = [f/F for f in f_mins] # probability of selection proportional to fitness

        for i in range(pop_size):
            # randomly choose two parents from P with 
            # probability proportional to fitness
            # NOTE X may = Y
            X = roulette_wheel(P, probs)
            Y = roulette_wheel(P, probs)

            # crossover X and Y to produce Z
            Z = crossover(X, Y)

            # with small fixed probablity mutate Z
            k = random.random() # pick a random probability (i.e. int between 0 and 1)
            if k <= p_mutation: 
              mutate(Z)
            
            new_P.append(Z)

        # update P & f_mins
        P = new_P
        f_mins, tau = get_f_mins(P, tau)

        # if tau different from that used to calulate best_fitness, recalculate f_min(best)
        if tau != best_tour_tau:
            best_fitness = tau - get_tour_length(best_tour)
            best_tour_tau = tau

        # update best with fitter individual
        temp_best_fitness = max(f_mins)
        if temp_best_fitness > best_fitness:
            best_fitness = temp_best_fitness
            best_tour = P[f_mins.index(best_fitness)] # keep best individual in memory

            # keep track of iterations where best is updated
            last_best_update = it
            if first_best_update == 0:
                first_best_update = it

            # break if fit enough
            sat_fitness = tau - sat_tour_length
            if best_fitness >= sat_fitness:
                break
        
        # break if time limit reached
        if timed and (time.time() - start_time > time_limit):
            break

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
