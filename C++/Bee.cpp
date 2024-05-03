//
// Created by Nicolas Schneider on 18.12.23.
//
#include <vector>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <cmath>
#include <chrono>
#include "TSP.h"
#include "Bee.h"

Bee::Bee(int ns, int nb, int ne, int nrb, int nre, int iterations, TSP problem)
    : ns(ns), nb(nb), ne(ne), nrb(nrb), nre(nre), iterations(iterations), problem(problem) {
    this->coords = problem.coords;
    this->distances = problem.distances;

    // Initialize best_objectives
    this->best_objectives = std::vector<double>(iterations, std::numeric_limits<double>::infinity());

    // Initialize bees
    this->bees = std::vector<std::vector<double>>(ns, std::vector<double>(problem.routeLen, 1.0));

}

void Bee::solve() {
    auto start = std::chrono::high_resolution_clock::now();
    initialRandSolution();
    for (int t = 0; t < iterations; ++t) {
        eliteSearch();
        bestSearch();
        globalFill();
        calculateBests();
        if (t % 250 == 0) {
            double best_objective1 = bees[0].back();
            std::cout << "Iteration: " << t << "; Distance: " << best_objective1 << "\n";
            // print time
            std::cout << "Time: " << std::chrono::duration_cast<std::chrono::seconds>(
                    std::chrono::high_resolution_clock::now() - start).count() << "s" << std::endl;
        }

    }
    std::vector<double> best_solution = bees[0];
    best_solution.pop_back();
    std::cout << "\n----------------------\n";

    std::cout << "Best solution: ";
    for (auto &val: best_solution) {
        std::cout << val << " ";
    }
    std::cout << "\nBest objective: " << bees[0].back() << std::endl;

    auto end = std::chrono::high_resolution_clock::now();
    // convert time to seconds
    std::cout << "Total Time: " << std::chrono::duration_cast<std::chrono::seconds>(end - start).count() << "s"
              << std::endl;
    std::cout << "\n========FINISHED========\n";
}

void Bee::initialRandSolution() {
    for (int iter = 0; iter < ns; ++iter) {
        std::vector<double> x = problem.random();
        x.push_back(problem.eval(x));
        bees[iter] = x;
    }
    std::sort(bees.begin(), bees.end(), [](const std::vector<double>& a, const std::vector<double>& b) {
        return a.back() < b.back();
    });
}

void Bee::calculateBests() {
    std::sort(bees.begin(), bees.end(), [](const std::vector<double>& a, const std::vector<double>& b) {
        return a.back() < b.back();
    });

    best_objectives.push_back(bees[0].back());
}

void Bee::eliteSearch() {
    for (int e = 0; e < ne; ++e) {
        double bestValue = std::numeric_limits<double>::infinity();
        std::vector<double> bestMutation;
        for (int i = 0; i < nre; ++i) {
            // print bees[e]

            std::vector<double> beeWithoutLastElement = std::vector<double>(bees[e].begin(), bees[e].end() - 1);
            std::vector<double> mutation = problem.mutate(beeWithoutLastElement);
            double mutationObjective = problem.eval(mutation);
            if (mutationObjective < bestValue) {
                bestMutation = mutation;
                bestValue = mutationObjective;
            }
        }
        if (bestValue < bees[e].back()) {
            bestMutation.push_back(bestValue);
            bees[e] = bestMutation;
        }
    }
}

void Bee::bestSearch() {
    for (int b = 0; b < nb; ++b) {
        double bestValue = std::numeric_limits<double>::infinity();
        std::vector<double> bestMutation;
        for (int i = 0; i < nrb; ++i) {
            std::vector<double> beeWithoutLastElement = std::vector<double>(bees[b].begin(), bees[b].end() - 1);
            std::vector<double> mutation = problem.mutate(beeWithoutLastElement);
            double mutationObjective = problem.eval(mutation);
            if (mutationObjective < bestValue) {
                bestMutation = mutation;
                bestValue = mutationObjective;
            }
        }
        if (bestValue < bees[b].back()) {
            bestMutation.push_back(bestValue);
            bees[b] = bestMutation;
        }
    }
}

void Bee::globalFill() {
    for (int g = nb + 1; g < bees.size(); ++g) {
        std::vector<double> randomSolution = problem.random();
        randomSolution.push_back(problem.eval(randomSolution));
        bees[g] = randomSolution;
    }
}






