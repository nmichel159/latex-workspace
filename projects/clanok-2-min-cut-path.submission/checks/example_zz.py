#!/usr/bin/env python3
"""Brute-force check of Example ex:zz-instance (the ZZ instance of the graph G_b) and of the claim of rem:zz-no-p2.

The first part enumerates all vertex sets of G_b. The second builds G_phi of Definition def:dt-graph for a small formula, computes the
preorder from the minimum sides of the assignments (Lemma lem:dt-cuts) and tests which incomparable pairs of Q meet neither below nor above.
"""
from itertools import combinations, product

E = "ua us sb ab at tv bv av ub".split()
V = "uvabst"


def boundary(S, edges):
    return {e for e in edges if (e[0] in S) != (e[1] in S)}


def main_gb():
    others = [x for x in V if x not in "uv"]
    sides = {}
    for r in range(len(others) + 1):
        for c in combinations(others, r):
            S = frozenset("u" + "".join(c))
            sides[S] = len(boundary(S, E))
    c = min(sides.values())
    mins = sorted((sorted(S) for S, k in sides.items() if k == c), key=len)
    assert c == 3
    assert {frozenset(m) for m in mins} == {frozenset(s) for s in ("u", "us", "usb", "usba", "usbat")}
    Q = "uabv"
    leq = {(x, y): all(x in m for m in mins if y in m) for x in Q for y in Q}
    assert [x for x in "ubav"] == sorted(Q, key=lambda x: sum(leq[(y, x)] for y in Q))
    R = sorted(e for e in E if e[0] in Q and e[1] in Q)
    assert set(map(frozenset, R)) == set(map(frozenset, "ua ub ab av bv".split()))
    assert boundary(frozenset("usb"), E) == {"ua", "ab", "bv"}
    print("G_b: c = 3, minimum sides", ["".join(m) for m in mins], "chain u < b < a < v, delta(usb) = ua, ab, bv: ok")


def main_gphi():
    # phi = (x1 or not x2) and (x2): the occurrence vertices are o11 (x1, positive), o12 (x2, negative), o21 (x2, positive).
    occ = {"o11": ("x1", True, 1), "o12": ("x2", False, 1), "o21": ("x2", True, 2)}
    m, L = 2, 3
    c0 = (m + 1) + 2 * L
    N = c0 + 2
    Ku = [f"u{k}" for k in range(m + 1)] + ["w1", "w2"] + [f"fu{i}" for i in range(N - m - 3)]
    Kv = [f"v{k}" for k in range(m + 1)] + ["z1", "z2"] + [f"fv{i}" for i in range(N - m - 3)]
    adj = {x: set() for x in Ku + Kv + list(occ)}

    def add(a, b):
        adj[a].add(b)
        adj[b].add(a)

    for K in (Ku, Kv):
        for a, b in combinations(K, 2):
            add(a, b)
    for k in range(m + 1):
        add(f"u{k}", f"v{k}")
    for o, (_, pos, k) in occ.items():
        for t in ([f"v{k-1}", f"v{k}", "w1", "w2"] if pos else [f"u{k-1}", f"u{k}", "z1", "z2"]):
            add(o, t)
    add("o12", "o21")
    # By Lemma lem:dt-cuts the minimum sides are K^u plus the occurrence vertices of the true variables.
    sides = []
    for tv in product([False, True], repeat=2):
        val = dict(zip(("x1", "x2"), tv))
        sides.append(set(Ku) | {o for o, (x, _, _) in occ.items() if val[x]})
    Q = Ku + Kv + list(occ)
    leq = lambda x, y: all(x in A for A in sides if y in A)
    bad = []
    for x, y in combinations(Q, 2):
        if leq(x, y) or leq(y, x):
            continue
        low = any(leq(z, x) and leq(z, y) and not leq(x, z) and not leq(y, z) for z in adj[x] & adj[y])
        up = any(leq(x, z) and leq(y, z) and not leq(z, x) and not leq(z, y) for z in adj[x] & adj[y])
        if not (low or up):
            bad.append((x, y))
    print("G_phi: incomparable pairs without a witness:", bad)
    assert bad == [("o11", "o12")]


if __name__ == "__main__":
    main_gb()
    main_gphi()
