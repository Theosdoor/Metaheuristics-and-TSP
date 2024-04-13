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
if os.path.isfile(path_for_city_files + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string(path_for_city_files + "/" + input_file, ord_range)
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

algorithm_code = "GA"

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

# Genetic algorithm
timed = False
time_limit = 50 # seconds
if timed:
    added_note += "Time limit = " + str(time_limit) + " seconds.\n"

# for added NOTE
first_best_update = 0 # iteration of first best tour update
last_best_update = 0 # iteration of last best tour update

# define core parameters
max_it = 1000 # max number of generations
pop_size = 250 # |P|
p_crossover = 0.9 # probability of crossover
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
    Returns length of given tour.

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

    REFERENCE
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

# If num_cities is small or runtime not restricted,
# generate nn tour starting from each city
# otherwise create only r nn tours
# NOTE num_cities <= 180 takes less than 1 second to generate all
m = 200
r = 70 # for large city sets > size m, generate only r nn tours
nn_tours = {}
if num_cities <= m or not timed:
    # create nn tour from every start city
    for i in range(num_cities):
        ith_tour = nearest_neighbours(start_city=i)
        ith_tour_length = get_tour_length(ith_tour)
        nn_tours[ith_tour_length] = ith_tour
else:
    # get list of r unique start cities
    start_cities = random.sample(range(num_cities), r)
    # create r nn tours
    for i in range(r):
        ith_tour = nearest_neighbours(start_city=start_cities[i])
        ith_tour_length = get_tour_length(ith_tour)
        nn_tours[ith_tour_length] = ith_tour

# get sorted list of nn tour lenghts
nn_lengths = sorted(nn_tours.keys())

# tour good enough if it is less than half the length of an nn tour
sat_tour_length = 0.5 * nn_lengths[0]

# generate initial population as follows:
P = []
# fill with available nn tours in order from shortest to longest
for i in range(len(nn_lengths)):
    individual = nn_tours[nn_lengths[i]]
    P.append(individual)
# then fill remaining space with randomised tours
for i in range(pop_size - len(nn_lengths)):
    individual = list(range(num_cities)) # init tour: [0, 1, 2, ..., num_cities - 1]
    random.shuffle(individual) # shuffle cities visited in each tour
    P.append(individual)

# init tau, fitness list, best individuals
f_mins, tau = get_f_mins(P)
best_fitness = max(f_mins)
best_tour = P[f_mins.index(best_fitness)]
best_tour_tau = tau
print("BEST LENGTH:", get_tour_length(best_tour))

# MAIN LOOP until:
# certain number of iterations done or
# some individual is fit enough or
# time limit reached
for it in range(max_it):
    if it % 50 == 0:
        print("it:", it, "/", max_it)
        # print("BEST LENGTH:", get_tour_length(best_tour)) 

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

        # with fixed probability crossover X, Y
        k = random.random() # pick random probability (i.e. int between 0 and 1)
        if k <= p_crossover:
            Z1 = crossover(X, Y)
        # if no crossover, keep parent
        else:
            Z1 = X

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
        print("BEST LENGTH:", get_tour_length(best_tour))

        # keep track of iterations where best is updated
        last_best_update = it
        if first_best_update == 0:
            first_best_update = it

        # break if fit enough
        sat_fitness = tau - sat_tour_length
        if best_fitness >= sat_fitness:
            print("Tour fit enough\n")
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
        print("Increasing p_mutation to", p2, "...")
        p_mutation = p2
    elif (it_since_last_best > p3_thresh) and p_mutation < p3:
        print("Increasing p_mutation to", p3, "...")
        p_mutation = p3
    elif (it_since_last_best > p4_thresh) and p_mutation < p4:
        print("Increasing p_mutation to", p4, "...")
        p_mutation = p4
    else:
        # reduce p_mutation if rate of improvement increases and P sufficiently diverse
        if p_mutation > p1 and (it_since_last_best < p2_thresh) and not homogeneous:
            print("Reducing p_mutation...")
            p_mutation = p1

    # break if time limit reached
    if timed and (time.time() - start_time > time_limit):
        print("Time's up! it:", it)
        max_it = it # TODO remove?
        break

added_note += "First best tour update at it = " + str(first_best_update) + ".\n"
added_note += "Last best tour update at it = " + str(last_best_update) + ".\n"

# output
tour = best_tour
tour_length = best_tour_tau - best_fitness # tour length = tau - f_min

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
