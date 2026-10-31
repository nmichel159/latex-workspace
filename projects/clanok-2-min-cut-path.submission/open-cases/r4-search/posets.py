"""Unlabeled posets on m elements (m <= 8) up to isomorphism, by adding a new maximal element above a down-set of each
poset on m - 1 elements; duplicates removed with an invariant hash and networkx isomorphism tests.
A poset is a tuple of m bit masks: below[j] = set of elements strictly below j (transitively closed).
Known counts (OEIS A000112): 1, 1, 2, 5, 16, 63, 318, 2045, 16999 for m = 0..8.
Usage: python posets.py M   (prints the counts up to M; caches posets-M.json in runs/)"""
import os
import sys
import json
import itertools
import networkx as nx
from common import HERE


def downsets_of(m, below):
    """all down-sets (bit masks) of the poset."""
    out = []
    for mask in range(1 << m):
        ok = True
        x = mask
        while x:
            low = x & -x
            j = low.bit_length() - 1
            x ^= low
            if below[j] & ~mask:
                ok = False
                break
        if ok:
            out.append(mask)
    return out


def to_graph(m, below):
    G = nx.DiGraph()
    G.add_nodes_from(range(m))
    for j in range(m):
        for i in range(m):
            if (below[j] >> i) & 1:
                G.add_edge(i, j)
    return G


def invariant(m, below):
    above = [0] * m
    for j in range(m):
        for i in range(m):
            if (below[j] >> i) & 1:
                above[i] |= 1 << j
    sig = sorted((bin(below[j]).count("1"), bin(above[j]).count("1"),
                  tuple(sorted(bin(below[i]).count("1") for i in range(m) if (below[j] >> i) & 1)),
                  tuple(sorted(bin(above[i]).count("1") for i in range(m) if (above[j] >> i) & 1)))
                 for j in range(m))
    return tuple(sig)


def posets(M):
    cache = os.path.join(HERE, "runs", "posets-%d.json" % M)
    if os.path.exists(cache):
        with open(cache) as f:
            return [tuple(p) for p in json.load(f)]
    level = [()]
    for m in range(1, M + 1):
        buckets = {}
        new = []
        for P in level:
            for S in downsets_of(m - 1, P):
                Q = tuple(P) + (S,)
                inv = invariant(m, Q)
                G = to_graph(m, Q)
                lst = buckets.setdefault(inv, [])
                if any(nx.is_isomorphic(G, H) for H in lst):
                    continue
                lst.append(G)
                new.append(Q)
        level = new
    with open(cache, "w") as f:
        json.dump([list(p) for p in level], f)
    return level


if __name__ == "__main__":
    M = int(sys.argv[1])
    for m in range(M + 1):
        print(m, len(posets(m)), flush=True)
