"""Referee qp-referee: the chain of qp-proof.md on random DC graphs with 9..13 vertices.

Graphs: verify/equivalence/randgraphs.py (generator only, imported read-only); the DC test, the open-case pairs and
every check are own code (qpr_lib.py), as in run_graphs.py.
usage: python run_rgraphs.py <seed> <count> <workers> [nmax]
"""
import os
import sys
import json
import time
import random
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qpr_lib as L
from run_graphs import merge

OC = os.path.dirname(os.path.dirname(HERE))


def gen(seed, count, nmax):
    p = os.path.join(OC, "verify", "equivalence")
    if p not in sys.path:
        sys.path.append(p)
    import randgraphs
    rng = random.Random(seed)
    out = []
    tries = 0
    while len(out) < count and tries < 100 * count:
        tries += 1
        r = (randgraphs.gen_core_ears if tries % 2 else randgraphs.gen_planted)(rng, k=2, nmin=9, nmax=nmax)
        if r:
            out.append((r[0], [tuple(e) for e in r[1]]))
    return out


def work(item):
    gi, (n, edges) = item
    stats = {}
    errs = []
    g = L.G(n, edges)
    if not (g.comp(0) == (1 << n) - 1):
        stats["disconnected (skipped)"] = 1
        return stats, errs
    c, cv = L.cvals_all(g)
    d = [g.dist(x) for x in range(n)]
    if any(d[x][y] > 2 and c[(x, y)] > 2 for x in range(n) for y in range(n) if x != y):
        stats["graphs not DC (skipped)"] = 1
        return stats, errs
    stats["graphs DC"] = 1
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and d[u][v] == 2 and c[(u, v)] >= 3]
    rng = random.Random(gi)
    rng.shuffle(pairs)
    for (u, v) in pairs[:6]:
        try:
            zz, info = L.graph_to_zz(n, edges, u, v, stats)
            sf, cinfo = L.zz_to_sf(zz)
            L.need(L.check_lemma32_33(zz, sf, cinfo), "L3.3: answers differ")
            L.check_lemma45(sf, stats)
            yes = zz.answer()
            stats["max m"] = max(stats.get("max m", 0), sf.m)
            stats["max n"] = max(stats.get("max n", 0), n)
            if yes and sf.s != sf.t:
                Ps = L.shortest_valid_paths(sf)
                L.need(Ps, "L3.4(b)")
                allD = sf.downsets()
                for P in Ps[:50]:
                    po = L.PathObj(sf, P)
                    L.check_lemma34(sf, P, po, allD)
                    L.check_section4(sf, P, po, stats)
                    L.theorem53(sf, P, stats)
                    stats["shortest paths checked"] = stats.get("shortest paths checked", 0) + 1
            r = L.idesc_exact(sf, maxm=7)
            if r is not None:
                L.need(r == yes, "IDESC exact differs")
                stats["IDESC exact run"] = stats.get("IDESC exact run", 0) + 1
        except L.Fail as e:
            errs.append({"n": n, "edges": edges, "u": u, "v": v, "err": str(e)})
        except Exception as e:
            errs.append({"n": n, "edges": edges, "u": u, "v": v, "err": "EXC " + repr(e), "tb": traceback.format_exc()})
    return stats, errs


def main():
    seed, count, workers = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    nmax = int(sys.argv[4]) if len(sys.argv) > 4 else 13
    t0 = time.time()
    gl = gen(seed, count, nmax)
    tot = {}
    allerrs = []
    from multiprocessing import Pool
    with Pool(workers) as pool:
        for i, (st, errs) in enumerate(pool.imap_unordered(work, list(enumerate(gl)))):
            merge(tot, st)
            allerrs.extend(errs)
    tag = "rgraphs-%d-%d-%d" % (seed, count, nmax)
    with open(os.path.join(HERE, "runs", tag + ".txt"), "w") as f:
        f.write("%s: %d graphs generated, %.0fs\n" % (tag, len(gl), time.time() - t0))
        for k in sorted(tot, key=str):
            f.write("  %-32s %s\n" % (k, tot[k]))
        f.write("  errors: %d\n" % len(allerrs))
        for e in allerrs[:20]:
            f.write("  " + json.dumps(e) + "\n")
    print(open(os.path.join(HERE, "runs", tag + ".txt")).read())


if __name__ == "__main__":
    main()
