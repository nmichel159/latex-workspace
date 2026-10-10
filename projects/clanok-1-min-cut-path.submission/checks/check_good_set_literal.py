"""Independent check of the lemma on good sets (draft section, Lemma lem:good-set).

Written from the text of the draft alone, with the literal definitions:

  G'      every edge e of G subdivided by a vertex z_e
  D       any vertex set of G' with u, v in D and z_e in D for every edge e of an
          inclusion-minimal u-v cut with at most b edges   (properties (a) and (c) of the lemma;
          (c) holds for every D that contains u and v)
  G_D     torso(G', D)
  omega   minimum number of vertices z_e among the internal vertices of an a-a' path of G' whose
          internal vertices lie outside D
  G_D^+   every torso edge with omega >= 1 replaced by a path with min(omega, b+1) new vertices
  good M  M subset of B | Y;  (i) M & B separates u from v in G_D^+;
          (ii) some u-v path of G_D^+ has all its vertices of B | Y in M

Claim: cp(u,v) <= b  iff  a good set with at most b vertices exists.

Good sets are enumerated as subsets (no reformulation). cp is computed from Definition 2.1.
Also checked: the contraction lemma, and property (c) (separation in the torso = separation in G').
"""

import itertools
import random
import sys


def comp_reach(adj, start, banned):
    seen = {start}
    stack = [start]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen and y not in banned:
                seen.add(y)
                stack.append(y)
    return seen


def edge_connected(n, edges, keep, a, b):
    adj = {x: [] for x in range(n)}
    for j in keep:
        x, y = edges[j]
        adj[x].append(y)
        adj[y].append(x)
    return b in comp_reach(adj, a, set())


def cp_bruteforce(n, edges, u, v):
    m = len(edges)
    allj = set(range(m))
    for size in range(1, m + 1):
        for S in itertools.combinations(range(m), size):
            S = set(S)
            if edge_connected(n, edges, S, u, v) and not edge_connected(n, edges, allj - S, u, v):
                return size
    return None


def is_cut(n, edges, F, u, v):
    return not edge_connected(n, edges, set(range(len(edges))) - set(F), u, v)


def minimal_cuts_upto(n, edges, u, v, b):
    """All inclusion-minimal u-v cuts with at most b edges, by plain enumeration of edge subsets."""
    m = len(edges)
    result = []
    for size in range(1, min(b, m) + 1):
        for F in itertools.combinations(range(m), size):
            if is_cut(n, edges, F, u, v) and all(
                not is_cut(n, edges, [x for x in F if x != j], u, v) for j in F
            ):
                result.append(frozenset(F))
    return result


def d_outside(n, edges, C, u, v):
    """min |P \\ C| over u-v paths P: 0/1 shortest path (Bellman-Ford style relaxation)."""
    dist = {x: 10**9 for x in range(n)}
    dist[u] = 0
    changed = True
    while changed:
        changed = False
        for j, (x, y) in enumerate(edges):
            w = 0 if j in C else 1
            if dist[x] + w < dist[y]:
                dist[y] = dist[x] + w
                changed = True
            if dist[y] + w < dist[x]:
                dist[x] = dist[y] + w
                changed = True
    return dist[v]


def build_subdivision(n, edges):
    adj = {("v", x): set() for x in range(n)}
    for j, (x, y) in enumerate(edges):
        z = ("z", j)
        adj[z] = {("v", x), ("v", y)}
        adj[("v", x)].add(z)
        adj[("v", y)].add(z)
    return adj


def torso_and_omega(adj, D):
    """For a, a' in D: omega[a, a'] defined iff aa' is a torso edge."""
    omega = {}
    Dl = sorted(D)
    for a, a2 in itertools.combinations(Dl, 2):
        best = None
        if a2 in adj[a]:
            best = 0
        # vertex-weighted shortest path through vertices outside D (Bellman-Ford style)
        dist = {}
        for w in adj[a]:
            if w not in D:
                dist[w] = 1 if w[0] == "z" else 0
        changed = True
        while changed:
            changed = False
            for x in list(dist):
                for y in adj[x]:
                    if y in D:
                        continue
                    c = dist[x] + (1 if y[0] == "z" else 0)
                    if c < dist.get(y, 10**9):
                        dist[y] = c
                        changed = True
        for x, c in dist.items():
            if a2 in adj[x]:
                if best is None or c < best:
                    best = c
        if best is not None:
            omega[(a, a2)] = best
    return omega


def build_plus(D, omega, b):
    adj = {a: set() for a in D}
    Y = set()
    for (a, a2), w in omega.items():
        if w == 0:
            adj[a].add(a2)
            adj[a2].add(a)
        else:
            prev = a
            for i in range(min(w, b + 1)):
                y = ("y", a, a2, i)
                Y.add(y)
                adj[y] = set()
                adj[prev].add(y)
                adj[y].add(prev)
                prev = y
            adj[prev].add(a2)
            adj[a2].add(prev)
    return adj, Y


def exists_good_set(plus, B, Y, s, t, b):
    """Literal enumeration of M subset of B | Y with |M| <= b; returns the least size or None."""
    pool = sorted(B | Y)
    labelled = B | Y
    for size in range(0, min(b, len(pool)) + 1):
        for M in itertools.combinations(pool, size):
            M = set(M)
            # (i): M & B separates s from t
            if t in comp_reach(plus, s, M & B):
                continue
            # (ii): an s-t path whose labelled vertices all lie in M
            if t in comp_reach(plus, s, labelled - M):
                return size
    return None


def check_property_c(adj, D, omega, s, t, rng):
    """Property (c): N subset of D \\ {s,t} separates s, t in the torso iff in G'."""
    tadj = {a: set() for a in D}
    for (a, a2) in omega:
        tadj[a].add(a2)
        tadj[a2].add(a)
    inner = sorted(D - {s, t})
    for _ in range(6):
        N = {x for x in inner if rng.random() < 0.4}
        in_torso = t in comp_reach(tadj, s, N)
        in_graph = t in comp_reach(adj, s, N)
        if in_torso != in_graph:
            return False
    return True


def random_connected_graph(rng, n, m):
    while True:
        all_pairs = list(itertools.combinations(range(n), 2))
        edges = sorted(rng.sample(all_pairs, m))
        if all(edge_connected(n, edges, set(range(m)), 0, x) for x in range(1, n)):
            return edges


def main():
    rng = random.Random(7)
    instances = constructions = 0
    yes = no = 0
    for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 400):
        n = rng.randint(3, 7)
        m = rng.randint(n - 1, min(n * (n - 1) // 2, 10))
        edges = random_connected_graph(rng, n, m)
        u, v = rng.sample(range(n), 2)
        cp = cp_bruteforce(n, edges, u, v)
        adj = build_subdivision(n, edges)
        s, t = ("v", u), ("v", v)
        instances += 1
        for b in range(1, min(cp + 1, 6) + 1):
            cuts = minimal_cuts_upto(n, edges, u, v, b)
            if not cuts:
                continue  # c(u,v) > b: the lemma assumes c(u,v) <= b
            # contraction lemma, restricted to cuts with at most b edges
            val = min(len(C) + d_outside(n, edges, C, u, v) for C in cuts)
            if (cp <= b) != (val <= b) or (cp <= b and val != cp):
                print("FAILED contraction", edges, u, v, b, cp, val)
                sys.exit(1)
            needed = {s, t} | {("z", j) for C in cuts for j in C}
            rest = sorted(set(adj) - needed)
            choices = [set(needed)]
            for _ in range(3):
                p = rng.random()
                choices.append(needed | {x for x in rest if rng.random() < p})
            for D in choices:
                omega = torso_and_omega(adj, D)
                if not check_property_c(adj, D, omega, s, t, rng):
                    print("FAILED property (c)", edges, u, v, sorted(D))
                    sys.exit(1)
                plus, Y = build_plus(D, omega, b)
                B = {x for x in D if x[0] == "z"}
                if len(B | Y) > 26:
                    continue
                good = exists_good_set(plus, B, Y, s, t, b)
                constructions += 1
                if cp <= b:
                    yes += 1
                    if good != cp:
                        print("FAILED good set (yes-instance)", edges, u, v, b, cp, good, sorted(D))
                        sys.exit(1)
                else:
                    no += 1
                    if good is not None:
                        print("FAILED good set (no-instance)", edges, u, v, b, cp, good, sorted(D))
                        sys.exit(1)
    print(f"instances: {instances}, constructions (b, D): {constructions} (cp <= b: {yes}, cp > b: {no})")
    print("No check failed.")


if __name__ == "__main__":
    main()
