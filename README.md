# BEE-TSP-Optimizer

## Description

This repository contains an implementation (in `python` and `C++`) of the Bee Algorithm designed to solve the Traveling Salesman Problem (TSP).
The Bee Algorithm is a population-based search algorithm that mimics the food foraging behavior of honey bees to find
the optimal route to minimize the total distance traveled between cities.

## Usage

Clone the repository and navigate to the desired implementation directory.

```
git clone https://github.com/Nicolas2912/bee-tsp-optimizer.git
cd bee-tsp-optimizer
```

### Matlab implementation

In order to run the MATLAB implementation just follow these steps:

1. **Execution:**

    * Execute the `main.m` file using MATLAB
    * Customize the algorithm parameters within the script based on your optimization problem and preferences.

2. **Animation (optional):**

    * To visualize the solving process, set the `animate` parameter to true in the `main.m` file.

### Python implementation

In order to run the the python implementation just follow these steps:

1. Installing the required packages:

    ```bash
    pip install numpy matplotlib pandas tqdm tabulate structlog
    ```
   
2. Run the `BeeAlgorithm.py` file using python:

    ```bash
    python BeeAlgorithm.py --ns 75 --nb 55 --ne 15 --nrb 25 --nre 25 --routeLen 50 --iterations 100 --visualize True --visualize_final True
    ```
   
Parameters:

* `ns`: Number of scout bees (default: 75)
* `nb`: Number of best bees (default: 55)
* `ne`: Number of elite bees (default: 15)
* `nrb`: Number of recruited bees (default: 25)
* `nre`: Number of recruited elite bees (default: 25)
* `routeLen`: Number of cities in the route (default: 50)
* `iterations`: Number of iterations (default: 100)
* `visualize`: Visualize the solving process (default: True)
* `visualize_final`: Visualize the final route (default: True)

#### Visualization

If `--visualize` or `--visualize_final` is set to True, the routes will be plottted. This helps in understanding how 
the algorithm progresses and converges to the best solution.

### C++ implementation

In order to run the C++ implementation just follow these steps:

1. Compile the `BeeAlgorithm.cpp` file using g++:

    ```bash
    g++ main.cpp TSP.cpp Bee.cpp -o main
    ```
   
2. Run the compiled file (with parameters):

    ```bash
    main.exe 75 55 15 25 25 50 100
    ```

3. Run the compiled file (with default parameters):

    ```bash
    main.exe
    ```

# Acknowledgements

* Inspired by the natural foraging behavior of honeybees.
* Thanks to the contributors of the Python packages used in this project.
* And a special thanks to @linuslangenkamp for helping me with this little project!


