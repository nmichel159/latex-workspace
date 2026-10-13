"""Driver of statements.py.

Part A: all connected graphs with 2..N vertices (networkx atlas, N <= 7), all pairs with c(u,v) = 2
        (both orders up to 6 vertices), all non-empty sub-families of the minimum cuts when there are at most
        `cap` cuts, otherwise the full family, the single cuts and random sub-families.
Part B: random chains of blocks (own generator), with and without the class.
Part C: random graphs G(n, p), n = 8..10.

Usage: python -B run_statements.py [--maxn 7] [--chains 600] [--random 400] [--jobs 16] [--cap 6]
"""

import argparse
import os
import random
import sys
import time
from collections import Counter
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref
import statements


def atlas(nmin, nmax):
    import networkx as nx
    from networkx.generators.atlas import graph_atlas_g
    for G in graph_atlas_g():
        n = G.number_of_nodes()
        if nmin <= n <= nmax and n >= 2 and nx.is_connected(G):
            yield n, sorted(G.edges())


def random_block(rng, size, dense):
    vs = list(range(size))
    es = set()
    for i in range(1, size):
        es.add((rng.randrange(i), i))
    for i in range(size):
        for j in range(i + 1, size):
            if rng.random() < (0.85 if dense else 0.35):
                es.add((i, j))
    return vs, es


def random_chain(rng, dense):
    """A chain of blocks joined by two routes with 0..2 one- or two-vertex parts each, plus pendant parts."""
    k = rng.randint(2, 5)
    edges = []
    nxt = [0]

    def new():
        nxt[0] += 1
        return nxt[0] - 1

    blocks = []
    for _ in range(k):
        size = rng.choice([1, 1, 2, 3, 3, 4, 4, 5] if not dense else [1, 2, 2, 3, 3, 4])
        vs, es = random_block(rng, size, dense)
        names = [new() for _ in vs]
        edges += [(names[a], names[b]) for a, b in es]
        blocks.append(names)
    for i in range(k - 1):
        for _ in range(2):
            prev = rng.choice(blocks[i])
            for _ in range(rng.choice([0, 0, 1, 1, 2])):
                a = new()
                edges.append((prev, a))
                prev = a
                if rng.random() < 0.3:
                    b = new()
                    edges.append((a, b))
                    if rng.random() < 0.5:
                        c = new()
                        edges += [(a, c), (b, c)]
                    prev = b
            edges.append((prev, rng.choice(blocks[i + 1])))
    if rng.random() < 0.3:
        a = new()
        edges.append((rng.randrange(a), a))
    u = rng.choice(blocks[0])
    v = rng.choice(blocks[-1])
    edges = sorted({(min(a, b), max(a, b)) for a, b in edges if a != b})
    return nxt[0], edges, u, v


def work(task):
    kind, n, edges, u, v, seed, cap = task
    adj = ref.graph(edges)
    for x in range(n):
        adj.setdefault(x, set())
    rng = random.Random(seed)
    done, info, fails = statements.check_pair(adj, u, v, rng, cap=cap)
    info["pairs"] += 1
    if ref.in_class(adj)[0]:
        info["pairs in a graph of the class"] += 1
    return kind, done, info, [(f, edges, u, v) for f in fails[:5]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxn", type=int, default=7)
    ap.add_argument("--chains", type=int, default=600)
    ap.add_argument("--random", type=int, default=400)
    ap.add_argument("--jobs", type=int, default=16)
    ap.add_argument("--cap", type=int, default=6)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    tasks = []
    for n, edges in atlas(2, args.maxn):
        adj = ref.graph(edges)
        for x in range(n):
            adj.setdefault(x, set())
        for u in range(n):
            for v in range(n):
                if u == v or (n == 7 and u > v):
                    continue
                if ref.cutvalue(adj, u, v, limit=3) == 2:
                    tasks.append(("atlas", n, edges, u, v, rng.randrange(10 ** 9), args.cap))
    made = 0
    tries = 0
    while made < args.chains and tries < 200 * args.chains + 1000:
        tries += 1
        dense = rng.random() < 0.5
        n, edges, u, v = random_chain(rng, dense)
        if n > 16 or u == v:
            continue
        adj = ref.graph(edges)
        if len(adj) != n or len(ref.comp(adj, u)) != n or ref.cutvalue(adj, u, v, limit=3) != 2:
            continue
        tasks.append(("chain", n, edges, u, v, rng.randrange(10 ** 9), min(args.cap, 5)))
        made += 1
    made = 0
    tries = 0
    while made < args.random and tries < 100000:
        tries += 1
        n = rng.randint(8, 10)
        p = rng.uniform(0.2, 0.4)
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < p]
        adj = ref.graph(edges) if edges else {}
        if len(adj) != n or len(ref.comp(adj, 0)) != n:
            continue
        pairs = [(a, b) for a in range(n) for b in range(n) if a != b and ref.cutvalue(adj, a, b, limit=3) == 2]
        if not pairs:
            continue
        u, v = rng.choice(pairs)
        tasks.append(("random", n, edges, u, v, rng.randrange(10 ** 9), min(args.cap, 5)))
        made += 1

    t0 = time.time()
    totals = {}
    with Pool(args.jobs) as pool:
        for kind, done, info, fails in pool.imap_unordered(work, tasks, chunksize=8):
            d, i, f = totals.setdefault(kind, (Counter(), Counter(), []))
            d.update(done)
            i.update(info)
            if len(f) < 20:
                f.extend(fails)
    for kind in ("atlas", "chain", "random"):
        if kind not in totals:
            continue
        d, i, f = totals[kind]
        print("==== %s ====" % kind)
        print("checks performed (name: count):")
        for name in sorted(d):
            print("  %-42s %d" % (name, d[name]))
        print("information (not failures):")
        for name in sorted(i):
            print("  %-70s %d" % (name, i[name]))
        print("FAILURES: %d" % len(f))
        for item in f[:20]:
            print("  ", item)
    print("time: %.0f s, tasks: %d" % (time.time() - t0, len(tasks)))


if __name__ == "__main__":
    main()
