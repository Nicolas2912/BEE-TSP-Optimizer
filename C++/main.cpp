#include <iostream>
#include <string>
#include "TSP.h"
#include "Bee.h"

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " <number of cities> <number of iterations>" << std::endl;
        return 1;
    }
    int routeLen = std::stoi(argv[1]);
    int iterations = std::stoi(argv[2]);
/*    int routeLen = 100;
    int iterations = 1000;*/

    std::cout << "Initialize Parameters" << "\n";
    std::cout << "Number of cities: " << routeLen << "\n";
    std::cout << "Number of iterations: " << iterations << "\n";

    std::cout << "----------------------" << "\n";

    TSP tsp(routeLen);  // Create a TSP object

    std::cout << "Coordinates: \n";
    for (auto &coord: tsp.coords) {
        std::cout << coord[0] << " " << coord[1] << "\n";
    }
    std::cout << "----------------------" << "\n";

    Bee bee(75, 55, 15, 25, 25, iterations, tsp);  // Pass the TSP object to the Bee constructor

    bee.solve();

    return 0;
}