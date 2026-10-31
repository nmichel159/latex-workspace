"""Gadget search, part B: simultaneous P2 repair of a 3-SAT encoding by strongest witnesses (agent r4-search).

For a no-instance I (the encoding of an unsatisfiable formula) and a direction vector c (one of 'low' / 'up' for every
incomparable pair without a witness) let I_c be I plus, for every such pair, its strongest witness of direction c_p
(gadgets.strongest), all added at once (transitive closure taken; it adds no relation among the old elements).
CEGAR: a SAT solver (minisat.py) proposes c (pairs blocked in one direction are fixed, blocked pairs make the problem infeasible);
the exact solver checks I_c; if I_c has a consistent zigzag, the witness elements on it give the clause
'some of these pairs takes the other direction' (the zigzag stays consistent in every I_c' that agrees with c on
them); repeat until a c with I_c a no-instance is found (a P2 completion that keeps the formula unsatisfiable) or the
clauses are infeasible (no completion by strongest witnesses; for E3 this means no conservative completion at all,
report Section 5.2).
Usage: python gadgets_b.py ENC SEED COUNT [MAXIT] [--bt]   (--bt: witnesses in the classes of u / v)   (ENC in E1, E2, E3; all4 plus COUNT random unsat formulas)"""
import sys
import json
import random
import time
import minisat
from common import zz, make_zz, HERE
from gadgets import enc_e1, enc_e2, enc_e3, analyse, random_unsat


def completion(z, pairs, c):
    """I plus strongest witnesses: pair p = (x, y) gets a new element n + p of direction c[p]."""
    n, le, lt = z.n, z.le, z.lt
    k = len(pairs)
    N = n + k
    L = [[False] * N for _ in range(N)]
    for a in range(n):
        for b in range(n):
            L[a][b] = le[a][b]
    R = list(z.R)
    for p, (x, y) in enumerate(pairs):
        w = n + p
        L[w][w] = True
        if c[p] == "low":
            for a in range(n):
                if lt[a][x] and lt[a][y]:
                    L[a][w] = True
                if le[x][a] or le[y][a]:
                    L[w][a] = True
            R += [(w, x), (w, y)]
        else:
            for a in range(n):
                if lt[x][a] and lt[y][a]:
                    L[w][a] = True
                if le[a][x] or le[a][y]:
                    L[a][w] = True
            R += [(x, w), (y, w)]
    # transitive closure (relations between new elements only)
    for m in range(N):
        Lm = L[m]
        for i in range(N):
            if L[i][m]:
                Li = L[i]
                for j in range(N):
                    if Lm[j]:
                        Li[j] = True
    for a in range(n):
        for b in range(n):
            assert L[a][b] == le[a][b], "not conservative"
    return make_zz(N, L, R, z.u, z.v)


def completion_bt(z, pairs, c):
    """I plus, for every pair, a private witness in the class of u (c = 'low') or of v (c = 'up'); such witnesses
    are comparable with every element, so the result satisfies P2 if every old pair got one."""
    n, le = z.n, z.le
    k = len(pairs)
    N = n + k
    L = [[False] * N for _ in range(N)]
    for a in range(n):
        for b in range(n):
            L[a][b] = le[a][b]
    B = [a for a in range(n) if le[a][z.u]]
    T = [a for a in range(n) if le[z.v][a]]
    R = list(z.R)
    for p, (x, y) in enumerate(pairs):
        w = n + p
        if c[p] == "low":
            for a in range(N):
                L[w][a] = True
            for b in B:
                L[b][w] = True
            R += [(w, x), (w, y)]
        else:
            for a in range(N):
                L[a][w] = True
            for t in T:
                L[w][t] = True
            R += [(x, w), (y, w)]
    for p in range(k):
        w = n + p
        if c[p] == "low":
            for q in range(k):
                if c[q] == "low":
                    L[w][n + q] = L[n + q][w] = True
        else:
            for q in range(k):
                if c[q] == "up":
                    L[w][n + q] = L[n + q][w] = True
    return make_zz(N, L, R, z.u, z.v)


MODE = "strongest"


def cegar(z, maxit=2000, log=None):
    bad, blocked, only_low, only_up, both = analyse(z)
    if blocked:
        return {"status": "blocked", "blocked": len(blocked), "pairs": len(bad)}
    pairs = list(bad)
    idx = {p: i for i, p in enumerate(pairs)}
    fixed = {}
    for p in only_low:
        fixed[idx[p] + 1] = True       # True = low
    for p in only_up:
        fixed[idx[p] + 1] = False
    clauses = []
    n = z.n
    t0 = time.time()
    prefer = {}
    for it in range(maxit):
        sol = minisat.solve(len(pairs), clauses, fixed, prefer)
        if sol is None:
            return {"status": "infeasible", "iterations": it, "pairs": len(pairs), "time": time.time() - t0}
        c = ["low" if sol[i + 1] else "up" for i in range(len(pairs))]
        prefer = dict(sol)
        zc = completion(z, pairs, c) if MODE == "strongest" else completion_bt(z, pairs, c)
        ok, walk = zz.exact_dfs(zc)
        if not ok:
            p2ok = not zc.p2_bad()
            return {"status": "completion", "p2": p2ok, "iterations": it, "pairs": len(pairs), "c": c,
                    "n_low": c.count("low"), "time": time.time() - t0}
        used = sorted({w - n for w in walk if w >= n})
        if not used:
            raise AssertionError("I itself is a yes-instance")
        clauses.append([-(p + 1) if c[p] == "low" else (p + 1) for p in used])
        if log and it % 50 == 0:
            log("  it %d used %d" % (it, len(used)))
    return {"status": "undecided", "iterations": maxit, "pairs": len(pairs)}


if __name__ == "__main__":
    enc_name, seed, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if "--bt" in sys.argv:
        MODE = "bt"
        sys.argv.remove("--bt")
    maxit = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    enc = {"E1": enc_e1, "E2": enc_e2, "E3": enc_e3}[enc_name]
    rng = random.Random(seed)
    formulas = [("all4", 2, [[1, 2], [1, -2], [-1, 2], [-1, -2]])]
    for i in range(count):
        nv = rng.randint(2, 4)
        width = rng.choice([2, 3]) if nv >= 3 else 2
        mcl = rng.randint(4, 8)
        formulas.append(("rand%d" % i, nv, random_unsat(rng, nv, mcl, width)))
    out = open("%s/runs/gadgets-B-%s-%s-%d.jsonl" % (HERE, enc_name, MODE, seed), "w")
    tot = {}
    for name, nv, cls in formulas:
        z, names = enc(nv, cls)
        r = cegar(z, maxit, log=lambda s: print(s, flush=True))
        tot[r["status"]] = tot.get(r["status"], 0) + 1
        r2 = {k: v for k, v in r.items() if k != "c"}
        print(name, nv, cls, "q=%d" % z.n, r2, flush=True)
        rec = {"name": name, "nv": nv, "clauses": cls, "q": z.n, "result": r}
        if "c" in r and names:
            rec["design"] = [[str(names[a]), str(names[b]), d] for (a, b), d in zip(z.p2_bad(), r["c"])]
        out.write(json.dumps(rec) + "\n")
        out.flush()
    print("FINAL %s seed=%d %s" % (enc_name, seed, tot), flush=True)
