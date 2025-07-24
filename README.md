# Metaheuristics for the Traveling Salesperson Problem (TSP)

This project implements and compares several metaheuristic algorithms for solving the Traveling Salesperson Problem (TSP). The implementations include both basic and enhanced versions of Genetic Algorithms (GA) and Ant Colony Optimization (ACO) algorithms.

- **Grade:** 1st Class (83%)
- **Notable Rankings:** Best tour in the class on 9 occasions.

**Instructor Feedback**
> "Both your basic implementations are correct so you get a correctness mark of 4/4. You implemented a demanding algorithm and your sophistication mark is 9/10. I looked for improvements of at least 400 for the small unseen city file and 240 for the larger one. Your improvements were such as to yield a mark of 1/2 for enhanced tour quality. Your enhancements in GA-enhanced.py are reasonable and worth 1.5/3 enhancement marks. Your enhancements in ACO-enhanced.py are reasonable and worth 1.5/3 enhancement marks. Your overall tour quality mark is 7.76/8 and you got the best tour in the class on 9 occasions. (The total number of marks available was 30.)"
— Prof. Iain Stewart, Durham University

**Contribution Note** - I wrote the Genetic Algorithm and Ant Colony Optimization implementations. The remaining framework code for file I/O, distance matrix creation, and tour output formatting was provided by the instructor.

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

## Algorithmic Enhancement Details

### Genetic algorithm enhancement details (GA-enhanced.py)

**Initial population** – Instead of generating it randomly, some nearest neighbours (NN) tours are calculated and used in the initial population $P$. These are generally shorter than randomised ones, so the initial $P$ is somewhat fit. This helps breed even fitter individuals faster than the basic version since short edges already exist in $P$ and don’t have to be created by crossover/mutation. Since NN tour generation is much more costly than randomised ones ($O(n^2)$ vs $O(n)$), a user-defined proportion, $0 < m < 1$, of the population is filled with NN tours with unique start cities. Remaining individuals are completely randomised since some randomness reduces risk of getting stuck in local minima.

**Sequentially constructed crossover (SCX) (Ahmed, 2010)** – SCX generates a child tour $Z$ from two parent tours $X$, $Y$ as follows: 1. $Z$’s start city $c_Z$ is the same as $X$’s or $Y$’s. 2. Search through $X$ and $Y$ for the first unvisited cities after $p$ – call these $c_X$ and $c_Y$. 3. If $c_X$ is nearer to $c_Z$ then add it to the end of $Z$, otherwise add $c_Y$. 4. Repeat 2-4 until $Z$ is complete. If a parent tour has a good sequence of cities, SCX makes $Z$ likely to inherit it. However, step 2 means that a new edge will be created if $c_X$ or $c_Y$ does not immediately follow $c_Z$ in $X$ or $Y$. This supports population diversity. With a randomised initial population, SCX generated a high-quality population in much fewer generations than the basic crossover. This resulted in much better tours for large city sets since more iterations could be used to improve further.

**Dynamic mutation probability** – Mutation is essential to escape local fitness maxima that hinder convergence on an optimal tour. If it occurs too often, divergence is possible since good tours can become worse. In the basic GA, this is fixed at 0.2 which works well initially. However, if the best tour has not been updated for many generations it is likely either a local extremum or in fact optimal. In the enhanced GA, the probability of mutation increases after either: many iterations pass without an update to the best tour, or if 90% of the population has the same fitness. Increments and their associated thresholds are user-defined. This appeared successful, with better tours often found immediately after a period of stagnation triggered more mutations.

---
### Ant Colony Optimisation algorithm enhancement details (ACO-enhanced.py)

**2-opt local search** - Once ant $k$ has built its tour, 2-opt local search can improve it. This searches the tour for a pair of disjoint edges, $(a_0, a_1)$ and $(b_0, b_1)$, that can be replaced by another pair of disjoint edges, $(a_0, b_0)$ and $(a_1, b_1)$, such that the new pair of edges have a lower cost than the original pair. This is equivalent to reversing the tour between (and including) $a_1$ and $b_0$. This significantly reduced each ant’s tour length by greedily looking for local optima within the ant’s tour, which are easily overlooked in basic ACO. Since this is very expensive, cities considered for $a_0$ are restricted to edges not already in the best tour found so far, since those have already undergone 2-opt. The cities considered for $b_0$ are limited to the first $k$ nearest neighbours of $a_0$, where $k$ is user-defined ($k=4$ strikes a good balance).

**Dynamic candidate lists** - each city has a candidate list, containing its $m$ nearest neighbours where $m$ is user-defined ($m=20$). During trail building, only the candidate list of the current city, $c$, undergoes the stochastic process. If all these have been visited, then the next city is deterministically chosen as the unvisited city with the greatest product of pheromone on the connecting edge and heuristic desirability (i.e., the numerator used to calculate probability in the stochastic process). To counteract this, each city $c$’s candidate list is dynamically updated by adding $s$ and $b$ to the front, where $s$ is the city such that the edge $c \rightarrow s$ has the most pheromone of $c$’s neighbours, and $b$ is the city visited after $c$ in the best tour found so far. This uses heuristic information that is readily available since it is calculated over the course of the ACO regardless, and it reduces the aforementioned limitations on the tour quality when using candidate lists.

**MAX-MIN AS (MMAS) (Stützle & Hoos, 2000)** - The basic ACO uses ASrank which gives generally better results than standard AS because only top ants and the globally best tour found so far deposit pheromone. Using the global best tour to deposit encourages convergence towards it which is important since better tours are assumed to share edges with the current best. Using the current iteration’s best tour promotes exploration of the search space, avoiding getting trapped in local minima. MMAS takes ASrank to the extreme by allowing only one of either the global best or current iteration’s best tour to deposit. Which one it is depends on a user-defined schedule which makes it more likely the current iteration’s best is used early on, but in following iterations the global best is used to encourage convergence. A maximum pheromone level is maintained to avoid premature convergence, and a non-zero minimum level means there is always a chance to visit other cities, promoting exploration. These are defined using the cited paper’s equations which are explained in the code.

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

The script will automatically handle loading the data, running the specified algorithm, and saving the resulting tour to the `tours` directory.

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


