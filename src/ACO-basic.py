import random
import time

algorithm_code = "AC"

def run(num_cities, dist_matrix, time_limit=None):
    start_time = time.time()
    
    # Ant Colony Optimisation BASIC
    timed = time_limit is not None
    added_note = ""
    if timed:
        added_note += "Time limit = " + str(time_limit) + " seconds.\n"
    variation = "AS_rank" # AS, EAS, AS_rank
    added_note += "ACO algorithm with " + variation + ".\n"

    # for added note
    first_best_update = 0 # iteration of first best tour update
    last_best_update = 0 # iteration of last best tour update

    # define core parameters
    max_it = 600 # max number of iterations
    num_ants = num_cities # N - recommended = num_cities

    # pheremone params
    alpha = 1 # pheromone influence - recommended = 1
    beta = 2 # edge-distance (local heuristic) influence - recommended between 2 and 5
    rho = 0.6 # pheromone evaporation rate - recommended = 0.5 for AS and EAS, 0.1 for AS_rank
    w = 6 # weight - recommended = num_ants for EAS (i.e. num. elite ants), 6 for AS_rank

    added_note += "alpha = " + str(alpha) + ", beta = " + str(beta) + ", rho = " + str(rho) + ".\n"
    if variation == 'EAS' or variation == 'AS_rank':
        added_note += "w = " + str(w) + ".\n"

    class Ant:
        def __init__(self, start_city=None):
            # init tour with specified or random start city
            if start_city is None:
                start_city = random.randint(0, num_cities - 1)
            self.tour = [start_city]
            self.tour_length = 0

            # init tabu list F_k for forbidden cities
            # (cities already visited by ant k)
            self.F_k = [start_city]

            # init list of unvisited cities
            self.unvisited = list(range(num_cities))
            self.unvisited.remove(start_city)

        def visit_city(self, city):
            self.tour.append(city)
            self.F_k.append(city)
            self.unvisited.remove(city)
        
        def reset(self):
            # reinit ant with same start city as current tour
            start_city = self.tour[0]
            self.tour = [start_city]
            self.tour_length = 0
            self.F_k = [start_city]
            self.unvisited = list(range(num_cities))
            self.unvisited.remove(start_city)

    # function to get tour length
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

    # function to get heurisisic desirability of edge
    epsilon = 0.000001 # small constant > 0 (avoid div by zero)
    def eta(i, j):
        return 1 / (dist_matrix[i][j] + epsilon)

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

    # get nn tour from random city for heurstic info
    nn_tour, nn_tour_length = nearest_neighbours()

    # init pheromone matrix tau, with initial deposit tau_0 on each edge
    if variation == 'EAS':
        tau_0 = (w + num_ants) / rho * nn_tour_length # EAS heuristic
    elif variation == 'AS_rank':
        tau_0 = (0.5 * w * (w-1)) / rho * nn_tour_length # AS_rank heuristic
    else:
        tau_0 = num_ants / nn_tour_length # AS heuristic (N / Lnn)

    # pheromone matrix
    tau = [[tau_0] * num_cities for i in range(num_cities)]

    # init best tour & length
    best_tour = []
    best_tour_length = float('inf')

    # place ants on cities
    ants = [Ant() for i in range(num_ants)] # randomly
    # ants = [Ant(i) for i in range(num_ants)] # specifically on each city (up to num_ants)

    # MAIN LOOP
    for t in range(max_it): # repeat for max_it iterations starting at t := 0
        # for each ant
        for ant_k in ants:
            # reset ant tour to start city if necessary
            if t > 0:
                ant_k.reset()

            # stochastically build a trail
            while len(ant_k.tour) < num_cities:
                # get current & unvisited cities
                current_city = ant_k.tour[-1]
                unvisited_cities = ant_k.unvisited

                # get probabilities for each unvisited city
                probs = [0] * num_cities

                # calculate denominator first (same for each city)
                denominator = 0
                for m in unvisited_cities:
                    denominator += (tau[current_city][m] ** alpha) * (eta(current_city, m) ** beta)
                    
                # calculate numerator and probability of visiting each city
                for j in unvisited_cities:
                    numerator = (tau[current_city][j] ** alpha) * (eta(current_city, j) ** beta)
                    probs[j] = numerator / denominator
                
                # choose next city from probabilities
                next_city = random.choices(list(range(num_cities)), weights=probs)[0]
                ant_k.visit_city(next_city)

            # evaluate & store ant tour length
            ant_k.tour_length = get_tour_length(ant_k.tour)

        # sort list of ants by tour length
        ants = sorted(ants, key=lambda ant: ant.tour_length)

        # update best if improved tour found
        if ants[0].tour_length < best_tour_length:
            best_tour_length = ants[0].tour_length
            best_tour = ants[0].tour

            # keep track of iterations where best is updated
            last_best_update = t
            if first_best_update == 0:
                first_best_update = t
            # print("BEST LENGTH:", best_tour_length)

        ## update pheremone matrix

        # evaporate on all edges
        for i in range(num_cities):
            for j in range(num_cities):
                tau[i][j] *= (1 - rho)

        # AS/EAS - for each ant, deposit on all edges in tour
        # AS_rank - only deposit on w-1 shortest tours
        if variation == 'AS_rank':
            depositing_ants = ants[:w-1]
        else:
            depositing_ants = ants

        for i in range(len(depositing_ants)):
            tour = depositing_ants[i].tour
            tour_length = depositing_ants[i].tour_length

            # for each city j deposit pheremone on edge to next city in tour
            # NOTE adds pher on edge j --> j+1 and j+1 --> j
            # so that ant on j+1 can smell pher on edge too.
            for j in range(num_cities - 1):
                if variation == 'AS_rank':
                    tau[tour[j]][tour[j + 1]] += (w - i - 1) * (1 / tour_length)
                    tau[tour[j + 1]][tour[j]] += (w - i - 1) * (1 / tour_length) # deposit in both directions
                else:
                    tau[tour[j]][tour[j + 1]] += 1 / tour_length
                    tau[tour[j + 1]][tour[j]] += 1 / tour_length

            # add pheremone on edge from last city back to start
            if variation == 'AS_rank':
                tau[tour[num_cities - 1]][tour[0]] += (w - i - 1) * (1 / tour_length)
                tau[tour[0]][tour[num_cities - 1]] += (w - i - 1) * (1 / tour_length)
            else:
                tau[tour[num_cities - 1]][tour[0]] += 1 / tour_length
                tau[tour[0]][tour[num_cities - 1]] += 1 / tour_length

        # EAS - reinforce edges in best tour found so far
        # AS_rank - best tour given top weighting
        if (variation == 'EAS' or variation == 'AS_rank'):
            for j in range(num_cities - 1):
                tau[best_tour[j]][best_tour[j + 1]] += w * (1 / best_tour_length)
                tau[best_tour[j + 1]][best_tour[j]] += w * (1 / best_tour_length)
            tau[best_tour[num_cities - 1]][best_tour[0]] += w * (1 / best_tour_length)
            tau[best_tour[0]][best_tour[num_cities - 1]] += w * (1 / best_tour_length)
        
        # break if time limit reached
        if timed and (time.time() - start_time > time_limit):
            break

    added_note += "\nFirst best tour update at t = " + str(first_best_update) + ".\n"
    added_note += "Last best tour update at t = " + str(last_best_update) + ".\n"

    try:
        param_note = f"The parameter values are 'max_it' = {max_it} and 'num_ants' = {num_ants}."
        if added_note:
            added_note += "\n" + param_note
        else:
            added_note = param_note
    except NameError:
        pass

    return best_tour, best_tour_length, added_note
