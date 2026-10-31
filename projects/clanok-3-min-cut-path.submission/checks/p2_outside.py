"""The step "z in Q" of lem:zz-instance(c) uses neither d(u, v) = 2 nor G in DC, so it is tested on all graphs with c(u, v) >= 3: an incomparable pair must not
have a common neighbour outside Q.  The experiment that tries to create the forbidden case adds an ear (a new vertex of degree two) between an incomparable
pair: the proof predicts that the pair stops being incomparable, or that the common neighbour joins Q.

Usage: p2_outside.py SEED SECONDS LOG FILE_G8
"""
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from graph_level import G, from_g6, random_graph  # noqa: E402
from zz_core import ClaimFail, bits, chk  # noqa: E402


def analyse(g, u, v):
    """Q, the relation <= by enumeration of minimum sides (in any connected graph); None if c(u, v) < 3."""
    c = g.cvalue(u, v)
    if c < 3:
        return None
    n = g.n
    uu, vv = 1 << u, 1 << v
    rest = ((1 << n) - 1) & ~uu & ~vv
    subs = [0]
    for b in bits(rest):
        subs += [s | 1 << b for s in subs]
    mins = [s | uu for s in subs if g.delta(s | uu) == c]
    Q = [u] + [x for x in range(n) if x != u and g.cvalue(u, x) >= 3]
    leq = {}
    for x in Q:
        for y in Q:
            leq[(x, y)] = all((A >> x & 1) or not (A >> y & 1) for A in mins)
    return Q, leq, mins, c


def check(g, u, v, st, rng, ears=True):
    r = analyse(g, u, v)
    if r is None:
        return
    Q, leq, mins, c = r
    Qm = sum(1 << x for x in Q)
    st["pairs with c >= 3"] += 1
    incs = []
    for i, x in enumerate(Q):
        for y in Q[i + 1:]:
            if not leq[(x, y)] and not leq[(y, x)]:
                incs.append((x, y))
                st["incomparable pairs"] += 1
                chk(not g.nb[x] >> y & 1, "incomparable elements adjacent")
                cn = g.nb[x] & g.nb[y]
                st["incomparable pairs with a common neighbour"] += 1 if cn else 0
                chk(cn & ~Qm == 0, "a common neighbour outside Q of an incomparable pair")
    if ears and incs and g.n < 13:
        x, y = rng.choice(incs)
        z = g.n
        g2 = G(g.n + 1, list(g.edges) + [(x, z), (y, z)])
        st["ears added between incomparable elements"] += 1
        r2 = analyse(g2, u, v)
        chk(r2 is not None, "c stays at least 3")
        Q2, leq2, mins2, c2 = r2
        chk(z not in Q2, "the ear vertex has degree two")
        if x in Q2 and y in Q2:
            inc2 = not leq2[(x, y)] and not leq2[(y, x)]
            chk(not inc2, "the ear vertex is a common neighbour outside Q of an incomparable pair")
            st["ear: the pair became comparable"] += 1


def main():
    seed, secs, logf, g8 = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3], sys.argv[4]
    rng = random.Random(seed)
    st = Counter()
    fails = []
    t0 = time.time()
    from networkx.generators.atlas import graph_atlas_g
    graphs = [G(H.number_of_nodes(), list(H.edges())) for H in graph_atlas_g() if H.number_of_nodes() >= 3]
    with open(g8) as f:
        graphs += [from_g6(ln.strip()) for ln in f if ln.strip()]
    for g in graphs:
        if time.time() - t0 > secs * 0.6:
            st["exhaustive part cut by the time limit"] += 1
            break
        if not g.connected():
            continue
        st["graphs"] += 1
        for u in range(g.n):
            for v in range(g.n):
                if u != v:
                    try:
                        check(g, u, v, st, rng)
                    except ClaimFail as ex:
                        fails.append((g.n, g.edges, u, v, str(ex)))
    while time.time() - t0 < secs:
        g = random_graph(rng)
        if not g.connected():
            continue
        st["random graphs"] += 1
        u, v = rng.sample(range(g.n), 2)
        try:
            check(g, u, v, st, rng)
        except ClaimFail as ex:
            fails.append((g.n, g.edges, u, v, str(ex)))
    with open(logf, "w", encoding="utf-8") as f:
        print("seed", seed, "time", round(time.time() - t0, 1), file=f)
        for k in sorted(st):
            print(k, st[k], file=f)
        print("FAILURES:", fails[:4] if fails else "none", file=f)


if __name__ == "__main__":
    main()
