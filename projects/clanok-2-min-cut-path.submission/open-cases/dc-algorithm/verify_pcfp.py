"""Independent check of a PC false positive (no import of zz.py, pcfast.py or tieslib.py).

Input: a JSON file {"n", "le" (0/1 matrix of the preorder), "R" (pairs), "u", "v"}.
Checks, all from the definitions of theory-dc.md Section 3 (problem ZZ):
  1. le is a preorder, u least, v greatest; every R pair is strict; {u, v} not in R.
  2. P2: every two incomparable elements have a common R-neighbour strictly below both or strictly above both.
  3. Exact answer: enumerate all down-sets of the quotient order containing u and not v (closed sets of classes), and
     search the graph of R-edges crossing the down-set for a u-v path.
  4. Strong path consistency of the path-position CSP with L positions: variables 0..L-1, values = R-edges (t, h)
     with t < h; position 0 has t = u, position L-1 has h = v; positions j, j+1 share the head if j is even
     (0-based), the tail if j is odd; every two positions hold compatible edges (not h <= t' and not h' <= t).
     Relations are sets of value pairs; PC-2 style fixpoint R_jk <- R_jk & (R_jl o R_lk) for all l, domains
     included as R_jj.
Usage: python verify_pcfp.py FILE.json [L ...]"""
import sys
import json
import itertools
from collections import deque


def load(fn):
    d = json.load(open(fn))
    n = d["n"]
    le = [[bool(x) for x in row] for row in d["le"]]
    R = [tuple(e) for e in d["R"]]
    return n, le, R, d["u"], d["v"]


def check_instance(n, le, R, u, v):
    for a in range(n):
        assert le[a][a]
        for b in range(n):
            for c in range(n):
                if le[a][b] and le[b][c]:
                    assert le[a][c]
        assert le[u][a] and le[a][v]
    lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
    E = []
    for a, b in R:
        if lt[b][a]:
            a, b = b, a
        assert lt[a][b], "R pair not strict"
        assert (a, b) != (u, v)
        E.append((a, b))
    return lt, sorted(set(E))


def p2(n, le, lt, E):
    nb = [set() for _ in range(n)]
    for a, b in E:
        nb[a].add(b)
        nb[b].add(a)
    bad = []
    for x in range(n):
        for y in range(x + 1, n):
            if le[x][y] or le[y][x]:
                continue
            if not any((lt[w][x] and lt[w][y]) or (lt[x][w] and lt[y][w]) for w in nb[x] & nb[y]):
                bad.append((x, y))
    return bad


def exact(n, le, E, u, v):
    # classes
    rep = {}
    classes = []
    for x in range(n):
        for c in classes:
            if le[x][c[0]] and le[c[0]][x]:
                c.append(x)
                break
        else:
            classes.append([x])
    cu = [c for c in classes if u in c][0]
    cv = [c for c in classes if v in c][0]
    mids = [c for c in classes if c is not cu and c is not cv]
    count = 0
    for mask in range(1 << len(mids)):
        D = set(cu)
        for i, c in enumerate(mids):
            if (mask >> i) & 1:
                D |= set(c)
        # down-set?
        if any(le[y][x] and y not in D for x in D for y in range(n)):
            continue
        count += 1
        adj = [[] for _ in range(n)]
        for a, b in E:
            if a in D and b not in D:
                adj[a].append(b)
                adj[b].append(a)
        seen = {u}
        dq = deque([u])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    dq.append(y)
        if v in seen:
            return True, count
    return False, count


def pc(le, E, u, v, L):
    D = len(E)
    compat = [[not le[h][t2] and not le[h2][t] for (t2, h2) in E] for (t, h) in E]

    def base(j, k, a, b):
        if j == k:
            return a == b
        if not compat[a][b]:
            return False
        lo, hi = min(j, k), max(j, k)
        if hi == lo + 1:
            ea, eb = (E[a], E[b]) if j == lo else (E[b], E[a])
            if lo % 2 == 0:
                return ea[1] == eb[1]      # share the head
            return ea[0] == eb[0]          # share the tail
        return True

    dom = []
    for j in range(L):
        s = set(range(D))
        if j == 0:
            s = {a for a in s if E[a][0] == u}
        if j == L - 1:
            s = {a for a in s if E[a][1] == v}
        dom.append(s)
    Rel = {}
    for j in range(L):
        for k in range(L):
            Rel[(j, k)] = {(a, b) for a in dom[j] for b in dom[k] if base(j, k, a, b)}
    changed = True
    while changed:
        changed = False
        for j in range(L):
            for k in range(L):
                for l in range(L):
                    rjl, rlk = Rel[(j, l)], Rel[(l, k)]
                    succ = {}
                    for a, c in rjl:
                        succ.setdefault(a, set()).add(c)
                    pred = {}
                    for c, b in rlk:
                        pred.setdefault(b, set()).add(c)
                    new = {(a, b) for (a, b) in Rel[(j, k)] if succ.get(a, set()) & pred.get(b, set())}
                    if new != Rel[(j, k)]:
                        Rel[(j, k)] = new
                        Rel[(k, j)] = {(b, a) for (a, b) in new}
                        changed = True
                        if not new:
                            return False, Rel
    return all(Rel[(j, k)] for j in range(L) for k in range(L)), Rel


if __name__ == "__main__":
    n, le, R, u, v = load(sys.argv[1])
    lt, E = check_instance(n, le, R, u, v)
    bad = p2(n, le, lt, E)
    ex, cnt = exact(n, le, E, u, v)
    print("n", n, "|R|", len(E), "P2 violations", len(bad), "down-sets checked", cnt, "exact", ex, flush=True)
    Ls = [int(x) for x in sys.argv[2:]] or [n if n % 2 else n - 1]
    for L in Ls:
        ok, _ = pc(le, E, u, v, L)
        print("L", L, "PC", ok, flush=True)
