#include <iostream>
#include <iomanip> // Include for std::setw and other IO manipulators
#include <string>
#include "TSP.h"
#include "Bee.h"

int main(int argc, char *argv[]) {
    int ns = 75, nb = 55, ne = 15, nrb = 25, nre = 25, routeLen = 50, iterations = 1000;
    
    if (argc >= 8) {
        try {
            ns = std::stoi(argv[1]);
            nb = std::stoi(argv[2]);
            ne = std::stoi(argv[3]);
            nrb = std::stoi(argv[4]);
            nre = std::stoi(argv[5]);
            routeLen = std::stoi(argv[6]);
            iterations = std::stoi(argv[7]);
        } catch (const std::invalid_argument& ia) {
            std::cerr << "Invalid argument: " << ia.what() << std::endl;
            return 1;
        } catch (const std::out_of_range& oor) {
            std::cerr << "Argument out of range: " << oor.what() << std::endl;
            return 1;
        }
    } else {
        std::cout << "No or insufficient input arguments. Using default values." << std::endl;
    }

    std::cout << std::left; // Align text to the left
    std::cout << "Initialize Parameters" << "\n";
    std::cout << std::setw(30) << "Number of scouts: " << std::setw(10) << ns << "\n";
    std::cout << std::setw(30) << "Number of best sites: " << std::setw(10) << nb << "\n";
    std::cout << std::setw(30) << "Number of elite sites: " << std::setw(10) << ne << "\n";
    std::cout << std::setw(30) << "Number of recruited bees: " << std::setw(10) << nrb << "\n";
    std::cout << std::setw(30) << "Number of recruited elite bees: " << std::setw(10) << nre << "\n";
    std::cout << std::setw(30) << "Number of cities: " << std::setw(10) << routeLen << "\n";
    std::cout << std::setw(30) << "Number of iterations: " << std::setw(10) << iterations << "\n";


    std::cout << "----------------------" << "\n";

    TSP tsp(routeLen);  // Create a TSP object

    Bee bee(ns, nb, ne, nrb, nre, iterations, tsp);  // Pass the TSP object to the Bee constructor

    bee.solve();

    return 0;
}