import os
import sys
import time
import argparse
from datetime import datetime
from src.utils import (
    read_file_into_string,
    remove_all_spaces,
    integerize,
    convert_to_list_of_int,
    build_distance_matrix,
    read_in_algorithm_codes_and_tariffs,
)

# --- Algorithm registry ---
# Add new algorithms here. Key = name you pass on the command line.
import src.ACO_basic
import src.ACO_enhanced
import src.GA_basic
import src.GA_enhanced

ALGORITHMS = {
    "ACO-basic":    src.ACO_basic,
    "ACO-enhanced": src.ACO_enhanced,
    "GA-basic":     src.GA_basic,
    "GA-enhanced":  src.GA_enhanced,
}


def run_algorithm(module_name, input_file_name, time_limit=None):
    if module_name not in ALGORITHMS:
        print(f"*** error: Unknown algorithm '{module_name}'. Choose from: {list(ALGORITHMS.keys())}")
        sys.exit()

    algorithm_module = ALGORITHMS[module_name]

    path_for_city_files = "city-files"
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
    print(f"  the number of cities is {num_cities}")

    stripped_file_string = file_string[comma + 1:]
    distances = convert_to_list_of_int(stripped_file_string)

    city_format = "strict_upper_tri"
    if len(distances) == num_cities * num_cities:
        city_format = "full"
    elif len(distances) == (num_cities * (num_cities + 1)) / 2:
        city_format = "upper_tri"

    dist_matrix = build_distance_matrix(num_cities, distances, city_format)
    print("  distance matrix built.")

    path_for_alg_codes_and_tariffs = "alg_codes_and_tariffs.txt"
    code_dictionary, _, flag = read_in_algorithm_codes_and_tariffs(path_for_alg_codes_and_tariffs)
    if flag != "good":
        print("*** error: 'alg_codes_and_tariffs.txt' does not exist.")
        sys.exit()

    algorithm_code = algorithm_module.algorithm_code
    if algorithm_code not in code_dictionary:
        print(f"*** error: algorithm code {algorithm_code} is illegal")
        sys.exit()
    print(f"  algorithm code: {algorithm_code} - {code_dictionary[algorithm_code]}")

    run_datetime = datetime.now()
    datetime_stamp = run_datetime.strftime("%Y%m%d_%H%M%S")
    datetime_readable = run_datetime.strftime("%Y-%m-%d %H:%M:%S")

    start_time = time.time()
    tour, tour_cost, added_note = algorithm_module.run(num_cities, dist_matrix, time_limit=time_limit)
    running_time = round(time.time() - start_time, 2)

    if added_note:
        added_note += "\n"
    added_note += f"Running time: {running_time} seconds."

    tour_file_name = f"tour{module_name}_{input_file_name[:-4]}_{datetime_stamp}.txt"
    try:
        with open(os.path.join("tours", tour_file_name), 'w') as f:
            f.write(f"DATETIME = {datetime_readable}\n")
            f.write(f"ALGORITHM_CODE = {algorithm_code}\n")
            f.write(f"COST = {tour_cost}\n")
            f.write(f"TOUR = {','.join(map(str, tour))}\n")
            f.write(f"NOTE = {added_note}\n")
        print(f"\nTour written to {tour_file_name}.")
    except Exception as e:
        print(f"*** error: Could not write tour file: {e}")
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a TSP algorithm.")
    parser.add_argument("module", help=f"Algorithm to run. Options: {list(ALGORITHMS.keys())}")
    parser.add_argument("city_file", help="Path to the city file.")
    parser.add_argument("--time_limit", type=float, help="Optional time limit in seconds.")
    args = parser.parse_args()

    run_algorithm(
        args.module,
        os.path.basename(args.city_file),
        time_limit=args.time_limit,
    )