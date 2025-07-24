import os
import sys
import time
import importlib
import argparse

from utils import (
    read_file_into_string,
    remove_all_spaces,
    integerize,
    convert_to_list_of_int,
    build_distance_matrix,
    read_in_algorithm_codes_and_tariffs,
)

def run_algorithm(module_name, user_name, input_file_name, time_limit=None):
    """
    Dynamically imports and runs a specified TSP algorithm module.
    """
    try:
        algorithm_module = importlib.import_module(module_name)
    except ImportError:
        print(f"*** error: Could not import algorithm module {module_name}")
        sys.exit()

    # --- Boilerplate setup from original scripts ---
    path_for_city_files = os.path.join("..", "city-files")
    path_to_input_file = os.path.join(path_for_city_files, input_file_name)

    if not os.path.isfile(path_to_input_file):
        print(f"*** error: The city file {input_file_name} does not exist.")
        sys.exit()

    ord_range = [[32, 126]]
    file_string = read_file_into_string(path_to_input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print(f"I have found and read the input file {input_file_name}:")

    location = file_string.find("SIZE=")
    comma = file_string.find(",", location)
    num_cities_as_string = file_string[location + 5:comma]
    num_cities = integerize(num_cities_as_string)
    print(f"   the number of cities is stored in 'num_cities' and is {num_cities}")

    stripped_file_string = file_string[comma + 1:]
    distances = convert_to_list_of_int(stripped_file_string)

    city_format = "strict_upper_tri"
    if len(distances) == num_cities * num_cities:
        city_format = "full"
    elif len(distances) == (num_cities * (num_cities + 1)) / 2:
        city_format = "upper_tri"

    dist_matrix = build_distance_matrix(num_cities, distances, city_format)
    print("   the distance matrix 'dist_matrix' has been built.")

    path_for_alg_codes_and_tariffs = os.path.join("..", "alg_codes_and_tariffs.txt")
    code_dictionary, _, flag = read_in_algorithm_codes_and_tariffs(path_for_alg_codes_and_tariffs)

    if flag != "good":
        print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
        sys.exit()
    print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

    algorithm_code = algorithm_module.algorithm_code
    if algorithm_code not in code_dictionary:
        print(f"*** error: the algorithm code {algorithm_code} is illegal")
        sys.exit()
    print(f"   your algorithm code is legal and is {algorithm_code} - {code_dictionary[algorithm_code]}.")

    start_time = time.time()

    # --- Execute the algorithm ---
    tour, tour_cost, added_note = algorithm_module.run(num_cities, dist_matrix, time_limit=time_limit)

    # --- Boilerplate teardown from original scripts ---
    end_time = time.time()
    running_time = round(end_time - start_time, 2)

    if added_note:
        added_note += "\n"
    added_note += f"Running time: {running_time} seconds."

    tour_file_name = f"tour{module_name}_{input_file_name[:-4]}_{user_name}.txt"
    
    # This part is a simplified version of the original tour file writing logic
    try:
        with open(os.path.join("..", "tours", tour_file_name), 'w') as f:
            f.write(f"USER = {user_name}\n")
            f.write(f"ALGORITHM_CODE = {algorithm_code}\n")
            f.write(f"COST = {tour_cost}\n")
            f.write(f"TOUR = {','.join(map(str, tour))}\n")
            f.write(f"NOTE = {added_note}\n")
        print(f"\nI have written the tour to the file {tour_file_name}.")
    except Exception as e:
        print(f"*** error: Could not write tour file: {e}")
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a TSP algorithm.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("module", help="The algorithm module to run (e.g., GA-enhanced).")
    parser.add_argument("city_file", help="Path to the city file (e.g., ../city-files/AISearchfile012.txt).")
    parser.add_argument("--time_limit", type=float, help="Optional time limit in seconds for the algorithm.")
    parser.add_argument("--user_name", type=str, default="nchw73", help="Your username.")

    args = parser.parse_args()

    run_algorithm(
        args.module,
        args.user_name,
        os.path.basename(args.city_file),
        time_limit=args.time_limit
    )
