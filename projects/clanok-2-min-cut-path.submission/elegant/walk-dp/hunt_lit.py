"""Structured P2 no-instances: take a planted yes-instance and fix literals at random.  Each fixed instance has P2 (asserted).  Compare the exact answer with singleton consistency on each.

A no-instance on which SAC passes refutes the conjecture "SAC decides ZZ with P2".
Modes: node = SAC probing nodes as in closure.sac.

Usage: hunt_lit.py SEED SECONDS LOG [families]
"""
import json
import random
import sys
import time
from collections import Counter

from wd import Budget, bits
from closure import Graph, Refuted, alive_conflicts, closure, sac
from literal import fix_high, fix_low
from zz_design import BASES
from run_planted import design_move, inst_move

FAMS = ["A", "B", "stair", "ties", "mix", "cross", "allstrict", "small", "kappa", "two"]


def sac_pass(I):
    G = Graph(I)
    try:
        sac(G, I.ALL, I.ALL)
        return True
    except Refuted:
        return False


def main():
    seed, secs, logf = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    fams = sys.argv[4].split(",") if len(sys.argv) > 4 else FAMS
    rng = random.Random(seed)
    res = {}
    found = []
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
            # a few moves to leave the pure design
            for _ in range(rng.randint(0, 6)):
                kind, J = inst_move(I, P, rng)
                if J is None:
                    continue
                try:
                    if J.shortest_walk(bound=len(P) - 1, budget=40000) is None:
                        I = J
                except Budget:
                    pass
            st["starts"] += 1
            for rnd in range(rng.randint(1, 8)):
                # fix one literal on an element with an alive conflict; prefer the side not refuted at once
                G = Graph(I)
                try:
                    AL, AH, _ = closure(G, I.ALL, I.ALL)
                except Refuted:
                    st["closure refuted before move"] += 1
                    break
                cand = alive_conflicts(I, AL, AH)
                if not cand:
                    st["no conflicts left"] += 1
                    break
                n = rng.choice(cand)
                x = n >> 1
                # a literal against the node: x high killed means x in D, x low killed means x not in D
                J = fix_low(I, x) if n & 1 else fix_high(I, x)
                if J is None:
                    continue
                if not J.p2():
                    st["P2 LOST (bug)"] += 1
                    break
                st["fixed"] += 1
                try:
                    ex = J.shortest_walk(budget=120000)
                except Budget:
                    st["budget"] += 1
                    continue
                p = sac_pass(J)
                if ex is None:
                    st["no-inst"] += 1
                    if p:
                        st["NO BUT SAC PASSES"] += 1
                        found.append(dict(m=J.m, up=[hex(z) for z in J.UP], edges=sorted(J.edges), u=J.u, v=J.v, fam=fam))
                        with open(logf + ".FOUND.json", "w", encoding="utf-8") as f:
                            json.dump(found[:20], f)
                    else:
                        st["no: refuted"] += 1
                else:
                    st["yes-inst"] += 1
                    if not p:
                        st["YES BUT SAC REFUTES (bug)"] += 1
                    I = J
            with open(logf, "w", encoding="utf-8") as f:
                print("time", round(time.time() - t0), file=f)
                for fam2 in sorted(res):
                    print(fam2, dict(sorted(res[fam2].items())), file=f)


if __name__ == "__main__":
    main()
