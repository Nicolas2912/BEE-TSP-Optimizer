#ifndef BEE_H
#define BEE_H

#include <vector>
#include "TSP.h"

class Bee {
public:
    int ns, nb, ne, nrb, nre, iterations;
    std::vector<std::vector<double>> bees, coords, distances;
    std::vector<double> best_objectives;
    TSP problem;

    Bee(int ns, int nb, int ne, int nrb, int nre, int iterations, TSP problem);

    void solve();

    void eliteSearch();

    void bestSearch();

    void globalFill();

    void calculateBests();

    void initialRandSolution();

};

#endif // BEE_H