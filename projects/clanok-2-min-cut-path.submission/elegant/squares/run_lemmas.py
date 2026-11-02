"""Check the statements of the proposed Section 4 against their definitions, by enumeration of all subsets.

Usage: run_lemmas.py SEED COUNT

For each instance with at most 13 vertices:
 L1  a set A with u in A, v not in A has |delta(A)| = 2 iff no arc of D leaves it;
 L2  u in X_0, v in X_t, every A_j is a minimum side, G[X_j] connected, no minimum side splits a layer;
 L3  the layers are the pieces of the article (components of G minus the union F of all minimum cuts);
     the squares are the article's squares (contain u or v, or entered by two edges of F);
 L4  entry x, exit y of a square, x != y: c(x,y) >= 3;
 L5  criterion: for every u-v path R (all simple paths up to a cap), G minus R has a u-v path iff no square
     has alpha_j, beta_j in different components of G[X_j] minus R;
 L6  characterization: the square/entry/exit/path condition (with all paths p of G[X]) holds iff cp = d.
"""
import itertools
import json
import random
import sys
import time
from collections import Counter

from core import (make_layers, sample_instance, ek, edges_of, connected, bfs, simple_paths, path_edges, flow,
                  brute_cp, residual_out)


def delta(adj, A):
    return [(x, y) for x, y in edges_of(adj) if (x in A) != (y in A)]


def all_min_sides(adj, u, v):
    others = [x for x in range(len(adj)) if x not in (u, v)]
    out = []
    for r in range(1 << len(others)):
        A = {u} | {others[i] for i in range(len(others)) if r >> i & 1}
        if len(delta(adj, A)) == 2:
            out.append(A)
    return out


def crossing(R, A):
    """Edges of R in delta(A), in order of R."""
    return [(a, b) for a, b in zip(R, R[1:]) if (a in A) != (b in A)]


def alpha_beta(L, R, j):
    """alpha_j, beta_j of the path R (None for a layer skipped by the second route)."""
    u, v = L.u, L.v
    if j == 0:
        al = u
    else:
        A = L.side(j - 1)
        cr = crossing(R, A)
        assert len(cr) == 1
        d = delta(L.adj, A)
        assert len(d) == 2
        s = [e for e in d if ek(*e) != ek(*cr[0])]
        assert len(s) == 1
        s = s[0]
        al = s[0] if s[0] not in A else s[1]
    if j == L.t:
        be = v
    else:
        A = L.side(j)
        cr = crossing(R, A)
        assert len(cr) == 1
        d = delta(L.adj, A)
        s = [e for e in d if ek(*e) != ek(*cr[0])]
        assert len(s) == 1
        s = s[0]
        be = s[0] if s[0] in A else s[1]
    return al, be


def check(adj, u, v, rng, st):
    val, L = make_layers(adj, u, v, rng, shuffle_order=True, cycles=rng.randint(0, 2))
    assert val == 2
    out = residual_out(adj, L.H)
    n = len(adj)
    sides = all_min_sides(adj, u, v)
    assert sides
    sset = [frozenset(a) for a in sides]
    # L1
    others = [x for x in range(n) if x not in (u, v)]
    for r in range(1 << len(others)):
        A = {u} | {others[i] for i in range(len(others)) if r >> i & 1}
        closed = all(y in A for x in A for y in out[x])
        assert closed == (len(delta(adj, A)) == 2), "L1"
    # L2
    for j in range(L.t):
        assert frozenset(L.side(j)) in sset, "L2 A_j"
    for c in L.comps:
        cs = set(c)
        assert all(connected(adj, c[0], y, allowed=cs) for y in c), "L2 connected"
        for a in sides:
            assert cs <= a or not (cs & a), "L2 split"
    # L3
    F = set()
    for a in sides:
        for e in delta(adj, a):
            F.add(ek(*e))
    pieces = []
    seen = set()
    for x in range(n):
        if x in seen:
            continue
        dist, _ = bfs(adj, x, frozenset(F))
        pieces.append(frozenset(dist))
        seen |= set(dist)
    assert set(pieces) == {frozenset(c) for c in L.comps}, "L3 pieces"
    for j in range(L.t + 1):
        X = set(L.comps[j])
        ent = [e for e in F if (e[0] in X) != (e[1] in X)]
        # edges of F entering X: tail outside; use the side A_{j-1}
        art = (u in X) or (v in X) or len(L.enter[j]) == 2
        assert art == L.is_square(j), "L3 square"
    st['squares'] += len(L.squares())
    st['layers'] += L.t + 1
    # L4
    for j in L.squares():
        for x, _ in L.entries(j):
            for y, _ in L.exits(j):
                if x != y:
                    assert flow(adj, x, y, 3)[0] >= 3, "L4"
                    st['L4'] += 1
    # L5
    du, _ = bfs(adj, u)
    d = du[v]
    cnt = 0
    for R in simple_paths(adj, u, v, n):
        cnt += 1
        if cnt > 400:
            break
        rem = frozenset(path_edges(R))
        conn = connected(adj, u, v, rem)
        crit = True
        for j in L.squares():
            al, be = alpha_beta(L, R, j)
            if not connected(adj, al, be, rem, set(L.comps[j])):
                crit = False
        assert conn == crit, ("L5", R)
        st['L5'] += 1
    # L6
    dv, _ = bfs(adj, v)
    found = False
    for j in L.squares():
        X = set(L.comps[j])
        Xadj = [adj[i] & X if i in X else set() for i in range(n)]
        for (x, al) in L.entries(j):
            for (y, be) in L.exits(j):
                for p in simple_paths(Xadj, x, y, len(X)) if x != y else [[x]]:
                    if du[x] + len(p) - 1 + dv[y] != d:
                        continue
                    if not connected(adj, al, be, frozenset(path_edges(p)), X):
                        found = True
    cp = brute_cp(adj, u, v)
    assert found == (cp == d), ("L6", found, cp, d)
    st['L6_yes' if found else 'L6_no'] += 1
    st['n'] += 1


def main():
    seed = int(sys.argv[1])
    count = int(sys.argv[2])
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    while st['n'] < count:
        s = sample_instance(rng, nmax=10)
        if s is None:
            continue
        g, adj, u, v = s
        if len(adj) > 13:
            continue
        try:
            check(adj, u, v, rng, st)
        except AssertionError as e:
            print("FAILURE", e)
            print(json.dumps(dict(n=len(adj), edges=edges_of(adj), u=u, v=v)))
            raise
        if st['n'] % 1000 == 0:
            print(st['n'], "done", round(time.time() - t0), "s", flush=True)
    print(json.dumps(dict(sorted(st.items()))))
    print("seconds", round(time.time() - t0))


if __name__ == '__main__':
    main()
