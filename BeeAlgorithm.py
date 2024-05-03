import random
import time
import argparse
import structlog

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tabulate

from tqdm import tqdm
from typing import List

# Set max columns to display in pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

parser = argparse.ArgumentParser(description='Bee Algorithm for TSP')
parser.add_argument('--ns', type=int, default=75, help='Number of scout bees')
parser.add_argument('--nb', type=int, default=55, help='Number of onlooker bees')
parser.add_argument('--ne', type=int, default=15, help='Number of elite bees')
parser.add_argument('--nrb', type=int, default=25, help='Number of onlooker bees for elite search')
parser.add_argument('--nre', type=int, default=25, help='Number of elite bees for elite search')
parser.add_argument('--routeLen', type=int, default=50, help='Number of cities')
parser.add_argument('--iterations', type=int, default=100, help='Number of iterations')
parser.add_argument('--visualize', type=bool, default=False, help='Visualize the TSP route')
parser.add_argument('--visualize_final', type=bool, default=False, help='Visualize the final TSP route')

args = parser.parse_args()
ns = args.ns
nb = args.nb
ne = args.ne
nrb = args.nrb
nre = args.nre
routeLen = args.routeLen
iterations = args.iterations
visualize = args.visualize
visualize_final = args.visualize_final

logger = structlog.get_logger()

logger.info("Bee Algorithm for TSP")


# random.seed(42)


class Bee:

    def __init__(self, ns, nb, ne, nrb, nre, iterations):
        self.ns = ns
        self.nb = nb
        self.ne = ne
        self.nrb = nrb
        self.nre = nre
        self.iterations = iterations
        self.bees = []

    def solve(self, visualize=False):
        self.initialRandSolution()
        for t in range(self.iterations):
            self.eliteSearch()
            self.bestSearch()
            self.globalFill()
            self.calculateBests()
        if visualize:
            self.visualize()
        return

    def eliteSearch(self):
        for e in range(self.ne):
            bestValue = float("inf")
            bestMutation = []
            for i in range(self.nre):
                mutation = self.mutate(self.bees[e][0])
                mutationObjective = self.eval(mutation)
                if mutationObjective < bestValue:
                    bestMutation, bestValue = mutation, mutationObjective
            if bestValue < self.bees[e][1]:
                self.bees[e] = (bestMutation, bestValue)
        return

    def bestSearch(self):
        for b in range(self.ne + 1, self.nb + 1):
            bestValue = float("inf")
            bestMutation = []
            for i in range(self.nrb):
                mutation = self.mutate(self.bees[b][0])
                mutationObjective = self.eval(mutation)
                if mutationObjective < bestValue:
                    bestMutation, bestValue = mutation, mutationObjective
            if bestValue < self.bees[b][1]:
                self.bees[b] = (bestMutation, bestValue)
        return

    def globalFill(self):
        for g in range(self.nb + 1, len(self.bees)):
            self.bees[g] = self.random()
        return

    def initialRandSolution(self):
        for iter in range(self.ns):
            x = self.random()
            y = self.eval(x)
            self.bees.append((x, y))
        self.bees.sort(key=lambda bee: bee[1])
        return

    def calculateBests(self):
        sorted(self.bees, key=lambda bee: bee[1])

    def mutate(self, instance):
        pass

    def eval(self, instance):
        return 0

    def random(self):
        pass

    def visualize(self):
        pass


class BeeTSP(Bee):

    def __init__(self, inp, ns=75, nb=55, ne=15, nrb=25, nre=25, iterations=100):
        """
        Initializes the BeeTSP solver with specified parameters.

        Args:
            inp (dict): Input configuration which must contain either 'routeLen' or 'coords'.
            ns (int): Number of scout bees.
            nb (int): Number of onlooker bees.
            ne (int): Number of elite bees.
            nrb (int): Number of onlooker bees for elite search.
            nre (int): Number of elite bees for elite search.
            iterations (int): Number of iterations to perform.
        """
        super(BeeTSP, self).__init__(ns, nb, ne, nrb, nre, iterations)
        if "routeLen" in inp:
            self.routeLen = inp["routeLen"]
            self.coords = self.randCoords()
        elif "coords" in inp:
            self.coords = inp["coords"]
            self.routeLen = len(self.coords)
        else:
            raise ValueError("Invalid input")
        self.distances = self.evalDistances()
        self.best_distances = list()
        self.termination_distances = list()
        self.fig, self.axs = plt.subplots(1, 2)
        self.execution_time = 0

        init_data = pd.DataFrame({
            "Cities": [self.routeLen],  # Number of cities
            "Scout Bees": [ns],  # Number of scout bees
            "Onlooker Bees": [nb],  # Number of onlooker bees
            "Elite Bees": [ne],  # Number of elite bees
            "Elite Onlooker Bees": [nrb],  # Number of onlooker bees for elite search
            "Elite Bees for Elite Search": [nre],  # Number of elite bees for elite search
            "Iterations": [iterations]  # Number of iterations
        })

        table = tabulate.tabulate(init_data, headers='keys', tablefmt='pretty')
        logger.info(f"Parameters:\n{table}")
        print("\n")

        # print(init_data)

        # logger.info(f"Parameters:", data=init_data.to_dict(orient='records'))

        # logger.info(f"Bee TSP initialized with {self.routeLen} cities; {ns} scout bees, {nb} onlooker bees, "
        #             f"{ne} elite bees, {nrb} onlooker bees for elite search, {nre} elite bees for elite search, "
        #             f"{iterations} iterations")

    def eval(self, instance: List[int]) -> float:
        """
        Evaluates the total distance of the given TSP route instance.

        Args:
            instance (list): A list of city indices representing the TSP route.

        Returns:
            float: Total distance of the route.
        """
        idx = np.array(instance)
        total_distance = np.sum(self.distances[idx[:-1], idx[1:]])
        total_distance += self.distances[idx[-1], idx[0]]
        return total_distance

    def random(self) -> List[int]:
        """
       Generates a random route for the TSP.

       Returns:
           list: A list representing a random TSP route.
       """
        r = list(range(1, self.routeLen))
        random.shuffle(r)
        return [0] + r

    def randCoords(self) -> np.ndarray:
        """
        Generates random coordinates for each city in the TSP.

        Returns:
            np.ndarray: An array of random coordinates for each city.
        """
        return np.random.randint(0, 100, (self.routeLen, 2))

    def evalDistances(self):
        """
        Evaluates the pairwise Euclidean distances between all cities.

        Returns:
            np.ndarray: A 2D array of distances between each pair of cities.
        """
        diff = self.coords[:, np.newaxis, :] - self.coords[np.newaxis, :, :]
        distances = np.sqrt(np.sum(diff ** 2, axis=2))
        return distances

    def mutate(self, instance: List[int]) -> List:
        """
        Performs a mutation on a TSP route to potentially improve it.

        Args:
            instance (list): The current TSP route.

        Returns:
            list: A new TSP route with a mutation applied.
        """
        idx1 = random.randint(1, self.routeLen)
        idx2 = random.randint(1, self.routeLen)
        if idx1 == idx2:
            return self.mutate(instance)
        elif idx1 < idx2:
            temp = instance[:]
            temp[idx1: idx2] = instance[idx1: idx2][::-1]
            return temp
        else:
            temp = instance[:]
            temp[idx2: idx1] = instance[idx2: idx1][::-1]
            return temp

    def visualize(self):
        """
        Visualizes the best TSP route found.
        """
        tspRoute, tspObjective = self.bees[0][0], self.bees[0][1]
        x_coords, y_coords = zip(*self.coords)
        plt.scatter(x_coords, y_coords, color='blue', marker='o', label='Cities')
        for i in range(len(tspRoute) - 1):
            plt.plot([x_coords[tspRoute[i]], x_coords[tspRoute[i + 1]]],
                     [y_coords[tspRoute[i]], y_coords[tspRoute[i + 1]]], color='red')
        plt.plot([x_coords[tspRoute[-1]], x_coords[tspRoute[0]]],
                 [y_coords[tspRoute[-1]], y_coords[tspRoute[0]]], color='red')
        plt.scatter(x_coords[tspRoute[0]], y_coords[tspRoute[0]], color='green', marker='s', label='Start')
        plt.title(f'TSP Route Visualization; Objective: {round(tspObjective, 3)}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend()
        plt.show()

    def update_plot(self):
        """
        Updates the plot with the current best route and objective value.
        """
        self.axs[0].clear()
        self.axs[0].plot(self.best_distances, label='Best Objective Value')
        self.axs[0].set_title(f'Best Objective Value')
        self.axs[0].set_xlabel('Iteration')
        self.axs[0].set_ylabel('Objective Value')
        self.axs[0].grid()
        self.axs[0].legend()

        # Update plot of best current route
        tspRoute, tspObjective = self.bees[0][0], self.bees[0][1]
        x_coords, y_coords = zip(*self.coords)
        self.axs[1].clear()
        self.axs[1].scatter(x_coords, y_coords, color='blue', marker='o', label='Cities')
        for i in range(len(tspRoute) - 1):
            self.axs[1].plot([x_coords[tspRoute[i]], x_coords[tspRoute[i + 1]]],
                             [y_coords[tspRoute[i]], y_coords[tspRoute[i + 1]]], color='red')
        self.axs[1].plot([x_coords[tspRoute[-1]], x_coords[tspRoute[0]]],
                         [y_coords[tspRoute[-1]], y_coords[tspRoute[0]]], color='red')
        self.axs[1].scatter(x_coords[tspRoute[0]], y_coords[tspRoute[0]], color='green', marker='s', label='Start')
        self.axs[1].set_title('TSP Route Visualization')

        plt.draw()
        plt.pause(0.01)  # Pause to update the plot

    def visualize_final_route(self):
        """
        Visualizes the final best route found.
        """
        plt.figure()
        plt.plot(self.best_distances, marker='o')
        plt.title('Final Best Route')
        plt.xlabel('Node Index')
        plt.ylabel('Node Value')
        plt.grid(True)
        plt.show()

    def solve(self, visualize=True, visualize_final=False):
        """
        Executes the bee algorithm to optimize the TSP solution over a set number of iterations.
        It applies search and mutation strategies to progressively find and refine solutions.

        Args:
            visualize (bool): If True, dynamically visualizes the optimization progress during iterations.
            visualize_final (bool): If True, displays the final optimized TSP route.

        This method integrates elite and best search strategies, updates the visualization of the
        optimization process, and terminates either after completing all iterations or when improvements
        cease. The final best route and its objective value are printed to the console.
        """
        if visualize:
            plt.ion()
            self.fig.show()

        self.initialRandSolution()
        for t in tqdm(range(self.iterations)):
            start_time = time.time()

            self.eliteSearch()
            self.bestSearch()
            self.globalFill()
            self.calculateBests()

            self.execution_time += time.time() - start_time
            self.termination_distances.append(self.bees[0][1])
            if t == 0:
                self.best_distances.append(self.bees[0][1])
                if visualize:
                    self.update_plot()
            else:
                if self.bees[0][1] < self.best_distances[-1]:
                    self.best_distances.append(self.bees[0][1])
                    if visualize:
                        self.update_plot()

            # Termination condition
            # If the objective value is not changing for n steps, break
            termination = 100
            if len(self.termination_distances) > termination and len(
                    set(self.termination_distances[-termination:])) == 1:
                print(f"Converged at iteration {t + 1}")
                break

            if (t + 1) % termination == 0:
                print(f"Iteration: {t + 1}, Best Objective Value: {self.bees[0][1]}")

        if visualize:
            plt.ioff()
            plt.close(self.fig)
            plt.close()

        if visualize_final:
            self.visualize()

        print(f"Best Route: {self.bees[0][0]}")
        print(f"Objective Value: {round(self.bees[0][1], 4)}")


if __name__ == "__main__":
    start = time.time()
    tsp = BeeTSP(inp={"routeLen": routeLen}, nb=nb, ns=ns, nre=nre, nrb=nrb, iterations=iterations)
    tsp.solve(visualize=visualize, visualize_final=visualize_final)
    print("-" * 100)
    print(f"Time taken: {round(time.time() - start, 3)} seconds")
    logger.info(f"Execution completed in {round(tsp.execution_time, 3)} seconds")
    print(input("Press Enter to exit"))
