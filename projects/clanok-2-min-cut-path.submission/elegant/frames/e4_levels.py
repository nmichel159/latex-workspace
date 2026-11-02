"""Experiment E4: branching depth with propagation (singleton consistency hierarchy).

Node (Lf, Uf).  Propagation: state graph with low states outside Uf, high states outside Lf; dead if u, v are not connected; every cut state between (u, low) and (v, high)
is on every walk, so it is forced: (x, low) gives Lf |= dn x, (x, high) gives Uf |= up x; repeat.  Acceptance: a shortest walk is valid, or D = Lf, or D = Q - Uf connects u and v
(checked directly, so a YES is sound).  Level k: for a pivot z try both sides at level k - 1; a refuted side gives an inference; both refuted gives NO; YES ends.

Usage: imported, or e4_levels.py SEED COUNT KMAX LOG
"""
import random
import sys
import time
from collections import Counter

from common import BASES, Inst, StateGraph, WData, bits, conflicts, popcnt


def cut_states(I, LOK, HOK):
    """Cut states separating (u, low) and (v, high) in the undirected state graph, by DFS lowpoints.  State index: 2x low, 2x + 1 high.
    Returns None if u and v are not connected."""
    s = 2 * I.u
    t = 2 * I.v + 1
    if not (LOK >> I.u & 1 and HOK >> I.v & 1):
        return None
    index = {s: 0}
    low = {s: 0}
    parent = {s: None}
    order = [s]
    counter = 1
    stack = [(s, None)]
    # iterative DFS with explicit neighbour lists

    def nbrs(st):
        x = st >> 1
        if st & 1:
            return [2 * y for y in bits(I.LO[x] & LOK)]
        return [2 * y + 1 for y in bits(I.HI[x] & HOK)]

    it = {s: iter(nbrs(s))}
    st = [s]
    while st:
        a = st[-1]
        for b in it[a]:
            if b not in index:
                index[b] = counter
                low[b] = counter
                counter += 1
                parent[b] = a
                it[b] = iter(nbrs(b))
                st.append(b)
                break
            elif b != parent[a]:
                low[a] = min(low[a], index[b])
        else:
            st.pop()
            p = parent[a]
            if p is not None:
                low[p] = min(low[p], low[a])
    if t not in index:
        return None
    # walk up the DFS tree from t: a tree vertex a != s on the tree path is a cut state iff the child c on the path has low[c] >= index[a]
    cuts = []
    c = t
    a = parent[t]
    while a is not None and a != s:
        if low[c] >= index[a]:
            cuts.append(a)
        c = a
        a = parent[a]
    return cuts


def propagate(I, Lf, Uf):
    while True:
        if Lf & Uf:
            return None
        LOK = I.ALL & ~Uf
        HOK = I.ALL & ~Lf
        cuts = cut_states(I, LOK, HOK)
        if cuts is None:
            return None
        nL, nU = Lf, Uf
        for stt in cuts:
            x = stt >> 1
            if stt & 1:
                nU |= I.UP[x]
            else:
                nL |= I.DN[x]
        if nL == Lf and nU == Uf:
            return Lf, Uf
        Lf, Uf = nL, nU


def accept(I, Lf, Uf):
    G = StateGraph(I, I.ALL & ~Uf, I.ALL & ~Lf)
    W = G.shortest()
    if W is None:
        return False
    if not conflicts(I, W):
        return True
    if I.connected_in_GD(Lf):
        return True
    if I.connected_in_GD(I.ALL & ~Uf):
        return True
    return False


class Stats:
    def __init__(self):
        self.calls = 0


def solve(I, Lf, Uf, k, stats, deadline=None):
    """Returns 'Y', 'N' or '?' ."""
    stats.calls += 1
    if deadline and time.time() > deadline:
        raise TimeoutError
    p = propagate(I, Lf, Uf)
    if p is None:
        return "N"
    Lf, Uf = p
    if accept(I, Lf, Uf):
        return "Y"
    if k == 0:
        return "?"
    changed = True
    while changed:
        changed = False
        G = StateGraph(I, I.ALL & ~Uf, I.ALL & ~Lf)
        aL, aH = G.alive()
        cand = aL & aH & ~Lf & ~Uf
        for z in bits(cand):
            if Lf >> z & 1 or Uf >> z & 1:
                continue
            r1 = solve(I, Lf | I.DN[z], Uf, k - 1, stats, deadline)
            if r1 == "Y":
                return "Y"
            r2 = solve(I, Lf, Uf | I.UP[z], k - 1, stats, deadline)
            if r2 == "Y":
                return "Y"
            if r1 == "N" and r2 == "N":
                return "N"
            if r1 == "N":
                Uf |= I.UP[z]
                changed = True
            elif r2 == "N":
                Lf |= I.DN[z]
                changed = True
            if changed:
                p = propagate(I, Lf, Uf)
                if p is None:
                    return "N"
                Lf, Uf = p
                if accept(I, Lf, Uf):
                    return "Y"
                break
    return "?"


def level(I, kmax, deadline=None):
    for k in range(kmax + 1):
        stats = Stats()
        r = solve(I, I.DN[I.u], I.UP[I.v], k, stats, deadline)
        if r != "?":
            return r, k, stats.calls
    return "?", kmax, stats.calls


def strip_edge(I, a, b):
    return Inst(I.m, list(I.UP), set(I.edges) - {(a, b)}, I.u, I.v, I.names)


def main():
    seed, count, kmax, logf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    fams = ["small", "B", "A", "stair", "ties", "mix", "cross", "allstrict", "kappa", "two"]
    with open(logf, "w", encoding="utf-8") as f:
        print("fam m q kind | result level calls seconds", file=f)
        for fam in fams:
            for _ in range(count):
                d = BASES[fam](rng)
                I, P = d.build()
                W = WData(I, P)
                P = W.P
                t0 = time.time()
                try:
                    r, k, c = level(I, kmax, time.time() + 120)
                except TimeoutError:
                    r, k, c = "timeout", -1, -1
                print(fam, I.m, len(P) - 1, "planted", "|", r, k, c, round(time.time() - t0, 1), file=f, flush=True)
                i = rng.randrange(len(P) // 4, 3 * len(P) // 4)
                a, b = (P[i], P[i + 1]) if i % 2 == 0 else (P[i + 1], P[i])
                J = strip_edge(I, a, b)
                t0 = time.time()
                try:
                    r, k, c = level(J, kmax, time.time() + 120)
                except TimeoutError:
                    r, k, c = "timeout", -1, -1
                print(fam, I.m, len(P) - 1, "stripped@%d" % i, "|", r, k, c, round(time.time() - t0, 1), file=f, flush=True)


if __name__ == "__main__":
    main()
