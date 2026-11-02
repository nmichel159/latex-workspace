"""Planted families: closure and singleton consistency, on the base instances and after hill climbing with the moves of run_planted.py.

Usage: q3_planted.py SEED SECONDS LOG [moves] [families]
"""
import json
import random
import sys
import time
from collections import Counter

from wd import Budget, WS, bits, popcnt
from closure import Graph, Refuted, alive_conflicts, bfs_walk, closure, sac, solve
from zz_design import BASES
from run_planted import design_move, inst_move

FAMS = ["A", "B", "stair", "ties", "mix", "cross", "allstrict", "small", "kappa", "two"]


def test(I, P, st, tag):
    G = Graph(I)
    t0 = time.time()
    try:
        AL, AH, _ = closure(G, I.ALL, I.ALL)
    except Refuted:
        st[tag + " closure REFUTES YES"] += 1
        return False
    cf0 = alive_conflicts(I, AL, AH)
    st[tag + " tests"] += 1
    w0 = bfs_walk(G, AL, AH)
    if I.is_valid_walk(w0):
        st[tag + " closure+bfs valid"] += 1
    if not cf0:
        st[tag + " closure no conflicts"] += 1
    t1 = time.time()
    try:
        AL, AH = sac(G, AL, AH)
    except Refuted:
        st[tag + " SAC REFUTES YES"] += 1
        return False
    t2 = time.time()
    w1 = bfs_walk(G, AL, AH)
    if I.is_valid_walk(w1):
        st[tag + " sac+bfs valid"] += 1
    cf1 = alive_conflicts(I, AL, AH)
    if not cf1:
        st[tag + " sac no conflicts"] += 1
    st[tag + " maxconf0"] = max(st[tag + " maxconf0"], len(cf0))
    st[tag + " maxconf1"] = max(st[tag + " maxconf1"], len(cf1))
    st[tag + " time sac"] = max(st[tag + " time sac"], round(t2 - t1, 2))
    s2 = Counter()
    r = solve(G, s2)
    if r is None or not I.is_valid_walk(r):
        st[tag + " SOLVE FAILED"] += 1
        return False
    st[tag + " solve nodes max"] = max(st[tag + " solve nodes max"], s2["nodes"])
    st[tag + " deep failures"] += s2["deep-failures"]
    return True


def main():
    seed, secs, logf = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    moves = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    fams = sys.argv[5].split(",") if len(sys.argv) > 5 else FAMS
    rng = random.Random(seed)
    res = {}
    t0 = time.time()
    while time.time() - t0 < secs:
        for fam in fams:
            if time.time() - t0 > secs:
                break
            st = res.setdefault(fam, Counter())
            d = BASES[fam](rng)
            I, P = d.build()
            if not I.p2():
                continue
            try:
                if I.shortest_walk(bound=len(P) - 1, budget=60000) is not None:
                    continue
            except Budget:
                continue
            st["m"] = max(st["m"], I.m)
            test(I, P, st, "base")
            na = 0
            for mv in range(moves):
                if time.time() - t0 > secs:
                    break
                d2 = d.copy()
                kind = design_move(d2, rng)
                if kind == "none":
                    continue
                I2, P2 = d2.build()
                if not I2.p2():
                    continue
                try:
                    if I2.shortest_walk(bound=len(P2) - 1, budget=60000) is not None:
                        continue
                except Budget:
                    continue
                d, I, P = d2, I2, P2
                na += 1
            if moves:
                st["accepted design moves"] += na
                test(I, P, st, "dsat")
            na = 0
            for mv in range(moves):
                if time.time() - t0 > secs:
                    break
                kind, J = inst_move(I, P, rng)
                if J is None:
                    continue
                try:
                    if J.shortest_walk(bound=len(P) - 1, budget=60000) is not None:
                        continue
                except Budget:
                    continue
                I = J
                na += 1
            if moves:
                st["accepted inst moves"] += na
                test(I, P, st, "isat")
            with open(logf, "w", encoding="utf-8") as f:
                print("time", round(time.time() - t0), file=f)
                for fam2 in sorted(res):
                    print(fam2, dict(sorted(res[fam2].items())), file=f)
    print("done")


if __name__ == "__main__":
    main()
