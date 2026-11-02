"""Closure and singleton consistency on the instances of the earlier rounds."""
import sys
import time
from collections import Counter

from wd import Budget
from closure import Graph, Refuted, bfs_walk, closure, sac, solve
import oldfam


def run(name, I):
    G = Graph(I)
    try:
        ex = I.shortest_walk(budget=300000)
        yes = ex is not None
    except Budget:
        yes = None
    t0 = time.time()
    try:
        closure(G, I.ALL, I.ALL)
        r0 = "pass"
    except Refuted:
        r0 = "REF"
    st = Counter()
    try:
        AL, AH = sac(G, I.ALL, I.ALL, st)
        r1 = "pass"
    except Refuted:
        r1 = "REF"
    s2 = Counter()
    r = solve(G, s2)
    res = "valid" if r is not None and I.is_valid_walk(r) else ("none" if r is None else "INVALID")
    p2 = I.p2()
    print("%-34s m=%3d p2=%d exact=%s closure=%s sac=%s solve=%s nodes=%d deep=%d t=%.1f" % (name, I.m, p2, yes, r0, r1, res, s2["nodes"], s2["deep-failures"], time.time() - t0), flush=True)
    return yes, r0, r1, res, s2


def main():
    tot = Counter()
    for nm, I in oldfam.hubs() + oldfam.ladders():
        y, r0, r1, res, s2 = run(nm, I)
        tot[(y, r1, res)] += 1
    for nm, I in oldfam.saved():
        y, r0, r1, res, s2 = run(nm, I)
        tot[(y, r1, res)] += 1
    print(tot)


if __name__ == "__main__":
    main()
