import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from tqdm import tqdm
import itertools

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

        self.current_sites = [self.init_random_route() for _ in range(ns)][:len(self.nb)]
        self.ne_int = ne
        self.ns_int = ns
        self.nb_int = nb

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

    def _performLocalSearches(self):
        for i in range(len(self.current_sites)):
            if i < self.ne_int:
                n_foragers = self.nre
            else:
                n_foragers = self.nrb
            self._localSearch(i, n_foragers)

    def _localSearch(self, index, n_foragers):
        for _ in range(n_foragers):
            new_route = self.two_edge_exchange(self.current_sites[index])
            if self.get_distance(new_route) < self.get_distance(self.current_sites[index]):
                self.current_sites[index] = new_route

    def performsinglestep(self):
        self._performLocalSearches()
        self.current_sites += [self.init_random_route() for _ in range(self.ns_int)]
        mapping_route_dist = {str(route): self.get_distance(route) for route in self.current_sites}
        mapping_route_dist = dict(sorted(mapping_route_dist.items(), key=lambda item: item[1]))
        self.current_sites = list(mapping_route_dist.keys())[:self.nb_int]
        if self.get_distance(eval(list(mapping_route_dist.keys())[0])) < self.best_distance:
            self.best_route = eval(list(mapping_route_dist.keys())[0])
            self.best_distance = self.get_distance(eval(list(mapping_route_dist.keys())[0]))

    def performFullOptimization(self, animate=True):
        distances = []

        if animate:
            fig, axs = plt.subplots(1, 2, figsize=(12, 9))
            best_route_line, = axs[1].plot([], [], 'k-')

        def update_plot(frame):
            axs[0].clear()
            axs[1].clear()

            # Plot the best distance
            axs[0].plot(range(1, frame + 2), distances[:frame + 1])
            axs[0].set_xlabel('Iteration')
            axs[0].set_ylabel('Best Distance')
            axs[0].set_title('Best Distance over Iterations')

            # Plot the best route
            best_route_coords = np.array([self.cities[i, :] for i in self.best_route])
            best_route_line.set_data(best_route_coords[:, 0], best_route_coords[:, 1])
            axs[1].plot(best_route_coords[:, 0], best_route_coords[:, 1], 'k-')
            axs[1].scatter(best_route_coords[:, 0], best_route_coords[:, 1], s=100, c='red')
            axs[1].set_xlabel('X')
            axs[1].set_ylabel('Y')
            axs[1].set_title('Best Route')

        iteration = 0
        for _ in tqdm(range(self.max_iter)):
            self.performsinglestep()
            distances.append(self.best_distance)
            if animate:
                update_plot(iteration)
                plt.pause(0.1)  # Kurze Pause, um die Aktualisierung sichtbar zu machen
            iteration += 1

        if animate:
            plt.show()

        # Output the final best route
        print(f"Best Route: {self.best_route}")
        print(f"Best Distance: {self.best_distance}")
        self.plot(self.best_route)

    def get_distance(self, route):
        # route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

        if isinstance(route, str):
            route = eval(route)

        # check if route is valid
        first_city = route[0]
        last_city = route[-1]

        if first_city != last_city:
            print(route)
            print(f"Type of route: {type(route)}")
            raise ValueError("Route is not valid. First and last cities must be connected.")
        if len(route) != self.n_cities + 1:
            print(route)
            print(len(route))
            # print missing city
            for c in range(self.n_cities):
                if c not in route:
                    print(f"Missing city: {c}")
            raise ValueError("Route is not valid. Route must contain all cities.")

        for c in range(self.n_cities):
            if c not in route:
                print(f"Missing city: {c}")
                print(f"Route: {route}")
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
        route = eval(route)
        plt.figure(figsize=(10, 10))
        plt.scatter(self.cities[:, 0], self.cities[:, 1], s=100)
        for i in range(self.n_cities):
            plt.annotate(i, (self.cities[i, 0] + 0.1, self.cities[i, 1] + 0.1), fontsize=20)
        for i in range(len(route) - 1):
            plt.plot([self.cities[route[i], 0], self.cities[route[i + 1], 0]],
                     [self.cities[route[i], 1], self.cities[route[i + 1], 1]], 'k-')

        title_text = f"Best Distance: {self.best_distance}\nBest Route: {self.best_route}"
        plt.title(title_text)

        plt.grid()
        plt.show()

    def neighborhood(self, route, n):
        neighborhoods = []
        while len(neighborhoods) < n:
            new_neighborhood = self.two_edge_exchange(route)
            if new_neighborhood not in neighborhoods:
                neighborhoods.append(new_neighborhood)

        return neighborhoods

    def best_search(self):
        # 2nd variant
        self.ne = self.ns[:self.ne_int]
        ne_route_dist_dict = {str(route): self.get_distance(route) for route in self.ne}
        ne_route_dist_dict = dict(sorted(ne_route_dist_dict.items(), key=lambda item: item[1]))

        index = 0
        for route, dist in ne_route_dist_dict.items():
            neighborhood = self.neighborhood(eval(route), self.nre)
            neighborhood_dict = {str(route_n): self.get_distance(route_n) for route_n in neighborhood}
            neighborhood_dict = dict(sorted(neighborhood_dict.items(), key=lambda item: item[1]))

            self.ns[index] = eval(list(neighborhood_dict.keys())[0])

            if dist < self.best_distance:
                self.best_distance = dist
                self.best_route = route
                self.ns[index] = eval(list(neighborhood_dict.keys())[0])

            index += 1
        ns_route_dist_dict = {str(route): self.get_distance(route) for route in self.ns}
        ns_route_dist_dict = dict(sorted(ns_route_dist_dict.items(), key=lambda item: item[1]))
        self.ns = [eval(route) for route in ns_route_dist_dict.keys()]

        # 1st variant
        # for i in range(len(self.ne)):
        #     neighborhood = self.neighborhood(self.ne[i], self.nre)
        #     neighborhood_dict = {str(route): self.get_distance(route) for route in neighborhood}
        #     neighborhood_dict = dict(sorted(neighborhood_dict.items(), key=lambda item: item[1]))
        #     self.ne[i] = list(neighborhood_dict.keys())[0]
        #
        #     local_best_distance = self.get_distance(self.ne[i])
        #
        #     if local_best_distance < self.get_distance(self.ns[i]):
        #         self.ns[i] = self.ne[i]
        #
        #     if local_best_distance < self.best_distance:
        #         self.best_route = self.ne[i]
        #         self.best_distance = local_best_distance

    def k_opt_exchange(self, route, k):
        if k < 2 or k >= len(route) - 2:
            print(k)
            raise ValueError("k must be between 2 and len(route) - 2")

        indices_to_swap = random.sample(range(1, len(route) - 1), k)

        new_route = route.copy()

        for i in range(k // 2):
            new_route[indices_to_swap[i]], new_route[indices_to_swap[k - i - 1]] = (
                new_route[indices_to_swap[k - i - 1]],
                new_route[indices_to_swap[i]],
            )

        return new_route

    def k_opt_exchange_reverse(self, route, k):
        # Zufällige Auswahl von k verschiedenen Städten
        indices = random.sample(range(1, len(route) - 1), k)
        indices.sort()

        # Reverse-Operation
        new_route_reverse = route[indices[0]:indices[-1] + 1][::-1]
        new_route = route[:indices[0]] + new_route_reverse + route[indices[-1] + 1:]

        return new_route

    def k_opt_insert(self, route, k):
        # Zufällige Auswahl von k verschiedenen Städten
        indices = random.sample(range(1, len(route) - 1), k)
        index_to_insert = random.randint(1, len(route) - 2)

        # Insert-Nachbarschaft
        new_route_insert = route.copy()

        for i in indices:
            city_to_move = new_route_insert.pop(i)
            new_route_insert.insert(index_to_insert, city_to_move)

        return new_route_insert

    def two_edge_exchange(self, route):
        if isinstance(route, str):
            route = eval(route)

        # random number from 1 to 3
        n = 2
        if n == 1:
            k = random.randint(2, len(route) - 3)
            return self.k_opt_exchange(route, k)
        elif n == 2:
            k = random.randint(2, len(route) - 3)
            return self.k_opt_exchange_reverse(route, k)

        elif n == 3:
            k = random.randint(2, len(route) - 3)
            return self.k_opt_insert(route, k)

    def elite_search(self):
        # 2nd variant
        nb_minus_ne = self.ns[:self.nb_int - self.ne_int] # ?? wrong??
        nb_minus_ne_dict = {str(route): self.get_distance(route) for route in nb_minus_ne}
        nb_minus_ne_dict = dict(sorted(nb_minus_ne_dict.items(), key=lambda item: item[1]))

        index = 0
        for route, dist in nb_minus_ne_dict.items():
            neighborhood = self.neighborhood(eval(route), self.nrb)
            neighborhood_dict = {str(route_n): self.get_distance(route_n) for route_n in neighborhood}
            neighborhood_dict = dict(sorted(neighborhood_dict.items(), key=lambda item: item[1]))

            self.ns[index] = eval(list(neighborhood_dict.keys())[0])

            if dist < self.best_distance:
                self.best_distance = dist
                self.best_route = route
                self.ns[index] = eval(list(neighborhood_dict.keys())[0])
            index += 1

        # sort ns
        ns_route_dist_dict = {str(route): self.get_distance(route) for route in self.ns}
        ns_route_dist_dict = dict(sorted(ns_route_dist_dict.items(), key=lambda item: item[1]))
        self.ns = [eval(route) for route in ns_route_dist_dict.keys()]

        # 1st variant
        # for route_index in range(self.nb_int - self.ne_int):
        #     neighborhood = self.neighborhood(self.nb[route_index], self.nrb)
        #     neighborhood_dict = {str(route): self.get_distance(route) for route in neighborhood}
        #     neighborhood_dict = dict(sorted(neighborhood_dict.items(), key=lambda item: item[1]))
        #     self.nb[route_index] = list(neighborhood_dict.keys())[0]
        #
        #     local_best_distance = self.get_distance(self.nb[route_index])
        #
        #     if local_best_distance < self.get_distance(self.ns[route_index]):
        #         self.ns[route_index] = self.nb[route_index]
        #
        #     if local_best_distance < self.best_distance:
        #         self.best_route = self.nb[route_index]
        #         self.best_distance = local_best_distance

    def global_search(self):
        ns_minus_nb_random = [self.init_random_route() for _ in range(self.ns_int - self.nb_int)]

        ns_minus_nb_random_dict = {str(route): self.get_distance(route) for route in ns_minus_nb_random}
        ns_minus_nb_random_dict = dict(sorted(ns_minus_nb_random_dict.items(), key=lambda item: item[1]))

        # nb_new = []
        # # get first nb routes from ns_minus_nb_random_dict
        # for i in range(len(self.nb)):
        #     if ns_minus_nb_random_dict[list(ns_minus_nb_random_dict.keys())[i]] < self.get_distance(self.nb[i]):
        #         nb_new.append(eval(list(ns_minus_nb_random_dict.keys())[i]))
        #     else:
        #         nb_new.append(self.nb[i])
        # self.nb = nb_new
        #
        # ne_new = []
        # # get first ne routes from ns_minus_nb_random_dict
        # for i in range(len(self.ne)):
        #     if ns_minus_nb_random_dict[list(ns_minus_nb_random_dict.keys())[i]] < self.get_distance(self.ne[i]):
        #         ne_new.append(eval(list(ns_minus_nb_random_dict.keys())[i]))
        #     else:
        #         ne_new.append(self.ne[i])
        # self.ne = ne_new

        # update ns
        index = 0
        for route, dist in ns_minus_nb_random_dict.items():
            if dist < self.get_distance(self.ns[index]) and eval(route) not in self.ns:
                self.ns[index] = eval(route)

                if dist < self.best_distance:
                    self.best_distance = dist
                    self.best_route = eval(route)
                    self.ns[index] = eval(route)
            index += 1

        # sort ns
        ns_route_dist_dict = {str(route): self.get_distance(route) for route in self.ns}
        ns_route_dist_dict = dict(sorted(ns_route_dist_dict.items(), key=lambda item: item[1]))
        self.ns = [eval(route) for route in ns_route_dist_dict.keys()]

    def fit(self, animate=True):
        distances = []
        if animate:
            fig, axs = plt.subplots(1, 2, figsize=(10, 7))
            best_route_line, = axs[1].plot([], [], 'k-')

            def update_plot(frame):
                axs[0].clear()
                axs[1].clear()

                # Plot the best distance
                axs[0].plot(range(1, frame + 2), distances[:frame + 1])
                axs[0].set_xlabel('Iteration')
                axs[0].set_ylabel('Best Distance')
                axs[0].set_title(f'Best Distance over Iterations ({self.best_distance})')

                # Plot the best route

                best_route_coords = np.array([self.cities[i, :] for i in eval(self.best_route)])
                best_route_line.set_data(best_route_coords[:, 0], best_route_coords[:, 1])
                axs[1].plot(best_route_coords[:, 0], best_route_coords[:, 1], 'k-')
                axs[1].scatter(best_route_coords[:, 0], best_route_coords[:, 1], s=100, c='red')
                axs[1].set_xlabel('X')
                axs[1].set_ylabel('Y')
                axs[1].set_title('Best Route')

        for _ in tqdm(range(self.max_iter)):
            self.best_search()  # best sites
            self.elite_search()  # elite sites

            self.global_search()  # global search

            # print lenghts
            # print(f"nb: {len(self.nb)}")
            # print(f"ne: {len(self.ne)}")
            # print(f"ns: {len(self.ns)}")

            distances.append(self.best_distance)
            if animate:
                update_plot(_)
                plt.pause(0.01)
            if not animate:
                # print every 1000 iterations
                if _ % 50 == 0:
                    print(f"Best Distance: {self.best_distance}; Iteration: {_}")

        # Output the final best route
        print(f"Best Route: {self.best_route}")
        print(f"Best Distance: {self.best_distance}")
        self.plot(self.best_route)


def fit_optimum(self):
    # brute force approach
    # calculate all possible routes
    all_routes = []


if __name__ == '__main__':
    ns = 100
    max_iter = 2000
    n_cities = 20
    nb = 20
    ne = 15
    nrb = 3
    nre = 50

    bee_tsp = BeeTSP(ns, max_iter, n_cities, nb, ne, nrb, nre)
    bee_tsp.fit(True)

    # bee_tsp.performFullOptimization(animate=True)
