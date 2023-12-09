import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from tqdm import tqdm

random.seed(42)


class BeeTSP:

    def __init__(self, ns: int, max_iter: int, n_cities: int, ne: int, nb: int, nrb: int,
                 nre: int):
        self.max_iter = max_iter
        self.n_cities = n_cities

        self.cities = self.init_cities()  # distance matrix

        # parameters
        self.nrb = nrb
        self.nre = nre

        # init scout bees
        self.ns = [self.init_random_route() for _ in range(ns)]

        self.route_fitness_dict = {str(route): self.get_distance(route) for route in self.ns}

        # sorty by value ascending
        self.route_fitness_dict = dict(sorted(self.route_fitness_dict.items(), key=lambda item: item[1]))

        self.best_route = eval(list(self.route_fitness_dict.keys())[0])
        self.best_distance = self.get_distance(self.best_route)

        # get the first nb and ne routes
        self.nb = list(self.route_fitness_dict.keys())[:nb]
        self.ne = list(self.route_fitness_dict.keys())[:ne]

        self.nb = [eval(route) for route in self.nb]
        self.ne = [eval(route) for route in self.ne]

    def init_random_route(self):
        route = list(range(self.n_cities))
        random.shuffle(route)
        route.append(route[0])
        return route

    def init_cities(self):
        distances = np.zeros((self.n_cities, self.n_cities))
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                if i != j:
                    rand_dist = random.randint(1, 100)
                    distances[i][j] = rand_dist
                    distances[j][i] = rand_dist
                else:
                    distances[i][j] = 0

        return distances

    def get_distance(self, route):
        # route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

        # check if route is valid
        first_city = route[0]
        last_city = route[-1]
        if first_city != last_city:
            raise ValueError("Route is not valid. First and last cities must be connected.")
        if len(route) != self.n_cities + 1:
            raise ValueError("Route is not valid. Route must contain all cities.")

        for c in range(self.n_cities):
            if c not in route:
                raise ValueError("Route is not valid. Route must contain all cities.")

        for c in range(self.n_cities):
            if route.count(c) > 1 and c != first_city and c != last_city:
                raise ValueError("Route is not valid. Route must contain all cities only once.")

        distance = 0
        for i in range(len(route) - 1):
            distance += self.cities[route[i]][route[i + 1]]

        return distance

    def plot(self, route):
        # plot
        plt.figure(figsize=(10, 10))
        plt.scatter(self.cities[:, 0], self.cities[:, 1], s=100)
        for i in range(self.n_cities):
            plt.annotate(i, (self.cities[i, 0] + 0.1, self.cities[i, 1] + 0.1), fontsize=20)
        for i in range(len(route) - 1):
            plt.plot([self.cities[route[i], 0], self.cities[route[i + 1], 0]],
                     [self.cities[route[i], 1], self.cities[route[i + 1], 1]], 'k-')

        plt.grid()
        plt.show()

    def local_search(self):
        for ne in self.ne:
            for nre in range(self.nre):
                new_route = self.two_edge_exchange(ne)
                if self.get_distance(new_route) < self.best_distance:
                    self.best_route = new_route
                    self.best_distance = self.get_distance(new_route)

                    # get largest route in ns
                    largest_route = max(self.ns, key=lambda x: self.get_distance(x))

                    # get index of largest route in ns
                    largest_route_index = self.ns.index(largest_route)

                    self.ns[largest_route_index] = new_route

    def two_edge_exchange(self, route):
        i, j = random.sample(range(1, len(route) - 1), 2)
        new_route = route.copy()
        new_route[i], new_route[j] = new_route[j], new_route[i]

        return new_route[::-1]

    def global_search(self):
        nb_minus_nb = len(self.nb) - len(self.ne)
        for route_index in range(nb_minus_nb):
            for nrb in range(self.nrb):
                new_route = self.two_edge_exchange(self.nb[route_index])
                if self.get_distance(new_route) < self.best_distance:
                    self.best_route = new_route
                    self.best_distance = self.get_distance(new_route)

                    # get largest route in ns
                    largest_route = max(self.ns, key=lambda x: self.get_distance(x))

                    # get index of largest route in ns
                    largest_route_index = self.ns.index(largest_route)

                    self.ns[largest_route_index] = new_route

    def fit(self, plot=True):
        if plot:

            fig, axs = plt.subplots(1, 2, figsize=(12, 9)) if plot else (None, None)
            distances = []
            best_route_line, = axs[1].plot([], [], 'k-') if plot else (None,)

            def update_plot(frame):
                axs[0].clear() if plot else None
                axs[1].clear() if plot else None

                # Local Search Phase
                self.local_search()

                # Global Search Phase
                self.global_search()

                ns_minus_nb = len(self.ns) - len(self.nb)
                ns_minus_nb_random = [self.init_random_route() for _ in range(ns_minus_nb)]
                ns_minus_nb_random_dict = {str(route): self.get_distance(route) for route in ns_minus_nb_random}
                ns_minus_nb_random_dict = dict(sorted(ns_minus_nb_random_dict.items(), key=lambda item: item[1]))

                self.nb = list(ns_minus_nb_random_dict.keys())[:len(self.nb)]
                self.ne = list(ns_minus_nb_random_dict.keys())[:len(self.ne)]

                self.nb = [eval(route) for route in self.nb]
                self.ne = [eval(route) for route in self.ne]

                # update best route and best distance
                for route in self.ns:
                    if self.get_distance(route) < self.best_distance:
                        self.best_route = route
                        self.best_distance = self.get_distance(route)

                distances.append(self.best_distance)

                # Plot the best distance
                axs[0].plot(range(1, frame + 2), distances[:frame + 1]) if plot else None
                axs[0].set_xlabel('Iteration') if plot else None
                axs[0].set_ylabel('Best Distance') if plot else None
                axs[0].set_title('Best Distance over Iterations') if plot else None

                # Plot the best route
                if plot:
                    best_route_coords = np.array([self.cities[i, :] for i in self.best_route])
                    best_route_line.set_data(best_route_coords[:, 0], best_route_coords[:, 1])
                    axs[1].plot(best_route_coords[:, 0], best_route_coords[:, 1], 'k-')
                    axs[1].scatter(best_route_coords[:, 0], best_route_coords[:, 1], s=100, c='red')
                    axs[1].set_xlabel('X')
                    axs[1].set_ylabel('Y')
                    axs[1].set_title('Best Route')

            ani = animation.FuncAnimation(fig, update_plot, frames=self.max_iter, repeat=False,
                                          interval=1) if plot else None
            plt.show() if plot else None

            # Output the final best route
            print(f"Best Route: {self.best_route}")
            print(f"Best Distance: {self.best_distance}")

        else:
            for _ in tqdm(range(self.max_iter)):
                # Local Search Phase
                self.local_search()

                # Global Search Phase
                self.global_search()

                ns_minus_nb = len(self.ns) - len(self.nb)
                ns_minus_nb_random = [self.init_random_route() for _ in range(ns_minus_nb)]
                ns_minus_nb_random_dict = {str(route): self.get_distance(route) for route in ns_minus_nb_random}
                ns_minus_nb_random_dict = dict(sorted(ns_minus_nb_random_dict.items(), key=lambda item: item[1]))

                self.nb = list(ns_minus_nb_random_dict.keys())[:len(self.nb)]
                self.ne = list(ns_minus_nb_random_dict.keys())[:len(self.ne)]

                self.nb = [eval(route) for route in self.nb]
                self.ne = [eval(route) for route in self.ne]

                # update best route and best distance
                for route in self.ns:
                    if self.get_distance(route) < self.best_distance:
                        self.best_route = route
                        self.best_distance = self.get_distance(route)

            # Output the final best route
            print(f"Best Route: {self.best_route}")
            print(f"Best Distance: {self.best_distance}")



if __name__ == '__main__':
    ns = 500
    max_iter = 10000
    n_cities = 20
    nb = 200
    ne = 40
    nrb = 50
    nre = 100

    bee_tsp = BeeTSP(ns, max_iter, n_cities, nb, ne, nrb, nre)
    bee_tsp.fit(False)
