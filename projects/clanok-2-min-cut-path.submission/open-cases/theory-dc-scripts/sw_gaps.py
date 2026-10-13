"""SW + P2: classify relaxation gaps (relaxed-yes, valid-no) by the least number r of switches whose modes must be
fixed (others keep both modes) so that the relaxation already says no for every choice of their modes.
Usage: python sw_gaps.py SEED COUNT"""
import sys, random, itertools
from sw import connected_with, p2, valid

def relaxed_partial(nb, nt, Fb, Ft, fixed, u, v, fixmodes):
    par = {x: x for x in Fb + Ft}
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    def un(a, b):
        a, b = f(a), f(b)
        if a != b: par[a] = b
    for a, b in fixed: un(a, b)
    for s in range(len(nb)):
        modes = (fixmodes[s],) if s in fixmodes else (0, 1)
        for m in modes:
            grp = nb[s] if m == 0 else nt[s]
            for x in grp[1:]:
                un(grp[0], x)
    return f(u) == f(v)

def explain(nb, nt, Fb, Ft, fixed, u, v):
    k = len(nb)
    for r in range(1, k + 1):
        for S in itertools.combinations(range(k), r):
            if all(not relaxed_partial(nb, nt, Fb, Ft, fixed, u, v, dict(zip(S, ms))) for ms in itertools.product((0, 1), repeat=r)):
                return r
    return None

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
dist = {}
ex = {}
for it in range(count):
    nbn, ntn, k = rng.randint(3, 8), rng.randint(3, 8), rng.randint(3, 8)
    Fb = ["b%d" % i for i in range(nbn)]; Ft = ["t%d" % i for i in range(ntn)]
    u, v = Fb[0], Ft[0]
    fixed = [(a, b) for a in Fb for b in Ft if rng.random() < 0.08 and not (a == u and b == v)]
    nb = [rng.sample(Fb, rng.randint(1, min(3, nbn))) for _ in range(k)]
    nt = [rng.sample(Ft, rng.randint(1, min(3, ntn))) for _ in range(k)]
    if not p2(nb, nt):
        continue
    if not relaxed_partial(nb, nt, Fb, Ft, fixed, u, v, {}):
        continue
    if valid(nb, nt, Fb, Ft, fixed, u, v):
        continue
    r = explain(nb, nt, Fb, Ft, fixed, u, v)
    dist[r] = dist.get(r, 0) + 1
    if r not in ex:
        ex[r] = (fixed, nb, nt)
print(dist)
for r in sorted(ex, key=lambda z: (z is None, z)):
    print(r, ex[r])
