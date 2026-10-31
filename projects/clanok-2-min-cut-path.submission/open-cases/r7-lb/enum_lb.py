"""Exact single-term cost on all ZZ instances with K middle elements (r7-lb.md Section 3.1).

usage: python enum_lb.py K PART NPARTS LOG [MODE] [SAMPLES] [SEED]
MODE 'all' (default): every preorder on the K middle elements (as relation matrices; verify/rv-r6-core/enum8.preorders),
  u strictly below and v strictly above every middle element, every set R of strict pairs except {u, v}; preorders
  with index = PART mod NPARTS.  MODE 'canon': one preorder per isomorphism class (canonical form under all
  permutations of the middle elements), every R.  MODE 'sample': SAMPLES random (preorder, R) pairs (seed SEED).
Per P2 yes-instance (switch form by verify/rv-r6-core/zzl.zz_to_sw): cost = lbcore.brute_mincost (every term of total
cost <= 4, flips arbitrary) and, for cost >= 1, cross-check with lbcore.mincost (exact search over the minimal pairs).
Records the distribution of the cost and saves an instance of every new maximum (lbcore.dump) next to LOG.
"""
import sys
import os
import time
import random
import itertools
from collections import Counter
import lbcore
from lbcore import brute_mincost, mincost
from zzl import zz_to_sw, zz_p2


def preorders(K):
    pairs = [(a, b) for a in range(K) for b in range(K) if a != b]
    out = []
    for mask in range(1 << len(pairs)):
        le = [[a == b for b in range(K)] for a in range(K)]
        for i, (a, b) in enumerate(pairs):
            if (mask >> i) & 1:
                le[a][b] = True
        if all(not (le[a][b] and le[b][c]) or le[a][c] for a in range(K) for b in range(K) for c in range(K)):
            out.append(le)
    return out


def canon(le, K):
    best = None
    for p in itertools.permutations(range(K)):
        key = tuple(le[p[a]][p[b]] for a in range(K) for b in range(K))
        if best is None or key < best:
            best = key
    return best


def instance(K, lem, mask):
    q = K + 2
    le = [[False] * q for _ in range(q)]
    for a in range(q):
        le[0][a] = True
        le[a][1] = True
        le[a][a] = True
    for a in range(K):
        for b in range(K):
            le[a + 2][b + 2] = lem[a][b]
    strict = [(0, w) for w in range(2, q)] + [(w, 1) for w in range(2, q)]
    strict += [(a + 2, b + 2) for a in range(K) for b in range(K) if lem[a][b] and not lem[b][a]]
    R = [strict[i] for i in range(len(strict)) if (mask >> i) & 1]
    return q, le, R, len(strict)


def run_one(K, lem, mask, st, best, logdir, out):
    q, le, R, _ = instance(K, lem, mask)
    st["instances"] += 1
    if not zz_p2(q, le, R):
        return
    st["P2"] += 1
    I, mid = zz_to_sw(q, 0, 1, le, R)
    if I.s == I.t:
        st["yes s=t"] += 1
        st["cost=0"] += 1
        return
    if not lbcore.is_yes(I):
        st["no"] += 1
        return
    st["yes"] += 1
    c = brute_mincost(I, cap=4)
    if c is None:
        c = ">4"
        st["COST >4"] += 1
    st["cost=%s" % c] += 1
    if c != 0:
        r = mincost(I, cap=8)
        if r["total"] != (c if isinstance(c, int) else r["total"]) or not r.get("verified"):
            st["MISMATCH brute/mincost FAIL"] += 1
            out("mismatch K=%d R=%r brute=%r mincost=%r" % (K, R, c, r))
    if isinstance(c, int) and c > best[0]:
        best[0] = c
        path = os.path.join(logdir, "enum-K%d-max-cost%d.json" % (K, c))
        lbcore.dump(I, path, dict(K=K, R=R, le=[[int(b) for b in row] for row in le], cost=c))
        out("new max cost %d (m=%d, R=%r) saved %s" % (c, I.m, R, path))


def main():
    K, part, nparts = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    logp = sys.argv[4]
    mode = sys.argv[5] if len(sys.argv) > 5 else "all"
    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
    logdir = os.path.dirname(os.path.abspath(logp))
    logf = open(logp, "a", encoding="utf-8")

    def out(s):
        print(s, flush=True)
        logf.write(s + "\n")
        logf.flush()
    st = Counter()
    best = [-1]
    t0 = time.time()
    pres = preorders(K)
    out("enum_lb K=%d part %d/%d mode %s preorders %d pid %d" % (K, part, nparts, mode, len(pres), os.getpid()))
    if mode == "sample":
        rng = random.Random(seed)
        for it in range(samples):
            lem = rng.choice(pres)
            _, _, _, ns = instance(K, lem, 0)
            run_one(K, lem, rng.getrandbits(ns), st, best, logdir, out)
            if (it + 1) % 20000 == 0:
                out("  sample %d  yes %d  costs %s  %.0fs" % (it + 1, st["yes"], sorted(
                    (k, v) for k, v in st.items() if k.startswith("cost=")), time.time() - t0))
    else:
        if mode == "canon":
            seen = set()
            cp = []
            for lem in pres:
                key = canon(lem, K)
                if key not in seen:
                    seen.add(key)
                    cp.append(lem)
            pres = cp
            out("canonical preorders %d" % len(pres))
        for pi, lem in enumerate(pres):
            if pi % nparts != part:
                continue
            _, _, _, ns = instance(K, lem, 0)
            for mask in range(1 << ns):
                run_one(K, lem, mask, st, best, logdir, out)
            out("  preorder %d/%d strict %d  instances %d  yes %d  costs %s  %.0fs" % (
                pi + 1, len(pres), ns, st["instances"], st["yes"],
                sorted((k, v) for k, v in st.items() if k.startswith("cost=")), time.time() - t0))
    out("SUMMARY enum_lb K=%d part %d/%d mode %s (%.0fs)" % (K, part, nparts, mode, time.time() - t0))
    for k in sorted(st):
        out("  %s: %d" % (k, st[k]))


if __name__ == "__main__":
    main()
