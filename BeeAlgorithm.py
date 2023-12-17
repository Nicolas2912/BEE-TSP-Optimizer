import random
import matplotlib.pyplot as plt


class Bee:

    def __init__(self, ns, nb, ne, nrb, nre, iterations):
        self.ns = ns
        self.nb = nb
        self.ne = ne
        self.nrb = nrb
        self.nre = nre
        self.iterations = iterations
        self.bees = []

    def solve(self):
        self.initialRandSolution()
        for t in range(self.iterations):
            self.eliteSearch()
            self.bestSearch()
            self.globalFill()
            self.calculateBests()


    def eliteSearch(self):
        pass

    def globalFill(self):
        pass

    def bestSearch(self):
        pass

    def mutate(self, instance):
        pass

    def eval(self, instance):
        pass

    def randSolution(self):
        pass

    def initialRandSolution(self):
        pass

    def calculateBests(self):
        pass


class BeeTSP(Bee):

    def __init__(self, inp, ns=75, nb=55, ne=15, nrb=25, nre=25, iterations=2000):
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

    def eval(self, instance):
        value = 0
        for i in range(1, len(instance)):
            value += self.distances[instance[i-1]][instance[i]]
        value += self.distances[instance[-1]][0]
        return value

    def random(self):
        r = list(range(1, self.routeLen))
        random.shuffle(r)
        return [0] + r

    def initialRandSolution(self):
        for iter in range(self.ns):
            x = self.random()
            y = self.eval(x)
            self.bees.append((x, y))
        self.bees.sort(key=lambda bee: bee[1])
        return

    def randCoords(self):
        coords = []
        for i in range(self.routeLen):
            coords.append((random.randint(0, 100), random.randint(0, 100)))
        return coords

    def evalDistances(self):
        distances = []
        for i in range(len(self.coords)):
            temp = []
            for j in range(len(self.coords)):
                temp.append(0)
            distances.append(temp)

        for i in range(len(self.coords)):
            for j in range(i + 1, len(self.coords)):
                distances[i][j] = ((self.coords[i][0] - self.coords[j][0]) ** 2 + (self.coords[i][1] - self.coords[j][1]) ** 2) ** 0.5
                distances[j][i] = distances[i][j]
        return distances

    def mutate(self, instance):
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

    def calculateBests(self):
        sorted(self.bees, key=lambda bee: bee[1])

    def visualize(self):
        tspRoute, tspObjective = self.bees[0][0], self.bees[0][1]
        x_coords, y_coords = zip(*self.coords)

        # Plot the points
        plt.scatter(x_coords, y_coords, color='blue', marker='o', label='Cities')

        # Plot the TSP route
        for i in range(len(tspRoute) - 1):
            plt.plot([x_coords[tspRoute[i]], x_coords[tspRoute[i + 1]]],
                     [y_coords[tspRoute[i]], y_coords[tspRoute[i + 1]]], color='red')

        # Connect the last point to the starting point to complete the loop
        plt.plot([x_coords[tspRoute[-1]], x_coords[tspRoute[0]]],
                 [y_coords[tspRoute[-1]], y_coords[tspRoute[0]]], color='red')

        # Highlight the starting point
        plt.scatter(x_coords[tspRoute[0]], y_coords[tspRoute[0]], color='green', marker='s', label='Start')

        # Add labels and title
        plt.title('TSP Route Visualization')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend()

        # Show the plot
        plt.show()

    def solve(self):
        self.initialRandSolution()
        for t in range(self.iterations):
            self.eliteSearch()
            self.bestSearch()
            self.globalFill()
            self.calculateBests()
        self.visualize()


tsp = BeeTSP(inp={"routeLen": 100})
tsp.solve()