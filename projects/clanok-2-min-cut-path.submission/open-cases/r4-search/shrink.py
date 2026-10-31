"""Greedy shrinking under portfolio-hardness (agent r4-search).

Property P(I): I satisfies P2, is a yes-instance, and no witness method of the portfolio at level K finds a solution
(portfolio.portfolio(..., level=K)['hard']).
Modes:
  zz   general ZZ instance; moves: delete one real edge; delete one element (not u, v); delete one cover relation
       between two classes (all pairs between the two classes; real edges between them dropped); split an element off
       its class (make it a class of its own just below / above the rest is not done; only deletions)
  sw   2CH instance; moves: remove a node from a side; merge two nodes; delete a node; delete a switch
Moves are tried in random order; the first move that keeps P(I) and reduces (q, |R|) lexicographically is applied;
stop when no move works (a local minimum: no single move keeps the property).
Usage: python shrink.py MODE START SEED K OUT
  START: a JSON instance file, or a known family name: T6tie, T6one, R8, R9, ...
"""
import sys
import json
import random
import time
from common import zz, make_zz, sw_to_zz, to_json, save, load, bits
import twoch
import swlib
import known
from portfolio import portfolio


def prop_zz(z, K, sw=None):
    if z.p2_bad():
        return False
    if not zz.exact_dfs(z)[0]:
        return False
    r = portfolio(z, level=K, sw=sw, exact_ans=True)
    return r["hard"]


def zz_moves(z):
    n, le = z.n, z.le
    mv = [("edge", e) for e in z.R]
    mv += [("elem", x) for x in range(n) if x not in (z.u, z.v)]
    # cover relations between classes
    cls = {}
    for x in range(n):
        key = tuple(y for y in range(n) if le[x][y] and le[y][x])
        cls.setdefault(key, []).append(x)
    reps = list(cls.keys())
    for a in reps:
        for b in reps:
            x, y = a[0], b[0]
            if a == b or not le[x][y]:
                continue
            if any(le[x][c[0]] and le[c[0]][y] and c not in (a, b) for c in reps):
                continue
            if z.u in a or z.v in b:
                continue   # keep u least and v greatest
            mv.append(("cover", a, b))
    return mv


def apply_zz(z, m):
    n = z.n
    le = [row[:] for row in z.le]
    R = list(z.R)
    if m[0] == "edge":
        R = [e for e in R if e != m[1]]
        return make_zz(n, le, R, z.u, z.v)
    if m[0] == "elem":
        x = m[1]
        keep = [y for y in range(n) if y != x]
        ren = {y: i for i, y in enumerate(keep)}
        le2 = [[le[a][b] for b in keep] for a in keep]
        R2 = [(ren[a], ren[b]) for a, b in R if a != x and b != x]
        return make_zz(n - 1, le2, R2, ren[z.u], ren[z.v])
    if m[0] == "cover":
        A, B = m[1], m[2]
        for a in A:
            for b in B:
                le[a][b] = False
        R2 = [(a, b) for a, b in R if le[a][b] and not le[b][a]]
        # transitivity check (removing a cover keeps it, but verify)
        for a in range(n):
            for b in range(n):
                if le[a][b]:
                    for c in range(n):
                        if le[b][c] and not le[a][c]:
                            return None
        return make_zz(n, le, R2, z.u, z.v)
    raise ValueError(m)


def sw_moves(inst):
    N, E, F, s, t = inst
    n = len(E)
    mv = []
    for i in range(n):
        for typ in (0, 1):
            S = E if typ == 0 else F
            for x in bits(S[i]):
                mv.append(("rm", i, typ, x))
    for x in range(N):
        for y in range(x + 1, N):
            if {x, y} != {s, t}:
                mv.append(("merge", x, y))
    for x in range(N):
        if x not in (s, t):
            mv.append(("del", x))
    for i in range(n):
        mv.append(("delsw", i))
    return mv


def compact(inst):
    N, E, F, s, t = inst
    used = (1 << s) | (1 << t)
    for m in list(E) + list(F):
        used |= m
    keep = [x for x in range(N) if (used >> x) & 1]
    ren = {x: i for i, x in enumerate(keep)}

    def rm(m):
        return sum(1 << ren[x] for x in keep if (m >> x) & 1)
    return (len(keep), [rm(m) for m in E], [rm(m) for m in F], ren[s], ren[t])


def apply_sw(inst, m):
    N, E, F, s, t = inst
    E, F = list(E), list(F)
    if m[0] == "rm":
        _, i, typ, x = m
        if typ == 0:
            E[i] &= ~(1 << x)
        else:
            F[i] &= ~(1 << x)
    elif m[0] == "merge":
        _, x, y = m   # y into x
        for S in (E, F):
            for i in range(len(S)):
                if (S[i] >> y) & 1:
                    S[i] = (S[i] & ~(1 << y)) | (1 << x)
        if y == s:
            s = x
        if y == t:
            t = x
    elif m[0] == "del":
        x = m[1]
        E = [e & ~(1 << x) for e in E]
        F = [f & ~(1 << x) for f in F]
    elif m[0] == "delsw":
        i = m[1]
        del E[i]
        del F[i]
    return compact((N, E, F, s, t))


def prop_sw(inst, K):
    N, E, F, s, t = inst
    if s == t or not twoch.p2_ok(E, F):
        return False
    if swlib.exact_2ch(inst) is None:
        return False
    z, names = sw_to_zz(inst)
    r = portfolio(z, level=K, sw=inst, exact_ans=True)
    return r["hard"]


def size_sw(inst):
    z, _ = sw_to_zz(inst)
    return (z.n, len(z.R))


def shrink(mode, start, rng, K, log):
    cur = start
    if mode == "zz":
        assert prop_zz(cur, K), "start instance does not have the property"
        size = (cur.n, len(cur.R))
    else:
        assert prop_sw(cur, K), "start instance does not have the property"
        size = size_sw(cur)
    log("start size %s" % (size,))
    improved = True
    while improved:
        improved = False
        moves = zz_moves(cur) if mode == "zz" else sw_moves(cur)
        rng.shuffle(moves)
        for m in moves:
            if mode == "zz":
                nxt = apply_zz(cur, m)
                if nxt is None:
                    continue
                ns = (nxt.n, len(nxt.R))
                if ns >= size:
                    continue
                if prop_zz(nxt, K):
                    cur, size = nxt, ns
                    improved = True
                    log("move %s -> size %s" % (m[0], size))
                    break
            else:
                nxt = apply_sw(cur, m)
                ns = size_sw(nxt)
                if ns >= size:
                    continue
                if prop_sw(nxt, K):
                    cur, size = nxt, ns
                    improved = True
                    log("move %s -> size %s" % (m[0], size))
                    break
    return cur, size


def start_instance(name):
    if name.endswith(".json"):
        z, sw, names = load(name)
        return ("sw", sw) if sw is not None else ("zz", z)
    if name.startswith("T"):
        L = int(name[1])
        mates = "tie" if name.endswith("tie") else "oneway"
        return "zz", known.tic_mates(L, mates)[1]
    if name.startswith("R"):
        L = int(name[1:].rstrip("H"))
        return "sw", known.rigid_2ch(L, helly=name.endswith("H"))[3]
    if name.startswith("Z"):
        # R_L as general ZZ (switch model lost after general moves)
        L = int(name[1:])
        return "zz", known.rigid_2ch(L)[1]
    raise ValueError(name)


if __name__ == "__main__":
    mode, startname, seed, K, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = random.Random(seed)
    m0, inst = start_instance(startname)
    assert m0 == mode or mode == "zz"
    if mode == "zz" and m0 == "sw":
        inst = sw_to_zz(inst)[0]
    t0 = time.time()

    def log(s):
        print("[%.0fs] %s" % (time.time() - t0, s), flush=True)
    res, size = shrink(mode, inst, rng, K, log)
    if mode == "zz":
        z, sw = res, None
    else:
        z, sw = sw_to_zz(res)[0], res
    r = portfolio(z, level=K, sw=sw, exact_ans=True, stop_early=False)
    d = to_json(z, name="shrunk-%s-%s-%d-K%d" % (mode, startname, seed, K), sw=sw, verdict=r,
                notes="greedy shrink (shrink.py) of %s, seed %d, level %d" % (startname, seed, K))
    save(out, d)
    log("final size %s verdict %s" % (size, {k: r[k] for k in ("yes", "hard")}))
