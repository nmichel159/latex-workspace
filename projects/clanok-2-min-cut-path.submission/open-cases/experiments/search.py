"""Tasks 2, 3 (O1) and 5: random instances with 9..16 vertices.

Generators (seeded, reproducible):
  gnp     G(n, p), p uniform in [0.12, 0.6], resampled until connected
  ears    random core on q vertices (G(q, p), p in [0.4, 0.9], connected) plus ears until n vertices: each ear is a
          new path with 1 or 2 inner vertices between two distinct random core-or-earlier vertices
  planted a random odd L in {3, 5, 7}, the path x_0..x_L alternating between two sides A, B; the other vertices get a
          random side; edges inside a side with probability pin, across with probability pout (pin > pout)
For every generated graph: the DC test, and for every pair u < v with d(u,v) = 2 and c(u,v) >= 3:
  exact     all u-v paths inside minimum cuts (residual-closure search), shortest length
  candidate O3 (some u-a-b-v with min cut({u,b},{a,v}) = c), computed by set-to-set max flow
  O1        every vertex of every such path has c(u,x) >= 3
Tallies per (generator, n, DC or not); examples where the candidate disagrees with the exact answer are kept
(smallest by (n, m) first).
Usage: python search.py <seconds per worker> <workers> [generators comma-separated]
"""

import os
import random
import sys
import time
import json
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutpaths as cpz  # noqa: E402
from cutpaths import mcp, Gr, PairInfo  # noqa: E402


def gen_gnp(rng, n):
    p = rng.uniform(0.12, 0.6)
    return mcp.random_connected(rng, n, p)


def gen_ears(rng, n):
    q = rng.randint(4, min(10, n - 1))
    p = rng.uniform(0.4, 0.9)
    core = mcp.random_connected(rng, q, p)
    es = list(core.edges)
    nv = q
    while nv < n:
        inner = 1 if (n - nv == 1 or rng.random() < 0.7) else 2
        a, b = rng.sample(range(nv), 2)
        if inner == 1:
            es += [(a, nv), (nv, b)]
        else:
            es += [(a, nv), (nv, nv + 1), (nv + 1, b)]
        nv += inner
    return Gr(n, es)


def gen_planted(rng, n):
    L = rng.choice([3, 5, 5, 7]) if n >= 12 else rng.choice([3, 5])
    L = min(L, n - 1 if (n - 1) % 2 == 1 else n - 2)
    side = [i % 2 for i in range(L + 1)] + [rng.randint(0, 1) for _ in range(n - L - 1)]
    pin = rng.uniform(0.3, 0.9)
    pout = rng.uniform(0.0, 0.25)
    es = [(i, i + 1) for i in range(L)]
    for a in range(n):
        for b in range(a + 1, n):
            if b == a + 1 and b <= L:
                continue
            pr = pin if side[a] == side[b] else pout
            if rng.random() < pr:
                es.append((a, b))
    g = Gr(n, es)
    if not mcp.is_connected(g):
        return None
    return g


def gen_family(rng, n):
    """Random relative of family.py: planted alternating path 0..L, u joined to some even path vertices and v to
    some odd ones, the remaining vertices are ears (degree 2, sometimes 3) on random vertices, random edges
    inside the two classes of path vertices and a few random edges across."""
    L = rng.choice([3, 5, 5, 7, 7, 9])
    while L > n - 3:
        L -= 2
    u, v = 0, L
    es = [(i, i + 1) for i in range(L)]
    pu = rng.uniform(0.4, 1.0)
    for i in range(2, L, 2):
        if rng.random() < pu:
            es.append((u, i))
    for i in range(1, L - 1, 2):
        if rng.random() < pu:
            es.append((i, v))
    qin = rng.uniform(0.0, 0.8)
    qx = rng.uniform(0.0, 0.15)
    for a in range(L + 1):
        for b in range(a + 2, L + 1):
            if (a, b) == (u, v):
                continue
            if (a - b) % 2 == 0:
                if rng.random() < qin:
                    es.append((a, b))
            elif rng.random() < qx:
                es.append((a, b))
    same = rng.uniform(0.3, 1.0)
    for w in range(L + 1, n):
        k = 2 if rng.random() < 0.8 else 3
        if rng.random() < same:
            par = rng.randint(0, 1)
            pool = [x for x in range(L + 1) if x % 2 == par]
        else:
            pool = list(range(w))
        if len(pool) < k:
            pool = list(range(w))
        for x in rng.sample(pool, k):
            es.append((x, w))
    g = Gr(n, es)
    return g if mcp.is_connected(g) else None


NCOL = 9

GENS = {"gnp": gen_gnp, "ears": gen_ears, "planted": gen_planted, "family": gen_family}


def analyze(g):
    """Per pair data for pairs with d = 2, c >= 3."""
    D = mcp.dist_matrix(g)
    dcv = cpz.dc_violations(g, D, stop=1)
    res = []
    for u in range(g.n):
        for v in range(u + 1, g.n):
            if D[u][v] != 2:
                continue
            P = PairInfo(g, u, v)
            if P.c < 3:
                continue
            paths = P.cut_paths(limit=200000)
            lens = sorted(set(len(p) - 1 for p in paths))
            cand = bool(cpz.o3_paths(g, u, v, P.c))
            o1 = True
            if paths:
                Q = cpz.class3(g, u)
                on = 0
                for p in paths:
                    for x in p:
                        on |= 1 << x
                o1 = not (on & ~Q)
            # property N: the even vertices of the path lie in N[u], the odd ones in N[v]
            Nu = (1 << u) | sum(1 << y for y, _ in g.adj[u])
            Nv = (1 << v) | sum(1 << y for y, _ in g.adj[v])
            nflags = [all(((Nu if i % 2 == 0 else Nv) >> x) & 1 for i, x in enumerate(p)) for p in paths]
            res.append((u, v, P.c, lens, cand, o1, any(nflags), all(nflags)))
    return not dcv, res


def worker(args):
    seed, seconds, gens = args
    rng = random.Random(seed)
    t0 = time.time()
    tal = {}
    examples = []
    o1_fail = []
    long_ex = []
    n_ex = []
    while time.time() - t0 < seconds:
        gname = rng.choice(gens)
        n = rng.randint(9, 16)
        g = GENS[gname](rng, n)
        if g is None:
            continue
        isdc, res = analyze(g)
        key = "%s|%d|%s" % (gname, n, "DC" if isdc else "notDC")
        t = tal.setdefault(key, [0] * NCOL)
        # graphs, pairs d=2 c>=3, pairs cp=c, pairs shortest>=5, pairs any>=5, candidate wrong, O1 fail,
        # property N fails for every path, property N fails for some path
        t[0] += 1
        for u, v, c, lens, cand, o1, nsome, nall in res:
            if lens and not nsome:
                t[7] += 1
                if len(n_ex) < 10:
                    n_ex.append((isdc, g.n, g.m, g.edges, u, v, c, lens))
            if lens and not nall:
                t[8] += 1
            t[1] += 1
            yes = bool(lens)
            if yes:
                t[2] += 1
            if yes and lens[0] >= 5:
                t[3] += 1
            if yes and lens[-1] >= 5:
                t[4] += 1
                if len(long_ex) < 30:
                    long_ex.append((isdc, g.n, g.m, g.edges, u, v, c, lens))
            if cand != (yes and lens[0] == 3):
                t[5] += 999999          # internal inconsistency between O3 and the closure search
            if cand != yes:
                t[5] += 1
                examples.append((isdc, g.n, g.m, g.edges, u, v, c, lens))
                examples.sort(key=lambda e: (not e[0], e[1], e[2]))
                del examples[20:]
            if not o1:
                t[6] += 1
                o1_fail.append((g.n, g.edges, u, v))
    return tal, examples, o1_fail[:10], long_ex, n_ex


def main():
    seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 60
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    gens = sys.argv[3].split(",") if len(sys.argv) > 3 else ["gnp", "ears", "planted"]
    tag = sys.argv[4] if len(sys.argv) > 4 else "search"
    t0 = time.time()
    tot = {}
    examples = []
    o1f = []
    longs = []
    nexs = []
    with Pool(workers) as pool:
        for tal, ex, of, le, nx_ in pool.imap_unordered(worker, [(1000 + i, seconds, gens) for i in range(workers)]):
            for k, t in tal.items():
                tt = tot.setdefault(k, [0] * NCOL)
                for i in range(NCOL):
                    tt[i] += t[i]
            examples += ex
            o1f += of
            longs += le
            nexs += nx_
    examples.sort(key=lambda e: (not e[0], e[1], e[2]))
    lines = ["%s.py run: %d workers x %.0f s, generators %s, n = 9..16" % (tag, workers, seconds, gens), "",
             "columns: graphs | pairs d=2,c>=3 | pairs with cp=c | shortest path >= 5 | some path >= 5 | "
             "candidate (O3) wrong | O1 failures | N fails for all paths | N fails for some path"]
    agg = {}
    for k in sorted(tot, key=lambda s: (s.split("|")[0], int(s.split("|")[1]), s.split("|")[2])):
        t = tot[k]
        lines.append("%-24s %7d %9d %7d %6d %6d %6d %4d %6d %6d" % (k, *t))
        g2 = k.split("|")[2]
        a = agg.setdefault(g2, [0] * NCOL)
        for i in range(NCOL):
            a[i] += t[i]
    lines.append("")
    for g2, a in sorted(agg.items()):
        lines.append("total %-6s %7d %9d %7d %6d %6d %6d %4d %6d %6d" % (g2, *a))
    lines.append("")
    lines.append("Smallest instances where the candidate disagrees with the exact answer (DC first):")
    seen = set()
    for isdc, n, m, es, u, v, c, lens in examples:
        if (n, m, tuple(es)) in seen:
            continue
        seen.add((n, m, tuple(es)))
        lines.append("  DC=%s n=%d m=%d u=%d v=%d c=%d lengths %s: %s" % (isdc, n, m, u, v, c, lens,
                                                                         " ".join("%d-%d" % e for e in es)))
        if len(seen) >= 12:
            break
    lines.append("O1 failures: %d %s" % (len(o1f), o1f[:3]))
    longs.sort(key=lambda e: (not e[0], -e[7][-1], e[1], e[2]))
    lines.append("Instances with some path of length >= 5 (longest first, DC first):")
    for isdc, n, m, es, u, v, c, lens in longs[:8]:
        lines.append("  DC=%s n=%d m=%d u=%d v=%d c=%d lengths %s: %s" % (isdc, n, m, u, v, c, lens,
                                                                         " ".join("%d-%d" % e for e in es)))
    nexs.sort(key=lambda e: (not e[0], e[1], e[2]))
    lines.append("Pairs where no path inside a minimum cut has its even vertices in N[u] and odd ones in N[v] (property N):")
    for isdc, n, m, es, u, v, c, lens in nexs[:6]:
        lines.append("  DC=%s n=%d m=%d u=%d v=%d c=%d lengths %s: %s" % (isdc, n, m, u, v, c, lens,
                                                                         " ".join("%d-%d" % e for e in es)))
    lines.append("Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-%s.txt" % tag), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
