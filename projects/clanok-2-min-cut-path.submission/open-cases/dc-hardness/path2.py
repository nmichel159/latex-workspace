"""PATH-2: the switch model SW+P2 as a graph problem.

Instance: graph on vertices s=0, t=1, E_i = 2+2i, F_i = 3+2i (i < k).  P2: for i != j, E_iE_j or F_iF_j is an edge.
Question: is there an s-t path that contains at most one of E_i, F_i for every i?
Equivalence with 2CH+P2: vertices = sets, edges = intersecting pairs (s, t joined to the sets containing them);
conversely every edge of PATH-2 becomes a node shared by its two ends.

Routines: valid_path_exists (DFS over simple paths with the pair constraint), relaxed (plain BFS), random instances,
and a search for small 'gap' instances (relaxed yes, valid no), minimised by deleting edges and switches.
Usage: python path2.py SEED COUNT"""
import sys
import random
from collections import deque


def E(i):
    return 2 + 2 * i


def F(i):
    return 3 + 2 * i


def sw(x):
    return (x - 2) // 2


def p2_ok(k, adj):
    return all((E(j) in adj[E(i)]) or (F(j) in adj[F(i)]) for i in range(k) for j in range(i + 1, k))


def relaxed(k, adj):
    n = 2 + 2 * k
    seen = {0}
    dq = deque([0])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                dq.append(y)
    return 1 in seen


def valid_path_exists(k, adj, limit=10 ** 7):
    """DFS over simple paths from s; a vertex E_i/F_i may be entered only if its partner is not on the path."""
    used = set([0])
    cnt = [0]

    def partner(x):
        return x + 1 if x % 2 == 0 else x - 1

    def dfs(x):
        cnt[0] += 1
        if cnt[0] > limit:
            raise RuntimeError("limit")
        if x == 1:
            return True
        for y in adj[x]:
            if y in used:
                continue
            if y >= 2 and partner(y) in used:
                continue
            used.add(y)
            if dfs(y):
                return True
            used.discard(y)
        return False

    return dfs(0)


def make_adj(k, edges):
    adj = {x: set() for x in range(2 + 2 * k)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def random_instance(rng, k, p):
    n = 2 + 2 * k
    edges = set()
    for a in range(n):
        for b in range(a + 1, n):
            if a >= 2 and b == a + 1 and a % 2 == 0:
                continue  # no edge E_i F_i
            if (a, b) == (0, 1):
                continue
            if rng.random() < p:
                edges.add((a, b))
    for i in range(k):
        for j in range(i + 1, k):
            if (E(i), E(j)) not in edges and (F(i), F(j)) not in edges:
                edges.add((E(i), E(j)) if rng.random() < 0.5 else (F(i), F(j)))
    return edges


def is_gap(k, edges):
    adj = make_adj(k, edges)
    return p2_ok(k, adj) and relaxed(k, adj) and not valid_path_exists(k, adj)


def minimise(k, edges):
    """Delete edges (keeping P2 and the gap) and then whole switches, greedily."""
    edges = set(edges)
    changed = True
    while changed:
        changed = False
        for e in sorted(edges):
            cand = edges - {e}
            if is_gap(k, cand):
                edges = cand
                changed = True
        # delete a switch i: relabel
        for i in range(k):
            def relabel(x):
                if x < 2:
                    return x
                j = sw(x)
                if j == i:
                    return None
                return x if j < i else x - 2
            cand = set()
            okk = True
            for a, b in edges:
                ra, rb = relabel(a), relabel(b)
                if ra is None or rb is None:
                    continue
                cand.add((min(ra, rb), max(ra, rb)))
            if k - 1 >= 1 and is_gap(k - 1, cand):
                k, edges = k - 1, cand
                changed = True
                break
    return k, edges


def name(x):
    if x == 0:
        return "s"
    if x == 1:
        return "t"
    return ("E%d" if x % 2 == 0 else "F%d") % sw(x)


def fmt(k, edges):
    return "k=%d edges: %s" % (k, " ".join("%s-%s" % (name(a), name(b)) for a, b in sorted(edges)))


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    best = {}
    ngap = 0
    for it in range(count):
        k = rng.randint(2, 7)
        edges = random_instance(rng, k, rng.uniform(0.08, 0.3))
        if is_gap(k, edges):
            ngap += 1
            k2, e2 = minimise(k, edges)
            key = (k2, len(e2))
            if key not in best:
                best[key] = fmt(k2, e2)
    print("gap instances:", ngap)
    for key in sorted(best)[:15]:
        print(key, best[key])
