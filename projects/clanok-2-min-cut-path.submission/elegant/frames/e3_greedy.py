"""Experiment E3: greedy conflict resolution without backtracking.

GREEDY(rule): Lf = dn u, Uf = up v; repeat: W = shortest walk of the state graph; no walk: reject; W valid: accept; else take a conflict (h, l) of W and apply the rule:
  IN1: h in D (Lf |= dn h);  IN2: l in D (Lf |= dn l);  OUT1: h not in D (Uf |= up h);  OUT2: l not in D (Uf |= up l).
Sound; at most m rounds.  Completeness is the question.  Tiny random instances are compared with the exact solver.

Usage: e3_greedy.py SEED SECONDS LOG
"""
import random
import sys
import time
from collections import Counter

from common import BASES, Inst, StateGraph, WData, bits, conflicts, popcnt, random_p2_instance


def greedy(I, rule, rng=None, select="first"):
    Lf, Uf = I.DN[I.u], I.UP[I.v]
    rounds = 0
    while True:
        rounds += 1
        if Lf & Uf:
            return None, rounds
        G = StateGraph(I, I.ALL & ~Uf, I.ALL & ~Lf)
        W = G.shortest(rng)
        if W is None:
            return None, rounds
        c = conflicts(I, W)
        if not c:
            return W, rounds
        h, l = c[0] if select == "first" else rng.choice(c)
        if rule == "IN1":
            Lf |= I.DN[h]
        elif rule == "IN2":
            Lf |= I.DN[l]
        elif rule == "OUT1":
            Uf |= I.UP[h]
        else:
            Uf |= I.UP[l]


def main():
    seed, secs, logf = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    st = Counter()
    bad = {}
    t0 = time.time()
    while time.time() - t0 < secs:
        I = random_p2_instance(rng, 5, 11, sparse=rng.random() < 0.7)
        if I is None:
            continue
        st["inst"] += 1
        w = I.shortest_walk()
        if w is None:
            st["no"] += 1
            for r in ("IN1", "IN2", "OUT1", "OUT2"):
                g, _ = greedy(I, r)
                assert g is None or I.is_valid_walk(g)
                assert g is None
            continue
        st["yes"] += 1
        if I.dist_in_GD(I.dn(1 << I.u)) is not None and False:
            pass
        ok = []
        for r in ("IN1", "IN2", "OUT1", "OUT2"):
            g, rounds = greedy(I, r)
            if g is not None:
                assert I.is_valid_walk(g)
                ok.append(r)
                st["ok " + r] += 1
            else:
                st["fail " + r] += 1
                bad.setdefault(r, (I.m, sorted(I.edges), [hex(x) for x in I.UP]))
        if not ok:
            st["all four fail"] += 1
            bad.setdefault("all", (I.m, sorted(I.edges), [hex(x) for x in I.UP]))
    # planted
    pl = Counter()
    for fam in ["small", "B", "A", "stair", "ties", "mix", "cross", "allstrict", "kappa", "two"]:
        for _ in range(3):
            d = BASES[fam](rng)
            I, P = d.build()
            for r in ("IN1", "IN2", "OUT1", "OUT2"):
                g, rounds = greedy(I, r)
                pl[(fam, r, g is not None)] += 1
                if g is not None:
                    assert I.is_valid_walk(g)
    with open(logf, "w", encoding="utf-8") as f:
        for k in sorted(st):
            print(k, st[k], file=f)
        print("bad", bad, file=f)
        for k in sorted(pl):
            print(k, pl[k], file=f)


if __name__ == "__main__":
    main()
