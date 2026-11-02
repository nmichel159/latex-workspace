"""Tiny random P2 instances: does the closure, or singleton consistency, decide them?  Compared with the exact solver.

Usage: q3_tiny.py SEED SECONDS LOG [mmax]
"""
import json
import random
import sys
import time
from collections import Counter

from wd import Inst, bits
from closure import Graph, Refuted, bfs_walk, closure, exact_alive, sac, solve

sys.path.insert(0, ".")
import run_tiny  # noqa: E402  (from checks/)


def gen_big(rng, mmax):
    """Middle elements with a random preorder, tops and bottoms as witnesses; many no-instances."""
    k = rng.randint(3, mmax)
    m = k + 2
    p = rng.uniform(0.02, 0.35)
    up = [1 << i for i in range(m)]
    up[0] = (1 << m) - 1
    for i in range(m):
        up[i] |= 2
    for i in range(2, m):
        for j in range(2, m):
            if i != j and rng.random() < p:
                up[i] |= 1 << j
    ch = True
    while ch:
        ch = False
        for i in range(m):
            for j in bits(up[i]):
                if up[j] & ~up[i]:
                    up[i] |= up[j]
                    ch = True
    I0 = Inst(m, up, [], 0, 1)
    pairs = [(x, y) for x in range(m) for y in bits(I0.USTR[x])]
    q = rng.uniform(0.05, 0.35)
    edges = {e for e in pairs if rng.random() < q}
    from run_planted import repair_p2
    rp = repair_p2(up, edges, m, 0, 1, rng, 60)
    if rp is None:
        return None
    up, edges, m = rp
    return Inst(m, up, edges, 0, 1)


def main():
    seed, secs, logf = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    mmax = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    rng = random.Random(seed)
    st = Counter()
    bad = []
    t0 = time.time()
    last = t0
    while time.time() - t0 < secs:
        I = run_tiny.random_instance(rng) if rng.random() < 0.3 else gen_big(rng, mmax)
        if I is None:
            continue
        if not I.p2():
            continue
        st["inst"] += 1
        w = I.shortest_walk()
        yes = w is not None
        st["yes" if yes else "no"] += 1
        G = Graph(I)
        # level 0 closure
        try:
            AL, AH, _ = closure(G, I.ALL, I.ALL)
            ref0 = False
        except Refuted:
            ref0 = True
        try:
            AL1, AH1 = sac(G, I.ALL, I.ALL)
            ref1 = False
        except Refuted:
            ref1 = True
        if yes and (ref0 or ref1):
            st["UNSOUND"] += 1
            bad.append(("unsound", I.m, sorted(I.edges), [hex(x) for x in I.UP]))
        if not yes:
            if ref0:
                st["no: closure refutes"] += 1
            if ref1:
                st["no: sac refutes"] += 1
            else:
                st["no: SAC PASSES"] += 1
                if len(bad) < 40:
                    bad.append(("sac-passes-no", I.m, sorted(I.edges), [hex(x) for x in I.UP]))
        else:
            # does the BFS walk after sac give a valid walk?
            w1 = bfs_walk(G, AL1, AH1)
            if I.is_valid_walk(w1):
                st["yes: sac + bfs valid"] += 1
            else:
                st["yes: sac + bfs invalid"] += 1
            s2 = Counter()
            r = solve(G, s2)
            if r is None or not I.is_valid_walk(r):
                st["SOLVE FAILED"] += 1
            st["solve nodes"] += s2["nodes"]
            st["solve maxdepth"] = max(st["solve maxdepth"], s2["maxdepth"])
            st["solve deep-failures"] += s2["deep-failures"]
            st["solve branches"] += s2["branches"]
        if time.time() - last > 20:
            last = time.time()
            with open(logf, "w", encoding="utf-8") as f:
                print(dict(sorted(st.items())), file=f)
                print(json.dumps(bad[:6]), file=f)
    with open(logf, "w", encoding="utf-8") as f:
        print(dict(sorted(st.items())), file=f)
        print(json.dumps(bad[:6]), file=f)


if __name__ == "__main__":
    main()
