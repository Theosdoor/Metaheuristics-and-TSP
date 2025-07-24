# Metaheuristics for the Traveling Salesperson Problem (TSP)

This project implements and compares several metaheuristic algorithms for solving the Traveling Salesperson Problem (TSP). The implementations include both basic and enhanced versions of Genetic Algorithms (GA) and Ant Colony Optimization (ACO) algorithms.

## Overview

The TSP is a classic optimization problem where the goal is to find the shortest possible route that visits each city exactly once and returns to the starting city. This project explores four different algorithmic approaches, each with distinct strategies for exploration and exploitation of the solution space.

## Algorithms Implemented

The core logic for each algorithm is contained in the `src` directory. The boilerplate code for file parsing and setup was provided as part of the original coursework and has been extracted into `src/utils.py`.

### Genetic Algorithm (GA)
- **`GA-basic.py`**: Standard genetic algorithm with:
  - Population size: 250
  - Crossover: Simple split-and-repair mechanism  
  - Mutation: Random city swapping (p=0.2)
  - Selection: Roulette wheel based on fitness

- **`GA-enhanced.py`**: Advanced GA with:
  - Smart initial population (95% nearest neighbor tours)
  - Sequential Constructive Crossover (SCX) operator
  - Adaptive mutation rates (0.2 → 0.5 based on convergence)
  - Population diversity monitoring

### Ant Colony Optimization (ACO)
- **`ACO-basic.py`**: Implementation supporting multiple ACO variants:
  - Ant System (AS)
  - Elitist Ant System (EAS) 
  - Ant System with Ranking (AS_rank)
  - Configurable pheromone parameters (α=1, β=2, ρ=0.6)

- **`ACO-enhanced.py`**: Advanced ACO with:
  - Max-Min Ant System (MMAS) with pheromone bounds
  - Candidate list strategy for reduced computational complexity
  - 2-opt local search for tour improvement
  - Dynamic pheromone scheduling

## How to Run

To run an algorithm, navigate to the `src` directory and use the `main.py` script. You must provide the algorithm module and the city file.

1.  Navigate to the `src` directory:
    ```bash
    cd src
    ```
2.  Execute `main.py` with the desired algorithm and city file:
    ```bash
    # Example: Run the enhanced Genetic Algorithm on a 12-city problem
    python main.py GA-enhanced ../city-files/AISearchfile012.txt

    # Example: Run the basic Ant Colony Optimization on a 100-city problem
    python main.py ACO-basic ../city-files/AISearchfile100.txt
    ```

3.  **Optional Arguments:**
    -   To set a time limit (in seconds), use the `--time_limit` flag:
        ```bash
        python main.py GA-enhanced ../city-files/AISearchfile535.txt --time_limit 60
        ```
    -   To specify a user name for the output file, use the `--user_name` flag:
        ```bash
        python main.py GA-enhanced ../city-files/AISearchfile012.txt --user_name MyUsername
        ```

The script will automatically handle loading the data, running the specified algorithm, and saving the resulting tour to the `best-tours` directory.

## File Structure

```
├── src/                  # Algorithm implementations
│   ├── main.py           # Central runner for all algorithms
│   ├── GA-basic.py       # Basic genetic algorithm module
│   ├── GA-enhanced.py    # Enhanced GA module
│   ├── ACO-basic.py      # Basic ACO module
│   └── ACO-enhanced.py   # Enhanced ACO module
│   └── utils.py          # Helper functions for data processing
├── city-files/           # TSP problem instances (12-535 cities)
├── best-tours/           # Generated solution files
├── Proforma.md           # Detailed implementation notes
└── README.md             # This file
```

## Note on Contribution

This project was originally coursework. I wrote the Genetic Algorithm and Ant Colony Optimization implementations. The surrounding framework code for file I/O, distance matrix creation, and tour output formatting was provided by the instructor.
