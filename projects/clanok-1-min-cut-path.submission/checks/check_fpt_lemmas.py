"""Brute-force checks of the draft section "Approximation and Parameterized Complexity".

  Contraction lemma   cp(u,v) = min |C| + d_C(u,v) over the inclusion-minimal u-v cuts C, where
                      d_C(u,v) is the least number of edges outside C on a u-v path
  Important cuts      the same minimum taken over important cuts only can exceed cp(u,v)
                      (left graph of Example 5.3)
  Equivalence lemma   for every vertex set D of the subdivided graph G' that contains u, v and the
                      vertex x_e of every edge e of a minimal u-v cut with at most b edges:
                      cp(u,v) <= b  iff  the labelled graph H+ built from torso(G', D) has a good
                      set with at most b vertices (and the two minima agree when cp(u,v) <= b)

cp(u,v) is computed from Definition 2.1 (smallest edge set S with u, v connected in (V, S) and
disconnected in G - S). The treewidth bound on torso(G', D) is not checked: it only matters for
the running time, and the equivalence holds for every admissible D.

Graphs: all connected graphs with 2 to 6 vertices (networkx atlas); D is the smallest admissible
set, the whole vertex set, and random sets in between.

Run:  python check_fpt_lemmas.py
"""

import heapq
import itertools
import random
import sys

import networkx as nx
from networkx.generators.atlas import graph_atlas_g


class Failure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def connected(n, edges, removed, a, b):
    """Are a and b connected in the graph on 0..n-1 with the edges whose index is not in removed?"""
    adj = [[] for _ in range(n)]
    for j, (x, y) in enumerate(edges):
        if j not in removed:
            adj[x].append(y)
            adj[y].append(x)
    seen = {a}
    stack = [a]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return b in seen


def cp_definition(n, edges, u, v):
    """Definition 2.1: the smallest S with u, v connected in (V, S) and disconnected in G - S."""
    m = len(edges)
    everything = set(range(m))
    for size in range(1, m + 1):
        for S in itertools.combinations(range(m), size):
            S = set(S)
            if connected(n, edges, everything - S, u, v) and not connected(n, edges, S, u, v):
                return size
    raise Failure("no cut-path")


def boundary(edges, R):
    return frozenset(j for j, (x, y) in enumerate(edges) if (x in R) != (y in R))


def induced_connected(n, edges, R):
    R = set(R)
    if not R:
        return False
    start = next(iter(R))
    inside = [j for j, (x, y) in enumerate(edges) if x in R and y in R]
    removed = set(range(len(edges))) - set(inside)
    return all(connected(n, edges, removed, start, x) for x in R)


def minimal_cuts(n, edges, u, v):
    """Inclusion-minimal u-v cuts: boundaries of sets R with u in R, v outside, both sides connected.

    Returns a dictionary cut -> list of the sets R that define it.
    """
    others = [x for x in range(n) if x not in (u, v)]
    cuts = {}
    for size in range(len(others) + 1):
        for extra in itertools.combinations(others, size):
            R = {u, *extra}
            rest = set(range(n)) - R
            if induced_connected(n, edges, R) and induced_connected(n, edges, rest):
                cuts.setdefault(boundary(edges, R), []).append(frozenset(R))
    return cuts


def distance_outside(n, edges, C, u, v):
    """d_C(u,v): the least number of edges outside C on a u-v path (edges of C cost nothing)."""
    adj = [[] for _ in range(n)]
    for j, (x, y) in enumerate(edges):
        w = 0 if j in C else 1
        adj[x].append((y, w))
        adj[y].append((x, w))
    dist = {u: 0}
    heap = [(0, u)]
    while heap:
        d, x = heapq.heappop(heap)
        if d > dist.get(x, 10**9):
            continue
        for y, w in adj[x]:
            if d + w < dist.get(y, 10**9):
                dist[y] = d + w
                heapq.heappush(heap, (d + w, y))
    return dist[v]


def important_cuts(cuts):
    """Minimal cuts delta(R) such that no minimal cut delta(R') with R a proper subset of R' is as small."""
    result = []
    for C, sets in cuts.items():
        dominated = False
        for C2, sets2 in cuts.items():
            if C2 != C and len(C2) <= len(C) and any(R < R2 for R in sets for R2 in sets2):
                dominated = True
                break
        if not dominated:
            result.append(C)
    return result


# ----------------------------------------------------------------------------------------------
# The construction of the equivalence lemma
# ----------------------------------------------------------------------------------------------

def subdivision(n, edges):
    """G': vertex ('v', x) for every vertex x, ('e', j) for every edge j."""
    adj = {("v", x): set() for x in range(n)}
    for j, (x, y) in enumerate(edges):
        adj[("e", j)] = {("v", x), ("v", y)}
        adj[("v", x)].add(("e", j))
        adj[("v", y)].add(("e", j))
    return adj


def torso_weights(adj, D):
    """omega(a, a') for every edge of torso(G', D).

    The minimum number of vertices ('e', j) among the internal vertices of an a-a' path of G' whose
    internal vertices lie outside D; 0 for vertices adjacent in G'.
    """
    omega = {}
    for a in D:
        dist = {}
        heap = []
        counter = 0
        for w in adj[a]:
            if w in D:
                key = frozenset((a, w))
                omega[key] = 0
            else:
                d = 1 if w[0] == "e" else 0
                if d < dist.get(w, 10**9):
                    dist[w] = d
                    counter += 1
                    heapq.heappush(heap, (d, counter, w))
        while heap:
            d, _, x = heapq.heappop(heap)
            if d > dist.get(x, 10**9):
                continue
            for y in adj[x]:
                if y == a:
                    continue
                if y in D:
                    key = frozenset((a, y))
                    if d < omega.get(key, 10**9):
                        omega[key] = d
                else:
                    d2 = d + (1 if y[0] == "e" else 0)
                    if d2 < dist.get(y, 10**9):
                        dist[y] = d2
                        counter += 1
                        heapq.heappush(heap, (d2, counter, y))
    return omega


def labelled_graph(D, omega, b):
    """H+: every torso edge with omega >= 1 is replaced by a path with min(omega, b + 1) new vertices."""
    adj = {a: set() for a in D}
    Y = set()
    for key, w in omega.items():
        a, a2 = tuple(key)
        if w == 0:
            adj[a].add(a2)
            adj[a2].add(a)
            continue
        previous = a
        for i in range(min(w, b + 1)):
            z = ("y", a, a2, i)
            Y.add(z)
            adj[z] = set()
            adj[previous].add(z)
            adj[z].add(previous)
            previous = z
        adj[previous].add(a2)
        adj[a2].add(previous)
    return adj, Y


def min_good_set(adj, A, Y, s, t, b):
    """The least size of a good set with at most b vertices, or None.

    A set M of vertices of A and Y is good if M & A separates s from t and some s-t path has all its
    vertices of A and Y in M. The minimum equals min |K| + (number of vertices of (A - K) | Y on an
    s-t path) over the subsets K of A that separate s from t.
    """
    best = None
    A = sorted(A)
    for size in range(0, min(b, len(A)) + 1):
        for K in itertools.combinations(A, size):
            K = set(K)
            # separation
            seen = {s}
            stack = [s]
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if y not in seen and y not in K:
                        seen.add(y)
                        stack.append(y)
            if t in seen:
                continue
            # cheapest path
            dist = {s: 0}
            heap = [(0, 0, s)]
            counter = 0
            while heap:
                d, _, x = heapq.heappop(heap)
                if d > dist.get(x, 10**9):
                    continue
                for y in adj[x]:
                    w = 1 if (y in Y or (y[0] == "e" and y not in K)) else 0
                    if d + w < dist.get(y, 10**9):
                        dist[y] = d + w
                        counter += 1
                        heapq.heappush(heap, (d + w, counter, y))
            if t in dist:
                total = size + dist[t]
                if total <= b and (best is None or total < best):
                    best = total
    return best


def check_equivalence(n, edges, u, v, cp, cuts, rng):
    tested = 0
    adj = subdivision(n, edges)
    everything = set(adj)
    for b in range(1, cp + 2):
        needed = {("v", u), ("v", v)}
        for C in cuts:
            if len(C) <= b:
                needed |= {("e", j) for j in C}
        choices = [set(needed), set(everything)]
        for _ in range(3):
            p = rng.random()
            choices.append(needed | {x for x in everything if rng.random() < p})
        for D in choices:
            omega = torso_weights(adj, D)
            plus, Y = labelled_graph(D, omega, b)
            A = {x for x in D if x[0] == "e"}
            good = min_good_set(plus, A, Y, ("v", u), ("v", v), b)
            if cp <= b:
                require(good == cp, f"equivalence: cp={cp}, b={b}, good={good}, edges={edges}, u={u}, v={v}, D={sorted(D)}")
            else:
                require(good is None, f"equivalence: cp={cp} > b={b} but good={good}, edges={edges}, u={u}, v={v}, D={sorted(D)}")
            tested += 1
    return tested


def main():
    rng = random.Random(20261010)
    graphs = pairs = constructions = 0
    important_worse = 0
    for G in graph_atlas_g():
        n = G.number_of_nodes()
        if n < 2 or n > 6 or not nx.is_connected(G):
            continue
        edges = sorted((min(a, b), max(a, b)) for a, b in G.edges())
        graphs += 1
        for u, v in itertools.combinations(range(n), 2):
            pairs += 1
            cp = cp_definition(n, edges, u, v)
            cuts = minimal_cuts(n, edges, u, v)
            by_cut = {C: len(C) + distance_outside(n, edges, C, u, v) for C in cuts}
            require(min(by_cut.values()) == cp, f"contraction lemma: edges={edges}, u={u}, v={v}")
            if min(by_cut[C] for C in important_cuts(cuts)) > cp:
                important_worse += 1
            constructions += check_equivalence(n, edges, u, v, cp, cuts, rng)

    # left graph of Example 5.3: vertices t, a, v, u, b, s
    t, a, v, u, b, s = range(6)
    edges = sorted((min(x, y), max(x, y)) for x, y in [(t, a), (t, v), (a, u), (a, b), (v, b), (u, s), (s, b)])
    cp = cp_definition(6, edges, u, v)
    cuts = minimal_cuts(6, edges, u, v)
    important = important_cuts(cuts)
    values = sorted(len(C) + distance_outside(6, edges, C, u, v) for C in important)
    require(cp == 3, "Example 5.3 (left): cp")
    require(values and values[0] == 4, "Example 5.3 (left): important cuts")
    reverse = minimal_cuts(6, edges, v, u)
    values_reverse = sorted(len(C) + distance_outside(6, edges, C, v, u) for C in important_cuts(reverse))
    require(values_reverse[0] == 4, "Example 5.3 (left): important cuts seen from v")

    print(f"graphs: {graphs}, pairs (u, v): {pairs}, constructions (b, D): {constructions}")
    print("contraction lemma: holds on every pair")
    print("equivalence lemma: holds on every construction")
    print(f"pairs on which the important cuts alone give more than cp: {important_worse}")
    print(f"Example 5.3 (left): cp = {cp}, minimal cuts: {len(cuts)}, important cuts: {len(important)}, "
          f"best value over important cuts: {values[0]} (from u), {values_reverse[0]} (from v)")
    print("No check failed.")


if __name__ == "__main__":
    try:
        main()
    except Failure as failure:
        print("FAILED:", failure)
        sys.exit(1)
