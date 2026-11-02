"""Harness power: deliberately wrong versions of the algorithm must be caught by brute force."""
import random
from core import solve, brute_cp, sample_instance, bfs, brute_brute_cp, edges_of
rng = random.Random(7)
miss = {'no_swap': 0, 'first_square': 0, 'x_only': 0}
n = 0
bb = 0
while n < 20000:
    s = sample_instance(rng)
    if s is None:
        continue
    g, adj, u, v = s
    n += 1
    cp = brute_cp(adj, u, v)
    if len(edges_of(adj)) <= 12 and bb < 400:
        assert cp == brute_brute_cp(adj, u, v)
        bb += 1
    d = bfs(adj, u)[0][v]
    for m in miss:
        r = solve(adj, u, v, rng=rng, mutation=m)
        if r['outcome'] == 'none' and cp == d:
            miss[m] += 1
print('instances', n, 'wrong answers by mutant', miss, 'brute vs definition checked on', bb)
