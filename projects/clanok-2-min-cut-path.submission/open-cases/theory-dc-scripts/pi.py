"""Problem Pi (theory-dc.md, Proposition 6): the open case of DC as a multigraph problem.

An instance is (q, R, W, u, v): vertex set 0..q-1, R a set of 'real' edges (simple graph), W[x][y] >= [xy in R]
the multiplicity of the pair in H (real edge plus ears).  Distance condition: every two vertices are adjacent in
R, have a common R-neighbour, or carry an ear (W > R).  Question: does some minimum u-v cut of H contain a u-v
path of R?

Exact routines: max flow, the residual preorder, all minimum cuts, the answer, and its realisation as a simple
graph (ears = vertices of degree two) for cross-checks with checks/mcp.py.
"""
import random
from collections import deque


class Inst:
    def __init__(self, q, R, W, u, v):
        self.q, self.u, self.v = q, u, v
        self.R = [[False] * q for _ in range(q)]
        for a, b in R:
            self.R[a][b] = self.R[b][a] = True
        self.W = [row[:] for row in W]
        for a in range(q):
            for b in range(q):
                if self.R[a][b] and self.W[a][b] < 1:
                    raise ValueError("real edge without weight")

    def real_edges(self):
        return [(a, b) for a in range(self.q) for b in range(a + 1, self.q) if self.R[a][b]]

    def ears(self):
        return [(a, b, self.W[a][b] - (1 if self.R[a][b] else 0)) for a in range(self.q) for b in range(a + 1, self.q)
                if self.W[a][b] - (1 if self.R[a][b] else 0) > 0]

    def dist_ok(self):
        q = self.q
        for x in range(q):
            for y in range(x + 1, q):
                if self.R[x][y] or self.W[x][y] > 0:
                    continue
                if not any(self.R[x][z] and self.R[z][y] for z in range(q)):
                    return False
        return True

    def realise(self):
        """(n, edges) of the simple graph: real edges plus one degree-two vertex per ear."""
        E = list(self.real_edges())
        n = self.q
        for a, b, k in self.ears():
            for _ in range(k):
                E.append((a, n))
                E.append((n, b))
                n += 1
        return n, E


def maxflow(W, s, t):
    """Edmonds-Karp on the symmetric capacity matrix W.  Returns (value, F) with F[x][y] the net flow x->y."""
    q = len(W)
    F = [[0] * q for _ in range(q)]
    value = 0
    while True:
        par = [-1] * q
        par[s] = s
        dq = deque([s])
        while dq and par[t] < 0:
            x = dq.popleft()
            for y in range(q):
                if par[y] < 0 and W[x][y] - F[x][y] > 0:
                    par[y] = x
                    dq.append(y)
        if par[t] < 0:
            return value, F
        y = t
        while y != s:
            x = par[y]
            F[x][y] += 1
            F[y][x] -= 1
            y = x
        value += 1


def residual_reach(W, F):
    """reach[x] = bit mask of vertices reachable from x in the residual digraph (x -> y iff W - F > 0)."""
    q = len(W)
    out = [[y for y in range(q) if W[x][y] - F[x][y] > 0] for x in range(q)]
    reach = []
    for s in range(q):
        seen = 1 << s
        dq = [s]
        for x in dq:
            for y in out[x]:
                if not (seen >> y) & 1:
                    seen |= 1 << y
                    dq.append(y)
        reach.append(seen)
    return reach


def cut_value(W, A):
    q = len(W)
    return sum(W[x][y] for x in range(q) if (A >> x) & 1 for y in range(q) if not (A >> y) & 1)


def min_cuts(inst, limit=None):
    """(c, reach, list of all minimum u-v cuts as vertex masks of the u-side)."""
    c, F = maxflow(inst.W, inst.u, inst.v)
    reach = residual_reach(inst.W, F)
    base = reach[inst.u]
    cand = [x for x in range(inst.q) if not (base >> x) & 1 and not (reach[x] >> inst.v) & 1]
    res = set()
    # closed sets = unions of closures; enumerate by include/exclude with closure on include
    stack = [(0, base)]
    while stack:
        i, A = stack.pop()
        while i < len(cand) and (A >> cand[i]) & 1:
            i += 1
        if i == len(cand):
            res.add(A)
            if limit is not None and len(res) > limit:
                raise RuntimeError("too many minimum cuts")
            continue
        x = cand[i]
        stack.append((i + 1, A))          # x stays out (may still be added later by a closure; duplicates ok)
        stack.append((i + 1, A | reach[x]))
    return c, reach, sorted(res)


def real_cut_path(inst, A):
    """Shortest u-v path using only real edges of delta(A) (vertex list) or None."""
    q = inst.q
    par = [-1] * q
    par[inst.u] = inst.u
    dq = deque([inst.u])
    while dq:
        x = dq.popleft()
        for y in range(q):
            if par[y] < 0 and inst.R[x][y] and (((A >> x) ^ (A >> y)) & 1):
                par[y] = x
                dq.append(y)
    if par[inst.v] < 0:
        return None
    path = [inst.v]
    while path[-1] != inst.u:
        path.append(par[path[-1]])
    return path[::-1]


def answer(inst, limit=None):
    """(c, yes?, witness cut, witness path, number of minimum cuts, number with a path, min length)."""
    c, reach, cuts = min_cuts(inst, limit)
    wit = None
    count = 0
    best = None
    for A in cuts:
        p = real_cut_path(inst, A)
        if p is not None:
            count += 1
            if best is None or len(p) - 1 < best:
                best = len(p) - 1
                wit = (A, p)
    return {"c": c, "yes": wit is not None, "witness": wit, "ncuts": len(cuts), "nyes": count, "minlen": best,
            "reach": reach, "cuts": cuts}


def random_instance(rng, q, p_real, p_ear, max_mult=2, force_dist=True):
    """Random Pi-instance: real edges with probability p_real; extra ears with probability p_ear each pair
    (multiplicity 1..max_mult); with force_dist an ear is added to every pair that violates the distance
    condition.  u = 0, v = 1 non-adjacent."""
    R = []
    Rm = [[False] * q for _ in range(q)]
    for a in range(q):
        for b in range(a + 1, q):
            if (a, b) == (0, 1):
                continue
            if rng.random() < p_real:
                R.append((a, b))
                Rm[a][b] = Rm[b][a] = True
    W = [[1 if Rm[a][b] else 0 for b in range(q)] for a in range(q)]
    for a in range(q):
        for b in range(a + 1, q):
            if rng.random() < p_ear:
                k = rng.randint(1, max_mult)
                W[a][b] += k
                W[b][a] += k
    if force_dist:
        for a in range(q):
            for b in range(a + 1, q):
                if not Rm[a][b] and W[a][b] == 0 and not any(Rm[a][z] and Rm[z][b] for z in range(q)):
                    W[a][b] = W[b][a] = 1
    return Inst(q, R, W, 0, 1)


def planted_instance(rng, q, k, p_in, p_cross, p_extra_ear, support_prob=1.0):
    """Pi-instance with a planted alternating path of length 2k+1 inside the cut (A, B): real edges inside the
    sides with probability p_in, extra real cross edges with probability p_cross; ears u-x (x in A) and v-y
    (y in B) of multiplicity equal to the cut degree (each with probability support_prob, otherwise one less),
    random extra ears inside the sides; finally ears for every pair violating the distance condition.
    The planted cut need not stay minimum; the answer is computed exactly afterwards."""
    u, v = 0, 1
    others = list(range(2, q))
    rng.shuffle(others)
    side = {u: 0, v: 1}
    for x in others:
        side[x] = rng.randint(0, 1)
    A = [x for x in range(q) if side[x] == 0]
    B = [x for x in range(q) if side[x] == 1]
    if len(A) < k + 1 or len(B) < k + 1:
        return None
    ev = [u] + rng.sample([x for x in A if x != u], k)
    od = rng.sample([x for x in B if x != v], k) + [v]
    path = []
    for i in range(k + 1):
        path.append(ev[i])
        path.append(od[i])
    Rm = [[False] * q for _ in range(q)]

    def addr(a, b):
        Rm[a][b] = Rm[b][a] = True

    for a, b in zip(path, path[1:]):
        addr(a, b)
    for a in range(q):
        for b in range(a + 1, q):
            if (a, b) == (u, v) or Rm[a][b]:
                continue
            if side[a] == side[b]:
                if rng.random() < p_in:
                    addr(a, b)
            elif rng.random() < p_cross:
                addr(a, b)
    W = [[1 if Rm[a][b] else 0 for b in range(q)] for a in range(q)]

    def adde(a, b, k=1):
        W[a][b] += k
        W[b][a] += k

    for x in range(q):
        if x in (u, v):
            continue
        dc = sum(1 for y in range(q) if Rm[x][y] and side[y] != side[x])
        root = u if side[x] == 0 else v
        mult = dc if rng.random() < support_prob else max(0, dc - 1)
        if mult:
            adde(x, root, mult)
    for a in range(q):
        for b in range(a + 1, q):
            if side[a] == side[b] and rng.random() < p_extra_ear:
                adde(a, b, 1)
    for a in range(q):
        for b in range(a + 1, q):
            if not Rm[a][b] and W[a][b] == 0 and not any(Rm[a][z] and Rm[z][b] for z in range(q)):
                adde(a, b, 1)
    R = [(a, b) for a in range(q) for b in range(a + 1, q) if Rm[a][b]]
    return Inst(q, R, W, u, v)
