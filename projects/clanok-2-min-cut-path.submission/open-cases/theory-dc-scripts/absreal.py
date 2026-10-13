"""Realisation lemma: a finite poset P with minimum u and maximum v and a set R of strictly comparable pairs
('real edges') becomes a Pi-like weighted graph: weight 1 on every comparable pair (a real edge if the pair is in
R, an ear otherwise), plus an ear u-a and an ear b-v for every comparable pair a < b with a != u, b != v.
Then every cut has value sum_{a<b} 1 + 2 * #{a<b : a outside A, b inside A}, the minimum cuts are exactly the
down-sets, and the distance condition holds iff every incomparable pair has a common R-neighbour.

abs_answer(order, R, u, v): exists a zigzag path (valleys in a down-set, peaks outside) -- by brute force over
down-sets; realise() returns a pi.Inst for cross-checks."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def closure(n, less):
    """transitive closure of the strict relation less (set of (a, b) meaning a < b)."""
    lt = [[False] * n for _ in range(n)]
    for a, b in less:
        lt[a][b] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                for j in range(n):
                    if lt[k][j]:
                        lt[i][j] = True
    for i in range(n):
        assert not lt[i][i], "cycle"
    return lt

def realise(n, lt, R, u, v):
    W = [[0] * n for _ in range(n)]
    Rset = {(min(a, b), max(a, b)) for a, b in R}
    for a in range(n):
        for b in range(n):
            if lt[a][b]:
                W[a][b] += 1; W[b][a] += 1
                if a != u:
                    W[u][a] += 1; W[a][u] += 1
                if b != v:
                    W[b][v] += 1; W[v][b] += 1
    return pi.Inst(n, sorted(Rset), W, u, v)

def p2_ok(n, lt, R):
    adj = [set() for _ in range(n)]
    for a, b in R:
        adj[a].add(b); adj[b].add(a)
    bad = []
    for x in range(n):
        for y in range(x + 1, n):
            if lt[x][y] or lt[y][x]:
                continue
            if not any((lt[w][x] and lt[w][y]) or (lt[x][w] and lt[y][w]) for w in adj[x] & adj[y]):
                bad.append((x, y))
    return bad

def downsets(n, lt, u, v):
    # all down-sets containing u, not v (brute force for small n)
    others = [x for x in range(n) if x not in (u, v)]
    res = []
    for mask in range(1 << len(others)):
        A = {u} | {others[i] for i in range(len(others)) if (mask >> i) & 1}
        if all((b not in A) or all(a in A for a in range(n) if lt[a][b]) for b in A):
            res.append(A)
    return res
