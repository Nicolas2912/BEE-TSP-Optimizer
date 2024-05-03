#ifndef TSP_H
#define TSP_H

#include <vector>

class TSP {
public:
    int routeLen;
    std::vector<std::vector<double>> coords;
    std::vector<std::vector<double>> distances;

    TSP(int routeLength);

    double eval(const std::vector<double>& instance);

    std::vector<double> random();

    std::vector<std::vector<double>> randCoords();

    std::vector<std::vector<double>> evalDistances();

    std::vector<double> mutate(const std::vector<double>& route);
};

#endif // TSP_H
