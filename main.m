% Initialize parameters
rng("default");
inp.routeLen = 200;
ns = 80;
nb = 55;
ne = 15;
nrb = 25;
nre = 25;
iterations = 1000;
tsp = BeeTSP(inp, ns, nb, ne, nrb, nre, iterations);

tsp.solve();
