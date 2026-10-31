"""Checks of Lemma W, Lemma D and Theorem Q (agent r5-classes, third run; r5-classes.md section 2b).

For random P2 instances with classes and every shortest valid path P (up to a limit) and both types T:
  - Lemma W: every P-consistent side not on P meets at most 3 consecutive members of P;
  - Lemma D: for every switch w of a T-class and v of an O-class: w^O meets v^O or w^T meets v^T;
  - Theorem Q: the least number c1 of O-sides of O-class switches meeting every needed O-side (O-sides of T-class
    switches), and the least number c2 of T-sides of T-class switches meeting every needed T-side; asserted
    min(c1, c2) <= floor(log2 m) + 1; for the optimal cover the mode vector sigma_U^Phi (Phi = misclassified classes
    of P) is built, |Phi| <= 3 * (number of centres) asserted, and connectivity of s, t asserted.
usage: python test_q.py SEED COUNT [NMAX] [nmax] [kmax] [pathlimit]
"""
import itertools
import math
import random
import sys
import ccore as C


def side_of(I, w, ty):
    m = I.sw[w][ty]
    return (2 * w + ty) if m else None


def min_cover(I, needed, centres):
    """least number of centre sides (from `centres`) whose union meets every side of `needed`; brute force
    (returns (size, tuple) or (None, None) if impossible)"""
    needed = list(needed)
    if not needed:
        return 0, ()
    cov = {}
    for c in centres:
        mc = I.mask[c]
        s = 0
        for i, z in enumerate(needed):
            if I.mask[z] & mc:
                s |= 1 << i
        if s:
            cov[c] = s
    full = (1 << len(needed)) - 1
    # remove dominated centres
    items = sorted(cov.items(), key=lambda kv: -bin(kv[1]).count("1"))
    keep = []
    for c, s in items:
        if not any((s | s2) == s2 for _, s2 in keep):
            keep.append((c, s))
    for k in range(1, len(keep) + 1):
        for combo in itertools.combinations(keep, k):
            u = 0
            for _, s in combo:
                u |= s
            if u == full:
                return k, tuple(c for c, _ in combo)
        if k >= 7:
            break
    return None, None


def check_path(I, P, stats):
    r = len(P)
    pt = {}
    for x in P:
        pt[I.scls[x]] = x & 1
    onP = set(P)
    pos_of_switch = {x >> 1: a for a, x in enumerate(P)}
    # Lemma W
    for y in I.sides:
        if y in onP:
            continue
        c = I.scls[y]
        if c in pt and pt[c] != (y & 1):
            continue
        hits = [a for a in range(r) if I.mask[y] & I.mask[P[a]]]
        if hits:
            assert max(hits) - min(hits) <= 2, ("Lemma W", y, hits)
            stats["W"] += 1
    m = I.n
    kq = int(math.floor(math.log2(m))) + 1 if m > 0 else 1
    for T in (0, 1):
        O = 1 - T
        Tsw = [w for w in range(I.n) if pt.get(I.cl[w]) == T]
        Osw = [v for v in range(I.n) if pt.get(I.cl[v]) == O]
        # Lemma D
        for w in Tsw:
            for v in Osw:
                ok = (I.sw[w][O] & I.sw[v][O]) or (I.sw[w][T] & I.sw[v][T])
                assert ok, ("Lemma D", w, v)
                stats["D"] += 1
        needA = [side_of(I, w, O) for w in Tsw if I.sw[w][O]]
        needB = [side_of(I, v, T) for v in Osw if I.sw[v][T]]
        centA = [side_of(I, v, O) for v in Osw if I.sw[v][O]]
        centB = [side_of(I, w, T) for w in Tsw if I.sw[w][T]]
        c1, cov1 = min_cover(I, needA, centA)
        c2, cov2 = min_cover(I, needB, centB)
        best = min(x for x in (c1, c2, 10 ** 9) if x is not None)
        assert best <= kq, ("Theorem Q", c1, c2, kq)
        stats["Q"] += 1
        stats["maxc"] = max(stats["maxc"], best)
        # build sigma_U^Phi for the better side and check connectivity and |Phi| <= 3 * centres
        for (cc, cov, tau) in ((c1, cov1, O), (c2, cov2, T)):
            if cc is None or cc != best:
                continue
            U = set()
            for z in cov:
                Zm = I.mask[z]
                for y in I.sides:
                    if (y & 1) == tau and I.mask[y] & Zm:
                        U.add(y)
            modes = {}
            for cl in I.classes:
                modes[cl] = (1 - tau) if I.Omega[(cl, tau)] <= U else tau
            phi = [cl for cl, ty in pt.items() if modes[cl] != ty]
            assert len(phi) <= 3 * cc, ("Phi", len(phi), cc)
            for cl in phi:
                modes[cl] = 1 - modes[cl]
            assert C.connected_masks(C.picked_masks(I, modes), I.s, I.t), "not connected"
            stats["phimax"] = max(stats["phimax"], len(phi))
            break


def main():
    seed = int(sys.argv[1])
    count = int(sys.argv[2])
    NMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    nmax = int(sys.argv[4]) if len(sys.argv) > 4 else 9
    kmax = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    plim = int(sys.argv[6]) if len(sys.argv) > 6 else 30
    rng = random.Random(seed)
    stats = {"inst": 0, "yes": 0, "paths": 0, "W": 0, "D": 0, "Q": 0, "maxc": 0, "phimax": 0}
    for it in range(count):
        N = rng.randint(3, NMAX)
        n = rng.randint(2, nmax)
        k = rng.randint(1, min(n, kmax))
        I = C.random_instance(rng, N, n, k, rng.choice([0.15, 0.25, 0.35]), rng.choice([0.15, 0.25, 0.35]),
                              fresh=rng.random(), p2=True)
        if not C.p2_ok(I):
            continue
        stats["inst"] += 1
        L, paths = C.shortest_valid_paths(I, limit=plim)
        if L is None:
            continue
        stats["yes"] += 1
        for P in paths:
            stats["paths"] += 1
            check_path(I, P, stats)
    print(stats, flush=True)


if __name__ == "__main__":
    main()
