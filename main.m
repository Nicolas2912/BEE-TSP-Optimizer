% Initialize parameters
rng("default");
inp.routeLen = 50;
ns = 75;
nb = 55;
ne = 15;
nrb = 25;
nre = 25;
iterations = 200;
animation = false;
tsp = TSP(inp);
bee = Bee(ns, nb, ne, nrb, nre, iterations, animation, tsp);
bee.solve();
