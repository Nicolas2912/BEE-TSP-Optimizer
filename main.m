% Initialize parameters
rng("default");
inp.routeLen = 100;
ns = 75;
nb = 55;
ne = 15;
nrb = 25;
nre = 25;
iterations = 1000;
animation = false;
tsp = TSP(inp);
bee = Bee(ns, nb, ne, nrb, nre, iterations, animation, tsp);
bee.solve();
