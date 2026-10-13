"""Cross-check of chaincsp.pimc_chaincsp (Theorem A) against brute force over all minimum cuts.

Families: (R) random connected graphs G(n, p), random pair; (P) Pi-instances of theory-dc-scripts/pi.py (random and
planted) realised as simple graphs (ears = degree-two vertices; the question is then asked in G itself);
(F) the long-path family G_k of theory-dc.md Theorem 8.  For every instance: same answer, the witness passes the
independent test of Lemma 6, and the largest values after arc consistency always form a solution (max-closure).
Usage: python test_chaincsp.py SEED COUNT [workers]"""
import os
import sys
import random
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "theory-dc-scripts")))
import chaincsp as C  # noqa: E402
import mcp  # noqa: E402
import pi  # noqa: E402


def gk(k):
    n = 4 * k + 2
    xs = list(range(2 * k + 2))
    a = [2 * k + 2 + i for i in range(k)]
    b = [3 * k + 2 + i for i in range(k)]
    E = [(xs[i], xs[i + 1]) for i in range(2 * k + 1)]
    ev = xs[0::2]
    od = xs[1::2]
    E += [(p, q) for i, p in enumerate(ev) for q in ev[i + 1:]]
    E += [(p, q) for i, p in enumerate(od) for q in od[i + 1:]]
    for i in range(1, k + 1):
        E += [(a[i - 1], 0), (a[i - 1], xs[2 * i])]
        E += [(b[i - 1], xs[2 * i - 1]), (b[i - 1], xs[2 * k + 1])]
    return n, E, 0, 2 * k + 1


def one(args):
    fam, seed = args
    rng = random.Random(seed)
    if fam == "R":
        n = rng.randint(5, 13)
        p = rng.choice([0.25, 0.35, 0.5, 0.7])
        g = mcp.random_connected(rng, n, p)
        u, v = rng.sample(range(n), 2)
    elif fam == "P":
        q = rng.randint(5, 9)
        if rng.random() < 0.5:
            inst = pi.random_instance(rng, q, rng.choice([0.3, 0.45, 0.6]), rng.choice([0.1, 0.25]))
        else:
            inst = None
            while inst is None:
                inst = pi.planted_instance(rng, q, rng.randint(1, max(1, (q - 2) // 2)), 0.4, 0.15, 0.1)
        n, E = inst.realise()
        g = mcp.Gr(n, E)
        if not mcp.is_connected(g):
            return fam, seed, "skip", None
        u, v = inst.u, inst.v
    else:
        k = 1 + seed % 4
        n, E, u, v = gk(k)
        g = mcp.Gr(n, E)
    t0 = time.time()
    yes, path, st = C.pimc_chaincsp(g, u, v)
    t1 = time.time()
    by, bp, ncuts = C.pimc_brute(g, u, v)
    t2 = time.time()
    ok = yes == by
    wit_ok = True
    if yes:
        wit_ok = C.path_in_some_min_cut(g, u, v, path)
    status = "ok" if ok and wit_ok and st["maxfail"] == 0 else "BAD"
    info = {"n": g.n, "m": g.m, "u": u, "v": v, "c": st["c"], "yes": yes, "brute": by, "path": path,
            "nodes": st["nodes"], "maxfail": st["maxfail"], "ncuts": ncuts, "t_alg": t1 - t0, "t_brute": t2 - t1,
            "len": None if path is None else len(path) - 1, "edges": g.edges if status == "BAD" else None}
    return fam, seed, status, info


if __name__ == "__main__":
    seed0, count = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    jobs = [(fam, seed0 * 1000003 + i) for i in range(count) for fam in ("R", "P")] + \
           [("F", k) for k in range(8)]
    stats = {}
    bad = []
    lens = {}
    maxnodes = 0
    with Pool(workers) as pool:
        for fam, seed, status, info in pool.imap_unordered(one, jobs, chunksize=8):
            key = (fam, status, None if info is None else info["yes"])
            stats[key] = stats.get(key, 0) + 1
            if info is not None:
                maxnodes = max(maxnodes, info["nodes"])
                if info["yes"]:
                    lens[info["len"]] = lens.get(info["len"], 0) + 1
            if status == "BAD":
                bad.append((fam, seed, info))
    for k in sorted(stats, key=str):
        print(k, stats[k])
    print("witness lengths:", dict(sorted(lens.items())))
    print("max search nodes:", maxnodes)
    print("BAD:", len(bad))
    for b in bad[:5]:
        print(b)
