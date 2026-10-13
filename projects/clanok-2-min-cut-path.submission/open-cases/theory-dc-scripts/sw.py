"""Switch model SW (a special case of Pi): fixed bottom vertices Fb (always on the u-side, u in Fb), fixed top
vertices Ft (always on the v-side, v in Ft), fixed edges Fb-Ft (always cut), and independent switches s with
bottom neighbours Nb(s) and top neighbours Nt(s).  A switch on the v-side connects Nb(s) (it is a peak), on the
u-side it connects Nt(s).  Question: is there an assignment with u ~ v?  P2: every two switches share a bottom or
a top neighbour.  Compare with the relaxation that may use both modes of a switch.
Usage: python sw.py SEED COUNT"""
import sys, random, itertools

def connected_with(nb, nt, Fb, Ft, fixed, assign, u, v):
    # union-find over fixed vertices
    par = {x: x for x in Fb + Ft}
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    def un(a, b):
        a, b = f(a), f(b)
        if a != b: par[a] = b
    for a, b in fixed: un(a, b)
    for s, mode in enumerate(assign):
        grp = nb[s] if mode == 0 else nt[s]
        for x in grp[1:]:
            un(grp[0], x)
    return f(u) == f(v)

def relaxed(nb, nt, Fb, Ft, fixed, u, v):
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
        for grp in (nb[s], nt[s]):
            for x in grp[1:]:
                un(grp[0], x)
    return f(u) == f(v)

def valid(nb, nt, Fb, Ft, fixed, u, v):
    k = len(nb)
    for assign in itertools.product((0, 1), repeat=k):
        if connected_with(nb, nt, Fb, Ft, fixed, assign, u, v):
            return True
    return False

def p2(nb, nt):
    k = len(nb)
    return all(set(nb[a]) & set(nb[b]) or set(nt[a]) & set(nt[b]) for a in range(k) for b in range(a + 1, k))

if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    best = {}
    stats = {"inst": 0, "gap": 0}
    for it in range(count):
        nbn, ntn, k = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 7)
        Fb = ["b%d" % i for i in range(nbn)]; Ft = ["t%d" % i for i in range(ntn)]
        u, v = Fb[0], Ft[0]
        fixed = [(a, b) for a in Fb for b in Ft if rng.random() < 0.15 and not (a == u and b == v)]
        nb = [rng.sample(Fb, rng.randint(0, min(3, nbn))) for _ in range(k)]
        nt = [rng.sample(Ft, rng.randint(0, min(3, ntn))) for _ in range(k)]
        if not p2(nb, nt):
            continue
        stats["inst"] += 1
        r = relaxed(nb, nt, Fb, Ft, fixed, u, v)
        if r and not valid(nb, nt, Fb, Ft, fixed, u, v):
            stats["gap"] += 1
            # essential switches: those used by both modes... record by k
            if k not in best:
                best[k] = (Fb, Ft, fixed, nb, nt)
    print(stats)
    for k in sorted(best):
        Fb, Ft, fixed, nb, nt = best[k]
        print("k=%d fixed=%s Nb=%s Nt=%s" % (k, fixed, nb, nt))
