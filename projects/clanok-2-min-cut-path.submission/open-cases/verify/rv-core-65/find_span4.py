"""Find and describe instances in which S_x = A & NE(E#x) (x not in L) spans 5 consecutive positions (span 4), the
largest span allowed by the reviewer's sharpened Lemma 6.3 (rv-core-65.md Section 2.3); saves the first few as JSON
and prints, for each element a of S_x, its witness type: (i) X_a meets E_x, (ii-P) a common lower middle neighbour z
on P, (ii-o) z off P; and whether x is on P.

usage: python find_span4.py SEED COUNT MMIN MMAX [MAXSAVE]
"""
import os
import sys
import json
import random
from collections import Counter
from gsf import bits, random_inst
from thy import Stars, Skel


def witness_types(I, St, K, x, a):
    out = []
    if I.E[x] & I.E[a]:
        out.append("i")
    for z in I.lmn[x] & I.lmn[a]:
        out.append("ii-P" if (K.onP >> z) & 1 else "ii-o")
    return out


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    maxsave = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    rng = random.Random(seed)
    st = Counter()
    saved = 0
    os.makedirs(os.path.join("runs", "span4"), exist_ok=True)
    for it in range(count):
        m = rng.randint(mmin, mmax)
        I = random_inst(rng, m, p_order=rng.choice([0.3, 0.45]), p_tie=rng.choice([0, 0.3]),
                        p_side=rng.choice([0.12, 0.2]), p_med=rng.choice([0.5, 0.8]),
                        repair=["low", "up", "low", "up", "freshE", "freshF"])
        if not I.p2() or I.s == I.t:
            continue
        r, paths = I.shortest_paths(cap=30)
        if r is None:
            continue
        St = Stars(I)
        for P in paths:
            K = Skel(I, P)
            for x in range(I.m):
                if (K.L >> x) & 1:
                    continue
                S = St.NEstar[x] & K.A
                if not S:
                    continue
                ps = sorted(K.pos[a] for a in bits(S))
                span = ps[-1] - ps[0]
                st["span %d" % span] += 1
                if span >= 4:
                    onP = bool((K.onP >> x) & 1)
                    types = {K.pos[a]: witness_types(I, St, K, x, a) for a in bits(S)}
                    win = [c for c in range(1, K.r + 1) if I.side_mask(P[c - 1]) & I.E[x]]
                    key = "x on P" if onP else ("x off P, window %s" % ("empty" if not win else "non-empty"))
                    st["span >= 4: " + key] += 1
                    if saved < maxsave:
                        saved += 1
                        fn = os.path.join("runs", "span4", "span4-%d-%d.json" % (seed, saved))
                        d = I.to_json()
                        d["path"] = [list(sd) for sd in P]
                        d["x"] = x
                        json.dump(d, open(fn, "w"))
                        print("saved %s: m %d, r %d, x %d (%s), window %s, positions -> witness types %s"
                              % (fn, I.m, K.r, x, key, win, dict(sorted(types.items()))), flush=True)
                    if span > 4:
                        st["SPAN > 4 (REVIEWER'S BOUND FAILS)"] += 1
    print("find_span4 seed %d count %d m %d-%d: %s" % (seed, count, mmin, mmax, dict(sorted(st.items()))))


if __name__ == "__main__":
    main()
