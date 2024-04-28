############
############ ALTHOUGH I GIVE YOU THIS TEMPLATE PROGRAM WITH THE NAME 'skeleton.py', 
############ YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR THE PURPOSES OF 
############ THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT THIS PROGRAM IS STILL 
############ CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES! TO SEE
############ THE STANDARD MODULES, TAKE A LOOK IN 'validate_before_handin.py'.
############
############ DO NOT INCLUDE ANY COMMENTS ON A LINE WHERE YOU IMPORT A MODULE.
############

import os
import sys
import time
import random

############ START OF SECTOR 0 (IGNORE THIS COMMENT)
############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############ BY 'DO NOT TOUCH' I REALLY MEAN THIS. EVEN CHANGING THE SYNTAX, BY
############ ADDING SPACES OR COMMENTS OR LINE RETURNS AND SO ON, COULD MEAN THAT
############ CODES MIGHT NOT RUN WHEN I RUN THEM!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r') 
    current_char = the_file.read(1) 
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}   
    tariff_dictionary = {}  
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"  
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)  
    location = 0
    EOF = False
    list_of_items = []  
    while EOF == False: 
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY!
############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT 
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############
############ END OF SECTOR 0 (IGNORE THIS COMMENT)

input_file = "AISearchfile535.txt"

############ START OF SECTOR 1 (IGNORE THIS COMMENT)
############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS STARTING
############ 'HAVE YOU TOUCHED ...'
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

############ END OF SECTOR 1 (IGNORE THIS COMMENT)

############ START OF SECTOR 2 (IGNORE THIS COMMENT)
path_for_city_files = os.path.join("..", "city-files")
############ END OF SECTOR 2 (IGNORE THIS COMMENT)

############ START OF SECTOR 3 (IGNORE THIS COMMENT)
path_to_input_file = os.path.join(path_for_city_files, input_file)
if os.path.isfile(path_to_input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string(path_to_input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the city-file folder.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY!
############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY 
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME.
############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS STARTING
############ 'HAVE YOU TOUCHED ...'
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############
############ END OF SECTOR 3 (IGNORE THIS COMMENT)

############ START OF SECTOR 4 (IGNORE THIS COMMENT)
path_for_alg_codes_and_tariffs = os.path.join("..", "alg_codes_and_tariffs.txt")
############ END OF SECTOR 4 (IGNORE THIS COMMENT)

############ START OF SECTOR 5 (IGNORE THIS COMMENT)
code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs(path_for_alg_codes_and_tariffs)

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY! SORRY TO GO ON ABOUT THIS BUT YOU NEED TO BE 
############ AWARE OF THIS FACT!
############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR
############ USER-NAME, E.G., "abcd12"
############
############ END OF SECTOR 5 (IGNORE THIS COMMENT)

my_user_name = "nchw73"

############ START OF SECTOR 6 (IGNORE THIS COMMENT)
############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT 
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############
############ END OF SECTOR 6 (IGNORE THIS COMMENT)

my_first_name = "Theo"
my_last_name = "Farrell"

############ START OF SECTOR 7 (IGNORE THIS COMMENT)
############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############
############ END OF SECTOR 7 (IGNORE THIS COMMENT)

algorithm_code = "AC"

############ START OF SECTOR 8 (IGNORE THIS COMMENT)
############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS STARTING
############ 'HAVE YOU TOUCHED ...'
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the algorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

start_time = time.time()

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY! SORRY TO GO ON ABOUT THIS BUT YOU NEED TO BE 
############ AWARE OF THIS FACT!
############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first 
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER. NOTE THAT I CALCULATE THE TIME OF
############ A RUN USING THE RESERVED VARIABLE 'start_time' AND INCLUDE THE RUN-TIME IN 'added_note' LATER.
############
############ IN FACT, YOU CAN INCLUDE YOUR ADDED NOTE IMMEDIATELY BELOW OR EVEN INCLUDE YOUR ADDED NOTE
############ AT ANY POINT IN YOUR PROGRAM: JUST DEFINE THE STRING VARIABLE 'added_note' WHEN YOU WISH
############ (BUT DON'T REMOVE THE ASSIGNMENT IMMEDIATELY BELOW).
############
############ END OF SECTOR 8 (IGNORE THIS COMMENT)

added_note = ""

############ START OF SECTOR 9 (IGNORE THIS COMMENT)
############
############ NOW YOUR CODE SHOULD BEGIN BUT FIRST A COMMENT.
############
############ IF YOU ARE IMPLEMENTING GA THEN:
############  - IF YOU EXECUTE YOUR MAIN LOOP A FIXED NUMBER OF TIMES THEN USE THE VARIABLE 'max_it' TO DENOTE THIS NUMBER
############  - USE THE VARIABLE 'pop_size' TO DENOTE THE SIZE OF YOUR POPULATION (THIS IS '|P|' IN THE PSEUDOCODE)
############
############ IF YOU ARE IMPLEMENTING AC THEN:
############  - IF YOU EXECUTE YOUR MAIN LOOP A FIXED NUMBER OF TIMES THEN USE THE VARIABLE 'max_it' TO DENOTE THIS NUMBER
############  - USE THE VARIABLE 'num_ants' TO DENOTE THE NUMBER OF ANTS (THIS IS 'N' IN THE PSEUDOCODE)
############
############ IF YOU ARE IMPLEMENTING PS THEN:
############  - IF YOU EXECUTE YOUR MAIN LOOP A FIXED NUMBER OF TIMES THEN USE THE VARIABLE 'max_it' TO DENOTE THIS NUMBER
############  - USE THE VARIABLE 'num_parts' TO DENOTE THE NUMBER OF PARTICLES (THIS IS 'N' IN THE PSEUDOCODE)
############
############ DOING THIS WILL MEAN THAT THIS INFORMATION IS WRITTEN WITHIN 'added_note' IN ANY TOUR-FILE PRODUCED.
############ OF COURSE, THE VALUES OF THESE VARIABLES NEED TO BE ACCESSIBLE TO THE MAIN BODY OF CODE.
############ IT'S FINE IF YOU DON'T ADOPT THESE VARIABLE NAMES BUT THIS USEFUL INFORMATION WILL THEN NOT BE WRITTEN TO ANY
############ TOUR-FILE PRODUCED BY THIS CODE.
############
############ END OF SECTOR 9 (IGNORE THIS COMMENT)


# Ant Colony Optimisation ENHANCED
timed = True
time_limit = 59 # seconds
if timed:
    added_note += "Time limit = " + str(time_limit) + " seconds.\n"
variation = 'MMAS' # AS_rank, MMAS (MAX-MIN Ant System)
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
                    for j in ant_k.unvisited:
                        numerator = (tau[current_city][j] ** alpha) * (eta(current_city, j) ** beta)
                        if numerator > best_num:
                            best_num = numerator
                            next_city = j
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
    if variation == 'MMAS':
        for j in range(num_cities - 1):
            tau[source_tour[j]][source_tour[j + 1]] += (1 / source_length)
        # deposit on edge back to start city
        tau[source_tour[num_cities - 1]][source_tour[0]] += (1 / source_length)

    # AS_rank - only deposit on w-1 shortest tours and globally best
    if variation == 'AS_rank':
        depositing_ants = ants[:w-1]

        for i in range(len(depositing_ants)):
            tour = depositing_ants[i].tour
            tour_length = depositing_ants[i].tour_length

            # for each city j deposit pheremone on edge to next city in tour
            # NOTE adds pher on edge j --> j+1 and j+1 --> j
            # so that ant on j+1 can smell pher on edge too.
            for j in range(num_cities - 1):
                tau[tour[j]][tour[j + 1]] += (w - i - 1) * (1 / tour_length)
                tau[tour[j + 1]][tour[j]] += (w - i - 1) * (1 / tour_length)
            # add pheremone on edge from last city back to start
            tau[tour[num_cities - 1]][tour[0]] += (w - i - 1) * (1 / tour_length)
            tau[tour[0]][tour[num_cities - 1]] += (w - i - 1) * (1 / tour_length)

        # AS_rank - global best tour given top weighting
        for j in range(num_cities - 1):
            tau[global_best[j]][global_best[j + 1]] += w * (1 / global_best_length)
        tau[global_best[num_cities - 1]][global_best[0]] += w * (1 / global_best_length)

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

# output
tour = global_best
tour_length = global_best_length


############ START OF SECTOR 10 (IGNORE THIS COMMENT)
############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour', 
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1} SO THAT EVERY INTEGER
############ APPEARS EXACTLY ONCE, AND YOU SHOULD ALSO HOLD THE LENGTH OF THIS TOUR IN THE RESERVED
############ INTEGER VARIABLE 'tour_length'.
############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE'S
############ NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATE AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############
############ DO NOT EDIT ANY TOUR FILE! ALL TOUR FILES MUST BE LEFT AS THEY WERE ON OUTPUT.
############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############

end_time = time.time()
elapsed_time = round(end_time - start_time, 1)

if algorithm_code == "GA":
    try: max_it
    except NameError: max_it = None
    try: pop_size
    except NameError: pop_size = None
    if added_note != "":
        added_note = added_note + "\n"
    added_note = added_note + "The parameter values are 'max_it' = " + str(max_it) + " and 'pop_size' = " + str(pop_size) + "."

if algorithm_code == "AC":
    try: max_it
    except NameError: max_it = None
    try: num_ants
    except NameError: num_ants = None
    if added_note != "":
        added_note = added_note + "\n"
    added_note = added_note + "The parameter values are 'max_it' = " + str(max_it) + " and 'num_ants' = " + str(num_ants) + "."

if algorithm_code == "PS":
    try: max_it
    except NameError: max_it = None
    try: num_parts
    except NameError: num_parts = None
    if added_note != "":
        added_note = added_note + "\n"
    added_note = added_note + "The parameter values are 'max_it' = " + str(max_it) + " and 'num_parts' = " + str(num_parts) + "."
    
added_note = added_note + "\nRUN-TIME = " + str(elapsed_time) + " seconds.\n"

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")
len_user_name = len(my_user_name)
user_number = 0
for i in range(0, len_user_name):
    user_number = user_number + ord(my_user_name[i])
alg_number = ord(algorithm_code[0]) + ord(algorithm_code[1])
tour_diff = abs(tour[0] - tour[num_cities - 1])
for i in range(0, num_cities - 1):
    tour_diff = tour_diff + abs(tour[i + 1] - tour[i])
certificate = user_number + alg_number + tour_diff
local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name,'w')
f.write("USER = {0} ({1} {2}),\n".format(my_user_name, my_first_name, my_last_name))
f.write("ALGORITHM CODE = {0}, NAME OF CITY-FILE = {1},\n".format(algorithm_code, input_file))
f.write("SIZE = {0}, TOUR LENGTH = {1},\n".format(num_cities, tour_length))
f.write(str(tour[0]))
for i in range(1,num_cities):
    f.write(",{0}".format(tour[i]))
f.write(",\nNOTE = {0}".format(added_note))
f.write("CERTIFICATE = {0}.\n".format(certificate))
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")

############ END OF SECTOR 10 (IGNORE THIS COMMENT)
