import random
import time

algorithm_code = "AC"

def run(num_cities, dist_matrix, time_limit=None):
    start_time = time.time()

    # Ant Colony Optimisation ENHANCED
    timed = time_limit is not None
    added_note = ""
    if timed:
        added_note += "Time limit = " + str(time_limit) + " seconds.\n"
    variation = 'MMAS' # AS_rank or MMAS (MAX-MIN Ant System)
    # MMAS gives just as good results as AS_rank, but MMAS converges faster
    # due to 2-opt, tau max/min limits, and faster due to candidate list
    added_note += variation + ' ACO algorithm\n'

    # for added note
    first_best_update = 0 # iteration of first best tour update
    last_best_update = 0 # iteration of last best tour update

    # define core parameters (SAME AS BASIC)
    max_it = 600 # max number of iterations
    num_ants = num_cities # N - recommended = num_cities

    # pheremone params (SAME AS BASIC)
    alpha = 1 # pheromone influence - 1
    beta = 2 # edge-distance (local heuristic) influence - recommended = 2 for MMAS
    rho = 0.6 # pheromone evaporation rate - recommended = 0.6 -> 0.9 for MMAS
    w = 6 # weight - for AS_rank

    added_note += "alpha = " + str(alpha) + ", beta = " + str(beta) + ", rho = " + str(rho) + ", w = " + str(w)

    # ENHANCED-SPECIFIC PARAMS
    use_candidate_list = True # whether to use candidate list - reduced number of unvisited cities considered when ant k moves
    cl_size = 20 # candidate list size - recommended between 10 and 30
    two_opt_limit = 4 # Since 2-opt is expensive, limit the search to this many nearest neighbours of the city
    p_best = 0.05 # probability that an ants tour exactly = the trail with most pheremone

    class City:
        def __init__(self, city):
            self.city = city

            # get list of adjacent cities ordered according to distance from self.city
            self.nearest_adj = sorted(list(range(num_cities)), key=lambda c: dist_matrix[self.city][c])
            self.nearest_adj.remove(self.city)

            # init candidate list with nearest neighbours
            self.cand_list = self.nearest_adj[:cl_size]
        
        def get_successor(self, tour):
            # get city after self.city in given tour
            i = tour.index(self.city)
            return tour[(i + 1) % num_cities]
        
        def get_predecessor(self, tour):
            # get city before self.city in given tour
            i = tour.index(self.city)
            return tour[(i - 1) % num_cities]

        def update_cand_list(self, best_tour, tau):
            '''
            Update candidate list based on pheromone and best tour found so far.
            
            Given city s, such that edge from current city --> s has most pheromone,
            and given city b, such that curent city --> b is edge in best tour found so far:
                If s and b are not in the candidate list, put them at the front.

            (Size of the list is maintained by dropping the last in the list if need be.)

            Note: this is my own implementation of Ismkhan's (2017) description
                of a 'dynamic' candidate list based on pheromone and best tour found so far.
            '''
            # get edge with most pheromone from current city
            max_pher = max(tau[self.city])
            stinkiest_neighbour = tau[self.city].index(max_pher)

            # put in cand list if not already
            if stinkiest_neighbour not in self.cand_list:
                self.cand_list.pop() # to maintain size of cand list, remove last element
                self.cand_list = [stinkiest_neighbour] + self.cand_list

            # get successor to city in best tour found so far
            succ = self.get_successor(best_tour)

            # put in cand list if not already
            if succ in self.cand_list:
                self.cand_list.pop()
                self.cand_list = [succ] + self.cand_list

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

    def two_opt(ant, checklist):
        '''
        2-opt local search to improve tour length by reversing a segment of the tour.

        Note: this is my own implementation of Skinderowicz' (2022) description & pseudocode
            of a 2-opt local search heuristic using a checklist.
        '''
        tour = ant.tour.copy()

        changes = 0 # num of successful 2-opt moves applied
        while len(checklist) > 0 and changes < num_cities:
            a = checklist.pop(0) # remove first city
            a_succ = cities[a].get_successor(tour) # city currently after a in tour
            a_pred = cities[a].get_predecessor(tour) # city currently before a in tour
            nn_list = cities[a].nearest_adj[:two_opt_limit] # a's nearest neighbouring cities
            move = [] # best 2-opt move for this nn list
            gain = 0 # cost change for move (improvement in tour length from move)

            # for each city, b, in a's nearest neighbours, compare a -> b with a -> a_succ
            # (tour = [..., a, a_succ, ..., b, b_succ, ...])
            for b in nn_list:
                b_succ = cities[b].get_successor(tour)
                # if a -> b shorter edge than current a -> a_succ:
                if dist_matrix[a][a_succ] > dist_matrix[a][b]:
                    # combined cost of existing edges after a, b in tour
                    cost_old = dist_matrix[a][a_succ] + dist_matrix[b][b_succ]
                    # combined cost of swapped edges
                    cost_new = dist_matrix[a][b] + dist_matrix[a_succ][b_succ]
                    # if this improves tour length more than previous best move, update best move
                    if cost_old - cost_new > gain:
                        gain = cost_old - cost_new
                        move = [a, a_succ, b, b_succ]
            
            # consider predecessors similarly
            for b in nn_list:
                b_pred = cities[b].get_predecessor(tour)
                # if a -> b shorter edge than current a_pred -> a
                if dist_matrix[a_pred][a] > dist_matrix[a][b]:
                    cost_old = dist_matrix[a_pred][a] + dist_matrix[b_pred][b]
                    cost_new = dist_matrix[a][b] + dist_matrix[a_pred][b_pred]
                    if cost_old - cost_new > gain:
                        gain = cost_old - cost_new
                        move = [a_pred, a, b_pred, b]

            if len(move) > 0: # if an improving move was found
                [w, x, y, z] = move
                # reverse a section of tour between x and y so x next to y and w next to z
                sect_start = tour.index(x) # mark start of section at x
                sect_end = (tour.index(y)+1) % num_cities # mark end of section just after y
                # if sect_start appears after sect_end in tour, wrap around list
                if sect_start > sect_end:
                    section = tour[sect_start:] + tour[:sect_end]
                    # add section to RHS of tour in reverse
                    for i in range(sect_start, num_cities):
                        tour[i] = section.pop()
                    # add section to LHS of tour in reverse
                    for i in range(0, sect_end):
                        tour[i] = section.pop()
                # otherwise slice tour as normal
                else:
                    prefix = tour[:sect_start]
                    section = tour[sect_start:sect_end]
                    suffix = tour[sect_end:]
                    section.reverse()
                    tour = prefix + section + suffix
                # append w, x, y, z to checklist
                checklist += [w, x, y, z]
                changes += 1
        
                # update ant
                ant.tour = tour.copy()
                ant.tour_length = get_tour_length(tour)

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

    # only deposit pheromone along the source tour for MMAS
    # init to nn_tour (best found so far)
    source_tour = nn_tour

    # MMAS - max and min pheremone allowed on a particular edge
    # values are from original paper https://www.sciencedirect.com/science/article/pii/S0167739X00000431?via%3Dihub#SEC16
    tau_max = 1 / (nn_tour_length * (1 - rho)) # Tau_max is estimate of asymptotically maximum value of pheromone that could be deposited on an edge
    avg = num_cities / 2 # average number of unvisited edges considered while calculating probabilities for trail
    tau_min = (tau_max * (1 - p_best)**(1 / num_cities)) / (avg - 1) * p_best**(1 / num_cities)
    # tau_min > 0 means always possible to visit an edge

    # init pheromone matrix tau, with initial deposit tau_0 on each edge
    tau_0 = (0.5 * w * (w-1)) / rho * nn_tour_length # AS_rank heuristic (same as AlgBbasic)
    # tau_0 = tau_max # MMAS heurstic
    # Note: after first iteration, all edges will be capped to tau_max.
    # (encourages initial unrestricted exploration)

    # pheromone matrix
    tau = [[tau_0] * num_cities for i in range(num_cities)]

    # init list of City class objects to reference city data (candidate lists, etc.)
    # NOTE purely for reference, not intended to be modified
    cities = [City(i) for i in range(num_cities)]

    # init global best tour & length
    global_best = []
    global_best_length = float('inf')

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

            ls_checklist = [] # to save time, only apply local search to edges not in best tour
            # (since have already done local search on that tour! (besides original nn tour))

            # stochastically build a trail
            while len(ant_k.tour) < num_cities:
                # get current city
                current_city = ant_k.tour[-1]

                # if using candidate list, reduce num cities considered for ant's next move
                if use_candidate_list:
                    cand_list = cities[current_city].cand_list

                    # take candidates from unvisited cities in current city's cand_list
                    candidates = [city for city in cand_list if city in ant_k.unvisited]

                    # if candidate list empty, deterministically choose unvisited city w/ highest numerator,
                    # referring to the numerator used to determine probability of visiting a city
                    if len(candidates) == 0:
                        best_num = 0
                        next_city = -1
                        for j in ant_k.unvisited:
                            numerator = (tau[current_city][j] ** alpha) * (eta(current_city, j) ** beta)
                            if numerator > best_num:
                                best_num = numerator
                                next_city = j
                        
                        if next_city == -1:
                            # if all unvisited cities have 0 probability (e.g. tau is 0)
                            # and we can't pick one, pick one at random to avoid getting stuck
                            if len(ant_k.unvisited) > 0:
                                next_city = random.choice(ant_k.unvisited)
                            else:
                                # tour is complete
                                continue

                        # visit next city and skip to next ant move
                        ant_k.visit_city(next_city)

                        # if edge not in source solution, add to checklist for 2-opt
                        succ = cities[current_city].get_successor(source_tour)
                        if next_city != succ:
                            ls_checklist.append(next_city)
                        continue
                # if not using candidate list, consider all unvisited cities for next move
                else:
                    candidates = ant_k.unvisited

                # get probabilities for each unvisited city
                probs = [0] * num_cities

                # calculate denominator first (same for each city)
                denominator = 0
                for m in candidates:
                    denominator += (tau[current_city][m] ** alpha) * (eta(current_city, m) ** beta)
                    
                # calculate numerator and probability of visiting each city
                for j in candidates:
                    numerator = (tau[current_city][j] ** alpha) * (eta(current_city, j) ** beta)
                    probs[j] = numerator / denominator

                # choose next city from probabilities
                next_city = random.choices(list(range(num_cities)), weights=probs)[0]
                ant_k.visit_city(next_city)

                # if edge not in source solution, add to checklist
                succ = cities[current_city].get_successor(source_tour)
                if next_city != succ:
                    ls_checklist.append(next_city)

            # evaluate & store ant tour length
            ant_k.tour_length = get_tour_length(ant_k.tour)
            
            # once trail is built, use local search to improve
            two_opt(ant_k, ls_checklist)

        # sort list of ants by tour length
        ants = sorted(ants, key=lambda ant: ant.tour_length)
        # print(set([ant.tour_length for ant in ants[:w]])) # print top 5 unique tour lengths

        # update best if improved tour found
        iter_best = ants[0].tour
        iter_best_length = ants[0].tour_length
        if iter_best_length < global_best_length:
            global_best_length = ants[0].tour_length
            global_best = ants[0].tour
            # print("BEST LENGTH:", global_best_length)

            # update tau max and min
            tau_max = 1 / (global_best_length * (1 - rho))
            tau_min = (tau_max * (1 - p_best)**(1 / num_cities)) / (avg - 1) * p_best**(1 / num_cities)
            
            # ensure tau_min doesnt exceed the maximum
            if tau_min > tau_max:
                tau_min = tau_max

            # keep track of iterations where best is updated
            last_best_update = t
            if first_best_update == 0:
                first_best_update = t

        ## update pheremone matrix
        
        # evaporate on all edges
        for i in range(num_cities):
            for j in range(num_cities):
                tau[i][j] *= (1 - rho)
                # ensure pheremone respects min limit
                if tau[i][j] < tau_min:
                    tau[i][j] = tau_min

        # MMAS only
        # global_best_freq (gbf) = x means that every x iters, global best ant is allowed to deposit
        # scheduled changes to global_best_freq
        # note: [a,b] means a < t <= b
        pher_schedule = {(0,25):0, (25,75):5, (75,125):3, (125,250):2, (250,max_it):1} # for example 
        # This eg. shifts emphasis to gb over time
        global_best_freq = 0 # Default value
        for bin in pher_schedule: # for bin (a,b)
            # if a < t <= b, set global_best_freq to associated value
            if t in range(bin[0], bin[1]):
                global_best_freq = pher_schedule[bin]

        # set source to be current best in iteration or global best
        if global_best_freq == 0:
            source_tour = iter_best
            source_length = iter_best_length
        else:
            # probabilitically choose global best or best within current iteration to deposit
            if random.random() <= 1 / global_best_freq:
                # note: risks worse exploration of search space & getting trapped in local minima
                source_tour = global_best
                source_length = global_best_length
            else:
                # note: risks taking longer to converge on a better tour
                source_tour = iter_best
                source_length = iter_best_length

        # MMAS AS - deposit on all edges of source tour
        # NOTE adds pher on edge j --> j+1 and j+1 --> j
        # so that ant on j+1 can smell pher on edge too.
        if variation == 'MMAS':
            for j in range(num_cities - 1):
                tau[source_tour[j]][source_tour[j + 1]] += (1 / source_length)
                tau[source_tour[j + 1]][source_tour[j]] += (1 / source_length)
            # deposit on edge back to start city
            tau[source_tour[num_cities - 1]][source_tour[0]] += (1 / source_length)
            tau[source_tour[0]][source_tour[num_cities - 1]] += (1 / source_length)

        # AS_rank - only deposit on w-1 shortest tours and globally best
        if variation == 'AS_rank':
            depositing_ants = ants[:w-1]

            for i in range(len(depositing_ants)):
                tour = depositing_ants[i].tour
                tour_length = depositing_ants[i].tour_length

                # for each city j deposit pheremone on edge to next city in tour
                for j in range(num_cities - 1):
                    tau[tour[j]][tour[j + 1]] += (w - i - 1) * (1 / tour_length)
                    tau[tour[j + 1]][tour[j]] += (w - i - 1) * (1 / tour_length)
                # add pheremone on edge from last city back to start
                tau[tour[num_cities - 1]][tour[0]] += (w - i - 1) * (1 / tour_length)
                tau[tour[0]][tour[num_cities - 1]] += (w - i - 1) * (1 / tour_length)

            # AS_rank - global best tour given top weighting
            for j in range(num_cities - 1):
                tau[global_best[j]][global_best[j + 1]] += w * (1 / global_best_length)
                tau[global_best[j + 1]][global_best[j]] += w * (1 / global_best_length)
            tau[global_best[num_cities - 1]][global_best[0]] += w * (1 / global_best_length)
            tau[global_best[0]][global_best[num_cities - 1]] += w * (1 / global_best_length)

        for i in range(num_cities):
            for j in range(num_cities):
                # ensure pheremone respects max limit
                if tau[i][j] > tau_max:
                    tau[i][j] = tau_max

        # update city candidate list
        for city in cities:
            city.update_cand_list(global_best, tau)

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

    return global_best, global_best_length, added_note
