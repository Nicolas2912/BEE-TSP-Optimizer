% Initialize parameters
rng("default");
inp.routeLen = 100;
ns = 75;
nb = 55;
ne = 15;
nrb = 25;
nre = 25;
iterations = 3000;
tsp = BeeTSP(inp, ns, nb, ne, nrb, nre, iterations);

tsp.solve();
