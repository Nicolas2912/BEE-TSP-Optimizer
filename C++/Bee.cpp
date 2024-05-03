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
    double lastBestValue = std::numeric_limits<double>::infinity();
    int noImprovementCounter = 0;
    int noImprovementThreshold = 100;  // Set this to the number of iterations without improvement you tolerate
    bool improvementThresholdReached = false;

    for (int t = 0; t < iterations; ++t) {
        eliteSearch();
        bestSearch();
        globalFill();
        calculateBests();

        // Check for improvement
        if (bees[0].back() < lastBestValue) {
            lastBestValue = bees[0].back();
            noImprovementCounter = 0;
        } else {
            noImprovementCounter++;
        }

        // Check if we have reached the no improvement threshold
        if (noImprovementCounter >= noImprovementThreshold) {
            std::cout << "Terminating after " << noImprovementThreshold << " iterations without improvement." << std::endl;
            improvementThresholdReached = true;
            break;
        }
    }

    std::vector<double> best_solution = bees[0];
    best_solution.pop_back();
    if (!improvementThresholdReached) {
        std::cout << "Terminating after " << iterations << " iterations." << std::endl;
    }
    std::cout << "\n----------------------\n";

    std::cout << "Route: ";
    for (auto &val: best_solution) {
        std::cout << val << " ";
    }
    std::cout << "\nObjective Value: " << bees[0].back() << std::endl;

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = end - start;
    auto duration_sec = std::chrono::duration_cast<std::chrono::seconds>(duration).count();
    auto duration_ms = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count() - 1000 * duration_sec;

    // Print total time in seconds and milliseconds
    std::cout << "Total Time: " << duration_sec << "s " << duration_ms << "ms" << std::endl;
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






