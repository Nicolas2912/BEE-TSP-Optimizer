#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <random>
#include "TSP.h"

TSP::TSP(int routeLength) : routeLen(routeLength) {
    coords = randCoords();
    distances = evalDistances();
}

    double TSP::eval(const std::vector<double>& instance) {
        double value = 0;
        for (size_t i = 0; i < instance.size(); ++i) {
            value += distances[instance[i - 1]][instance[i]];
        }
        value += distances[instance.back()][0];
        return value;
    }

    std::vector<double> TSP::random() {
        std::vector<double> r(routeLen - 1);
        std::iota(r.begin(), r.end(), 1);
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(r.begin(), r.end(), g);
        std::vector<double> result = {0};
        result.insert(result.end(), r.begin(), r.end());
        return result;
}

    std::vector<std::vector<double>> TSP::randCoords() {
    std::vector<std::vector<double>> c(routeLen, std::vector<double>(2, 0.0));
    for (size_t i = 0; i < routeLen; ++i) {
        c[i] = {static_cast<double>(rand() % 100), static_cast<double>(rand() % 100)};
    }
    return c;
}

    std::vector<std::vector<double>> TSP::evalDistances() {
        std::vector<std::vector<double>> d(routeLen, std::vector<double>(routeLen, 0.0));
        for (size_t i = 0; i < routeLen; ++i) {
            for (size_t j = i + 1; j < routeLen; ++j) {
                double deltaX = coords[i][0] - coords[j][0];
                double deltaY = coords[i][1] - coords[j][1];
                d[i][j] = sqrt(deltaX * deltaX + deltaY * deltaY);
                d[j][i] = d[i][j];
            }
        }
        return d;
    }

    std::vector<double> TSP::mutate(const std::vector<double>& route) {
        size_t idx1 = rand() % (routeLen - 1) + 1;
        size_t idx2 = rand() % (routeLen - 1) + 1;

        if (idx1 == idx2) {
            return mutate(route);
        } else {
            // Erstellen Sie eine Kopie der Route
            std::vector<double> newRoute = route;

            // Stellen Sie sicher, dass idx1 kleiner als idx2 ist
            if (idx1 > idx2) {
                std::swap(idx1, idx2);
            }

            // Führen Sie den 2-Kantentausch durch, indem Sie die Reihenfolge der Elemente zwischen idx1 und idx2 umkehren
            std::reverse(newRoute.begin() + idx1, newRoute.begin() + idx2);

            return newRoute;
        }
    }



