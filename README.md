# Metaheuristics for the Traveling Salesperson Problem (TSP)

This project implements and compares several metaheuristic algorithms for solving the Traveling Salesperson Problem (TSP). The implementations include both basic and enhanced versions of Genetic Algorithms (GA) and Ant Colony Optimization (ACO) algorithms.

## Overview

The TSP is a classic optimization problem where the goal is to find the shortest possible route that visits each city exactly once and returns to the starting city. This project explores four different algorithmic approaches, each with distinct strategies for exploration and exploitation of the solution space.

## Algorithms Implemented

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

## Performance Features

- **Time Management**: All algorithms respect a ~59 second time limit
- **Solution Quality Tracking**: Records first and last improvement iterations  
- **Convergence Detection**: Early termination when satisfactory solutions found
- **Benchmarking**: Uses nearest neighbor heuristic for initial solution quality assessment

## File Structure

```
├── search-algs/          # Algorithm implementations
│   ├── GA-basic.py       # Basic genetic algorithm
│   ├── GA-enhanced.py    # Enhanced GA with SCX crossover & adaptive mutation
│   ├── ACO-basic.py      # Basic ACO with multiple variant support
│   └── ACO-enhanced.py   # Enhanced ACO with MMAS & local search
├── city-files/           # TSP problem instances (12-535 cities)
├── best-tours/           # Generated solution files
├── benchmark.py          # Performance testing suite
├── analyze_results.py    # Visualization and analysis tools
├── config.py            # Algorithm parameter configurations
└── requirements.txt     # Python dependencies
```


## Algorithm Details

### Genetic Algorithm Enhancements
The enhanced GA implements several advanced techniques:
- **Sequential Constructive Crossover (SCX)**: Preserves good edge characteristics from both parents
- **Adaptive Mutation**: Dynamically adjusts mutation rate (0.2→0.5) based on convergence patterns
- **Smart Population Initialization**: 95% nearest neighbor tours + 5% random for diversity
- **Convergence Monitoring**: Tracks population homogeneity and adaptation

### ACO Algorithm Variants
The ACO implementations support multiple algorithmic variants:
- **Ant System (AS)**: Basic pheromone update mechanism
- **Elitist Ant System (EAS)**: Emphasizes elite solutions
- **Ant System with Ranking**: Weighted pheromone updates
- **Max-Min Ant System (MMAS)**: Bounded pheromone values with local search

## Performance Characteristics

Based on testing across 11 instances (12-535 cities):
- **GA-enhanced** typically finds highest quality solutions on larger instances
- **ACO-enhanced** excels on medium-sized problems with local search integration
- **Basic variants** provide reliable baseline performance with faster execution
- All algorithms respect 59-second time constraints for fair comparison

## Technical Implementation Notes

### Key Algorithmic Features
- **Time-bounded execution**: All algorithms implement proper time management
- **Memory efficiency**: Distance matrices computed once and reused
- **Solution validation**: Tours verified for completeness and optimality
- **Reproducible results**: Configurable random seeds for testing

### Code Architecture
- **Separation of concerns**: Algorithm logic separate from I/O framework
- **Extensible design**: Easy to add new metaheuristic variants
- **Performance monitoring**: Built-in iteration and improvement tracking

## Note on Contribution

**Note**: This project was originally coursework. My algorithm implementations begin at line 356 in each Python file. The framework code (lines 1-355) was provided by the instructor and handles file I/O, distance matrix creation, and tour output formatting.
