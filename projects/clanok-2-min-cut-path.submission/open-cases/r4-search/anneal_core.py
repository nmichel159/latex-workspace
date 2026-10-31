"""Annealing for core yes-instances of general ZZ + P2 that defeat the newest methods (agent r4-search).

State: a general ZZ instance (preorder with ties and one-way relations, middle edges), u = 0, v = n - 1.
Constraints kept at every step: P2, yes-instance (zz.exact_dfs), the core (Theorem R of r4-general does not apply
after forced-exit propagation: hyb.analyse(...)['core']).
Score (maximised): failures of the witness methods, weighted:
   G2 + LAT2 + GC2 + NG2 + 2 HYB(1,0,1,3) + HYB(1,1,2,6) + HYB(2,1,4,8)   (each 1 if the method fails)
minus 0.02 q.  Moves: add / delete a real edge; add / delete a cover relation between middle classes; tie two
middle elements; add a twin of a middle element (same relations, random part of its edges); add a middle element
between two random elements; delete an element.  After a move P2 is repaired by random witness edges.
Metropolis acceptance with a geometric temperature schedule; every new best is saved.
Usage: python anneal_core.py START SEED STEPS OUT.json
  START: a JSON instance, 'Z2', 'ZB2', 'Z3', or 'rand:NM' (a random core instance with NM middle elements)."""
import sys
import math
import random
import time
import json
from common import zz, make_zz, to_json, save, load, to_gc, HERE
import gcert
import mixed
from portfolio import Masks, guess, lattice2
from hyb import analyse, rng_ng


def closure(le):
    n = len(le)
    le = [row[:] for row in le]
    for k in range(n):
        lk = le[k]
        for i in range(n):
            if le[i][k]:
                li = le[i]
                for j in range(n):
                    if lk[j]:
                        li[j] = True
    return le


def norm(n, le, R):
    """valid instance or None: u = 0 least, v = n - 1 greatest, not equivalent; R strictly increasing."""
    if le[n - 1][0]:
        return None
    for x in range(n):
        if not le[0][x] or not le[x][n - 1]:
            return None
    R2 = set()
    for a, b in R:
        if le[a][b] and not le[b][a] and (a, b) != (0, n - 1):
            R2.add((a, b))
        elif le[b][a] and not le[a][b] and (b, a) != (0, n - 1):
            R2.add((b, a))
    return make_zz(n, le, sorted(R2), 0, n - 1)


def middle(z):
    return [x for x in range(z.n) if not z.le[x][0] and not z.le[z.n - 1][x]]


def repair_p2(rng, z):
    n, le, lt = z.n, z.le, z.lt
    R = set(z.R)
    for _ in range(3):
        bad = make_zz(n, le, sorted(R), 0, n - 1).p2_bad()
        if not bad:
            return make_zz(n, le, sorted(R), 0, n - 1)
        for x, y in bad:
            cands = [w for w in range(n) if (lt[w][x] and lt[w][y]) or (lt[x][w] and lt[y][w])]
            w = rng.choice(cands)
            for t in (x, y):
                e = (w, t) if lt[w][t] else (t, w)
                if e != (0, n - 1):
                    R.add(e)
    zz2 = make_zz(n, le, sorted(R), 0, n - 1)
    return zz2 if not zz2.p2_bad() else None


def move(rng, z):
    n, le = z.n, [row[:] for row in z.le]
    R = list(z.R)
    mid = middle(z)
    k = rng.random()
    if k < 0.25:
        pairs = [(a, b) for a in range(n) for b in range(n) if z.lt[a][b] and (a, b) != (0, n - 1)
                 and (a, b) not in set(R)]
        if not pairs:
            return None
        R.append(rng.choice(pairs))
        return norm(n, le, R)
    if k < 0.45:
        if not R:
            return None
        R.remove(rng.choice(R))
        return norm(n, le, R)
    if k < 0.55 and len(mid) >= 2:
        x, y = rng.sample(mid, 2)
        if le[x][y] or le[y][x]:
            return None
        le[x][y] = True
        return norm(n, closure(le), R)
    if k < 0.65 and len(mid) >= 2:
        x, y = rng.sample(mid, 2)
        if not (le[x][y] and not le[y][x]):
            return None
        # remove x <= y if it is a cover between the classes
        if any(le[x][c] and le[c][y] and not le[c][x] and not le[y][c] for c in mid):
            return None
        cx = [a for a in range(n) if le[a][x] and le[x][a]]
        cy = [b for b in range(n) if le[b][y] and le[y][b]]
        for a in cx:
            for b in cy:
                le[a][b] = False
        for a in range(n):
            for b in range(n):
                if le[a][b]:
                    for c in range(n):
                        if le[b][c] and not le[a][c]:
                            return None
        return norm(n, le, R)
    if k < 0.72 and len(mid) >= 2:
        x, y = rng.sample(mid, 2)
        if le[x][y] or le[y][x]:
            return None
        le[x][y] = le[y][x] = True
        return norm(n, closure(le), R)
    if k < 0.85 and mid:
        # twin of x inserted before v
        x = rng.choice(mid)
        N = n + 1
        w = n - 1          # new element takes index n-1; v moves to n
        L = [[False] * N for _ in range(N)]
        for a in range(n - 1):
            for b in range(n - 1):
                L[a][b] = le[a][b]
            L[a][n] = True
        L[n][n] = True
        for a in range(n - 1):
            if a == x:
                continue
            if le[a][x]:
                L[a][w] = True
            if le[x][a]:
                L[w][a] = True
        L[w][w] = True
        L[w][n] = True
        L[x][w] = L[w][x] = False
        if rng.random() < 0.3:
            L[x][w] = L[w][x] = True     # a tied twin
        L = closure(L)
        R2 = [(a if a != n - 1 else n, b if b != n - 1 else n) for a, b in R]
        for a, b in R:
            if b == x and rng.random() < 0.7:
                R2.append((a if a != n - 1 else n, w))
            if a == x and rng.random() < 0.7:
                R2.append((w, b if b != n - 1 else n))
        return norm(N, L, R2)
    if k < 0.92:
        N = n + 1
        w = n - 1
        L = [[False] * N for _ in range(N)]
        for a in range(n - 1):
            for b in range(n - 1):
                L[a][b] = le[a][b]
            L[a][n] = True
        L[n][n] = True
        L[w][w] = True
        L[w][n] = True
        lo = rng.choice(list(range(n - 1)))
        L[lo][w] = True
        cand_hi = [b for b in range(n - 1) if not le[b][lo]]
        if cand_hi and rng.random() < 0.7:
            L[w][rng.choice(cand_hi)] = True
        L = closure(L)
        if L[w][0] or L[N - 1][w]:
            return None
        R2 = [(a if a != n - 1 else n, b if b != n - 1 else n) for a, b in R]
        others = [a for a in range(N) if a != w]
        for _ in range(rng.randint(2, 4)):
            a = rng.choice(others)
            R2.append((a, w))
        return norm(N, L, R2)
    if mid:
        x = rng.choice(mid)
        keep = [y for y in range(n) if y != x]
        ren = {y: i for i, y in enumerate(keep)}
        le2 = [[le[a][b] for b in keep] for a in keep]
        R2 = [(ren[a], ren[b]) for a, b in R if a != x and b != x]
        return norm(n - 1, le2, R2)
    return None


def score(z):
    """(score, details) or None if the constraints fail."""
    if z.p2_bad():
        return None
    if not zz.exact_dfs(z)[0]:
        return None
    a = analyse(z, all_params=True, with_thr=False)
    if a["prop_refutes"] or not a["core"]:
        return None
    M = Masks(z)
    d = {}
    d["G2"] = guess(M, 2) is None
    d["LAT2"] = lattice2(M) is None
    I = to_gc(z)
    d["GC2"] = gcert.certificate(I, 2) is None
    d["NG2"] = rng_ng.ng(I, 2, 0) is None
    d["HYB13"] = not a["hyb_all"]["(1, 0, 1, 3)"]
    d["HYB26"] = not a["hyb_all"]["(1, 1, 2, 6)"]
    d["HYB48"] = not a["hyb_all"]["(2, 1, 4, 8)"]
    s = d["G2"] + d["LAT2"] + d["GC2"] + d["NG2"] + 2 * d["HYB13"] + d["HYB26"] + d["HYB48"] - 0.02 * z.n
    return s, d


def start_instance(name, rng):
    if name.endswith(".json"):
        return load(name)[0]
    if name.startswith("Z"):
        import os
        sys.path.append(os.path.join(HERE, "..", "r4-general"))
        import zfam
        k = int(name[-1])
        I, names, info = zfam.zfam(k, block=name.startswith("ZB"))
        return make_zz(I.n, I.le, I.R, I.u, I.v)
    if name.startswith("rand:"):
        nm = int(name.split(":")[1])
        while True:
            I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
            z = make_zz(I.n, I.le, I.R, I.u, I.v)
            if score(z) is not None:
                return z
    raise ValueError(name)


def main():
    start, seed, steps, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    cur = start_instance(start, rng)
    # make the start a valid state
    cs = score(cur)
    assert cs is not None, "start lacks the constraints"
    best, bs = cur, cs
    T0, T1 = 1.0, 0.05
    t0 = time.time()
    for step in range(steps):
        T = T0 * (T1 / T0) ** (step / max(1, steps - 1))
        nxt = move(rng, cur)
        if nxt is None:
            continue
        if nxt.p2_bad():
            nxt = repair_p2(rng, nxt)
            if nxt is None:
                continue
        if nxt.n > 40:
            continue
        ns = score(nxt)
        if ns is None:
            continue
        dlt = ns[0] - cs[0]
        if dlt >= 0 or rng.random() < math.exp(dlt / T):
            cur, cs = nxt, ns
            if cs[0] > bs[0]:
                best, bs = cur, cs
                print("[%.0fs] step %d new best %.2f q=%d |R|=%d %s" % (time.time() - t0, step, bs[0], best.n,
                                                                         len(best.R), bs[1]), flush=True)
                save(out, to_json(best, name="anneal-core-%d" % seed, verdict=bs[1],
                                  notes="anneal_core.py from %s seed %d step %d score %.2f" % (start, seed, step,
                                                                                               bs[0])))
        if step % 500 == 0:
            print("[%.0fs] step %d cur %.2f (q=%d) best %.2f" % (time.time() - t0, step, cs[0], cur.n, bs[0]),
                  flush=True)
    print("final best %.2f %s" % (bs[0], bs[1]), flush=True)


if __name__ == "__main__":
    main()
