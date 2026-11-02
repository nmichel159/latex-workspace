"""Calibration without P2: the K4 encoding and random 3-SAT encodings.  Does singleton consistency pass on no-instances when P2 fails?

Usage: calib.py SECONDS"""
import itertools
import random
import sys
import time
from collections import Counter

from closure import Graph, Refuted, closure, sac, solve
import oldfam


def report(name, I):
    G = Graph(I)
    t0 = time.time()
    try:
        closure(G, I.ALL, I.ALL)
        r0 = "pass"
    except Refuted:
        r0 = "REF"
    s = Counter()
    try:
        sac(G, I.ALL, I.ALL, s)
        r1 = "pass"
    except Refuted:
        r1 = "REF"
    s2 = Counter()
    r = solve(G, s2)
    res = "valid" if r is not None and I.is_valid_walk(r) else ("none" if r is None else "INVALID")
    print("%-20s m=%3d p2viol=%d closure=%s sac=%s solve=%s nodes=%d branches=%d deep=%d t=%.1f" % (
        name, I.m, len(I.p2_violations()), r0, r1, res, s2["nodes"], s2["branches"], s2["deep-failures"], time.time() - t0), flush=True)
    return r1, res


def main():
    import k4
    import zz
    import hunt2
    for kk, col in ((3, 2), (4, 3), (5, 4)):
        inst = k4.build(k=kk, colours=col)
        z = zz.from_sw(*hunt2.ch_to_sw(inst[:5]))
        report("K%d %d colours" % (kk, col), oldfam.from_zz(z))
    rng = random.Random(1)
    tot = Counter()
    t0 = time.time()
    while time.time() - t0 < float(sys.argv[1]):
        nv = rng.randint(4, 9)
        nc = int(nv * rng.uniform(3.5, 6.0))
        cl = []
        for _ in range(nc):
            vs = rng.sample(range(1, nv + 1), 3)
            cl.append([v if rng.random() < 0.5 else -v for v in vs])
        zi = zz.from_sat(nv, cl)[0]
        z2 = oldfam.from_zz(zi)
        G = Graph(z2)
        sat = False
        for bitsv in itertools.product([False, True], repeat=nv):
            if all(any((l > 0) == bitsv[abs(l) - 1] for l in c) for c in cl):
                sat = True
                break
        try:
            sac(G, z2.ALL, z2.ALL)
            r1 = "pass"
        except Refuted:
            r1 = "REF"
        s2 = Counter()
        r = solve(G, s2)
        tot[("sat" if sat else "unsat", "sac " + r1, "found" if r is not None else "none", "deep" if s2["deep-failures"] > 0 else "shallow")] += 1
        tot["m"] = max(tot["m"], z2.m)
        tot["p2viol"] = max(tot["p2viol"], len(z2.p2_violations()))
    print(tot)


if __name__ == "__main__":
    main()
