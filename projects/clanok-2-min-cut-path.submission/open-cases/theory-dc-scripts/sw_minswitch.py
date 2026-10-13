"""SW + P2: in yes-instances, the least number of switches that must be set (the others removed) to connect u
and v.  Usage: python sw_minswitch.py SEED COUNT"""
import sys, random, itertools
from sw import connected_with, p2

def min_switches(nb, nt, Fb, Ft, fixed, u, v):
    k = len(nb)
    for r in range(0, k + 1):
        for S in itertools.combinations(range(k), r):
            for modes in itertools.product((0, 1), repeat=r):
                nb2 = [nb[s] for s in S]; nt2 = [nt[s] for s in S]
                if connected_with(nb2, nt2, Fb, Ft, fixed, modes, u, v):
                    return r
    return None

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
dist = {}
ex = None
for it in range(count):
    nbn, ntn, k = rng.randint(3, 9), rng.randint(3, 9), rng.randint(3, 9)
    Fb = ["b%d" % i for i in range(nbn)]; Ft = ["t%d" % i for i in range(ntn)]
    u, v = Fb[0], Ft[0]
    fixed = [(a, b) for a in Fb for b in Ft if rng.random() < 0.06 and not (a == u and b == v)]
    nb = [rng.sample(Fb, rng.randint(1, min(3, nbn))) for _ in range(k)]
    nt = [rng.sample(Ft, rng.randint(1, min(3, ntn))) for _ in range(k)]
    if not p2(nb, nt):
        continue
    r = min_switches(nb, nt, Fb, Ft, fixed, u, v)
    dist[r] = dist.get(r, 0) + 1
    if r is not None and (ex is None or r > ex[0]):
        ex = (r, fixed, nb, nt)
print(dist)
print("max example:", ex)
