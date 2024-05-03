import unittest
from Python.BeeAlgorithm import BeeTSP
import numpy as np


class TestBeeAlgorithm(unittest.TestCase):

    def test_random(self):
        bee = BeeTSP(inp={'routeLen': 10})
        route = bee.random()
        self.assertEqual(len(route), 10)
        self.assertEqual(len(set(route)), 10)
        self.assertIn(0, route)

    def test_eval(self):
        bee = BeeTSP(inp={'coords': np.random.randint(0, 100, (10, 2))})
        route = list(range(10))
        distance = bee.eval(route)
        self.assertIsInstance(distance, float)

    def test_mutate(self):
        bee = BeeTSP(inp={'routeLen': 10})
        route = list(range(10))
        mutated = bee.mutate(route)
        self.assertNotEqual(route, mutated)
        self.assertEqual(len(mutated), 10)

    def test_evalDistances(self):
        bee = BeeTSP(inp={'coords': np.random.randint(0, 100, (10, 2))})
        bee.evalDistances()
        self.assertEqual(bee.distances.shape, (10, 10))
        self.assertEqual(bee.distances[0, 0], 0)
        self.assertEqual(bee.distances[0, 1], bee.distances[1, 0])

    def test_solve(self):
        bee = BeeTSP(inp={'coords': np.random.randint(0, 100, (10, 2))})
        bee.solve()
        self.assertEqual(len(bee.bestRoute), 10)
        self.assertEqual(len(set(bee.bestRoute)), 10)
        self.assertIn(0, bee.bestRoute)
        self.assertIsInstance(bee.bestDistance, float)
        self.assertIsInstance(bee.bestRoute, list)


if __name__ == '__main__':
    unittest.main()
