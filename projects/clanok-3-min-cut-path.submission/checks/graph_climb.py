"""Task B1, second part: hill climbing on small graphs of DC towards ZZ instances with long shortest valid walks and many incomparable pairs, so that the graph
level does not stop at walks of length three.  Every improved or sampled graph goes through all checks of graph_level.run_pair.

Usage: graph_climb.py SEED SECONDS NMAX LOG
"""
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from graph_level import G, run_pair  # noqa: E402
from zz_core import ClaimFail, Inst, bits  # noqa: E402


def build_quick(g, c_all, u, v):
    """The ZZ instance of def:zz-instance by enumeration of the minimum sides; a light version for the score only."""
    n = g.n
    c = c_all[u][v]
    uu, vv = 1 << u, 1 << v
    rest = ((1 << n) - 1) & ~uu & ~vv
    subs = [0]
    for b in bits(rest):
        subs += [s | 1 << b for s in subs]
    mins = [s | uu for s in subs if g.delta(s | uu) == c]
    Q = [u] + [x for x in range(n) if x != u and c_all[u][x] >= 3]
    idx = {x: i for i, x in enumerate(Q)}
    tr = [sum(1 << idx[x] for x in Q if A >> x & 1) for A in mins]
    up = [0] * len(Q)
    for x in range(len(Q)):
        for y in range(len(Q)):
            if all((t >> x & 1) or not (t >> y & 1) for t in tr):
                up[x] |= 1 << y
    Qm = sum(1 << x for x in Q)
    edges = []
    for a, b in g.edges:
        if Qm >> a & 1 and Qm >> b & 1:
            ia, ib = idx[a], idx[b]
            ab, ba = up[ia] >> ib & 1, up[ib] >> ia & 1
            if ab and not ba:
                edges.append((ia, ib))
            elif ba and not ab:
                edges.append((ib, ia))
    return Inst(len(Q), up, edges, idx[u], idx[v])


def score(g, u, v):
    if not g.connected():
        return None
    c_all = g.all_c()
    dd = [g.dist(i) for i in range(g.n)]
    if not g.in_DC(c_all, dd) or dd[u][v] != 2 or c_all[u][v] < 3:
        return None
    I = build_quick(g, c_all, u, v)
    w = I.shortest_walk()
    q = len(w) - 1 if w else 0
    inc = sum(1 for x in range(I.m) for y in range(x + 1, I.m) if I.inc(x, y))
    return (q, inc, I.m), c_all, dd


def main():
    seed, secs, nmax, logf = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    st = Counter()
    fails = []
    t0 = time.time()
    best_q = 0
    records = Counter()
    while time.time() - t0 < secs:
        # start: G_b-like graph or a random small one
        n = rng.randint(6, nmax)
        pr = rng.uniform(0.2, 0.6)
        e = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < pr]
        g = G(n, e)
        pairs = []
        sc = None
        for _ in range(30):
            u, v = rng.sample(range(n), 2)
            sc = score(g, u, v)
            if sc is not None:
                break
        if sc is None:
            continue
        cur = sc[0]
        for it in range(400):
            if time.time() - t0 > secs:
                break
            a, b = rng.sample(range(n), 2)
            e2 = [x for x in g.edges]
            ed = (min(a, b), max(a, b))
            if ed in e2:
                e2.remove(ed)
            else:
                e2.append(ed)
            if rng.random() < 0.3:
                c, d = rng.sample(range(n), 2)
                ed2 = (min(c, d), max(c, d))
                if ed2 in e2:
                    e2.remove(ed2)
                else:
                    e2.append(ed2)
            g2 = G(n, e2)
            sc2 = score(g2, u, v)
            if sc2 is None:
                continue
            if sc2[0] >= cur:
                improved = sc2[0] > cur
                g, cur = g2, sc2[0]
                if improved or rng.random() < 0.02:
                    try:
                        run_pair(g2, sc2[1], sc2[2], u, v, st, rng, deep=n <= 10)
                    except ClaimFail as ex:
                        fails.append((n, g2.edges, u, v, str(ex)))
                    records["q=%d" % cur[0]] += 1
                    if cur[0] > best_q:
                        best_q = cur[0]
    with open(logf, "w", encoding="utf-8") as f:
        print("seed", seed, "time", round(time.time() - t0, 1), "nmax", nmax, "best q", best_q, file=f)
        print("graphs checked by q:", dict(records), file=f)
        for k in sorted(st):
            print(k, st[k], file=f)
        print("FAILURES:", fails[:4] if fails else "none", file=f)


if __name__ == "__main__":
    main()
