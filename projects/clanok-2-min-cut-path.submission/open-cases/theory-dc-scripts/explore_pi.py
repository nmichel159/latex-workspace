"""Random exploration of Problem Pi: cross-check against the simple-graph realisation, statistics of the
yes-instances and tests of candidate polynomial criteria.

Usage: python explore_pi.py SEED COUNT
"""
import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi
import dctools as T
import mcp


def gen_cuts(inst, reach, gens):
    """Smallest closed set containing u and the vertices in gens (None if it contains v)."""
    A = reach[inst.u]
    for x in gens:
        A |= reach[x]
    if (A >> inst.v) & 1:
        return None
    return A


def co_cut(inst, reach, gens):
    """Largest closed set avoiding v and every vertex of gens: complement of the set of vertices that reach
    v or a vertex of gens."""
    bad = 0
    for x in range(inst.q):
        if (reach[x] >> inst.v) & 1 or any((reach[x] >> y) & 1 for y in gens):
            bad |= 1 << x
    A = ((1 << inst.q) - 1) & ~bad
    if not (A >> inst.u) & 1:
        return None
    return A


def criterion_single(inst, res):
    """Yes if some cut cl(u, x) or the complement of the co-closure of (v, y) has a real cut path."""
    reach = res["reach"]
    for x in range(inst.q):
        A = gen_cuts(inst, reach, [x])
        if A is not None and pi.real_cut_path(inst, A) is not None:
            return True
        A = co_cut(inst, reach, [x])
        if A is not None and pi.real_cut_path(inst, A) is not None:
            return True
    return False


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    rng = random.Random(seed)
    stats = {"inst": 0, "c>=3": 0, "yes": 0, "crossok": 0, "crossbad": 0, "crit_fail": 0}
    lens = {}
    fails = []
    for it in range(count):
        q = rng.randint(5, 10)
        inst = pi.random_instance(rng, q, rng.uniform(0.2, 0.7), rng.uniform(0.0, 0.3), max_mult=rng.randint(1, 3))
        if not inst.dist_ok():
            continue
        stats["inst"] += 1
        res = pi.answer(inst, limit=20000)
        if res["c"] < 3:
            continue
        stats["c>=3"] += 1
        if res["yes"]:
            stats["yes"] += 1
            lens[res["minlen"]] = lens.get(res["minlen"], 0) + 1
            if not criterion_single(inst, res):
                stats["crit_fail"] += 1
                fails.append(inst)
        # cross-check with the realisation on small graphs
        n, E = inst.realise()
        if n <= 14 and it % 5 == 0:
            g = T.gr(n, E)
            c2, cuts2 = T.min_cut_sets(g, inst.u, inst.v)
            yes2 = any(T.shortest_in_edge_set(g, inst.u, inst.v, mcp.mask_of(T.cut_edges(g, A))) is not None for A in cuts2)
            cp = mcp.cp_brute(g, inst.u, inst.v)[0]
            ok = (c2 == res["c"]) and (yes2 == res["yes"]) and ((cp == c2) == yes2) and mcp.in_dc(g)[0]
            stats["crossok" if ok else "crossbad"] += 1
            if not ok:
                print("CROSS MISMATCH", inst.q, inst.real_edges(), inst.ears(), res["c"], c2, res["yes"], yes2, cp)
    print("seed", seed, stats, "min lengths of yes-instances:", dict(sorted(lens.items())))
    for inst in fails[:3]:
        print("criterion fails:", inst.q, "real", inst.real_edges(), "ears", inst.ears())


if __name__ == "__main__":
    main()
