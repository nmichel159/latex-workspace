"""Agent DC-algorithm: FPT algorithm in c = c(u,v) for PIMC ("does some minimum u-v cut contain a u-v path?").

Method (dc-algorithm.md, Theorem A).  Fix a maximum u-v flow and decompose it into c edge-disjoint simple u-v paths
pi_1..pi_c (the chains).  A minimum cut delta(A) meets every chain in exactly one edge, at the step where the chain
leaves A.  A u-v path inside delta(A) therefore uses distinct chains i_1..i_L (L odd, L <= c), one edge per chain.
For a fixed sequence (i_1..i_L) the remaining question is a binary CSP whose variable j is the position s_j of the
chosen edge on chain i_j; all its constraints are max-closed with respect to the positions, so arc consistency
followed by taking the largest value of every domain decides it (and yields a witness).  The sequences are
enumerated by depth-first search with arc-consistency pruning; worst case O(c! * e * poly(n)).

Library functions:
  chains(g, u, v)              flow, residual closures, chain decomposition
  pimc_chaincsp(g, u, v)       the algorithm; returns (yes?, witness path or None, statistics)
  pimc_brute(g, u, v)          all minimum cuts (closed sets) and a BFS inside each cut
Imports checks/mcp.py read-only.
"""
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
if CHECKS not in sys.path:
    sys.path.insert(0, CHECKS)
import mcp  # noqa: E402


# ----------------------------------------------------------------------------------------------------------
# flow, chain decomposition, residual closures
# ----------------------------------------------------------------------------------------------------------

def decompose(g, u, v, flow):
    """Edge-disjoint simple u-v paths carrying the flow after cancelling cycles.  Returns (paths, arcs used)."""
    out = [[] for _ in range(g.n)]
    for e, (a, b) in enumerate(g.edges):
        if flow[e] > 0:
            out[a].append(b)
        elif flow[e] < 0:
            out[b].append(a)
    paths = []
    while out[u]:
        walk = [u]
        pos = {u: 0}
        x = u
        while x != v:
            y = out[x].pop()
            if y in pos:                      # cycle: drop it
                k = pos[y]
                for z in walk[k + 1:]:
                    del pos[z]
                walk = walk[:k + 1]
                x = y
                continue
            pos[y] = len(walk)
            walk.append(y)
            x = y
        paths.append(walk)
    return paths


def flow_from_paths(g, paths):
    flow = [0] * g.m
    for p in paths:
        for a, b in zip(p, p[1:]):
            e = g.edge_id(a, b)
            flow[e] += 1 if a == g.edges[e][0] else -1
    return flow


def residual_closures(g, flow):
    """cl[x] = bit mask of the vertices reachable from x in the residual digraph (x included)."""
    n = g.n
    out = [0] * n
    for e, (a, b) in enumerate(g.edges):
        f = flow[e]
        if f == 0:
            out[a] |= 1 << b
            out[b] |= 1 << a
        elif f > 0:
            out[b] |= 1 << a
        else:
            out[a] |= 1 << b
    cl = [0] * n
    for s in range(n):
        seen = 1 << s
        stack = [s]
        while stack:
            x = stack.pop()
            new = out[x] & ~seen
            seen |= new
            while new:
                low = new & -new
                stack.append(low.bit_length() - 1)
                new ^= low
        cl[s] = seen
    return cl


class Chains:
    """c, the chains pi_1..pi_c, the closures, and for every chain the positions s whose edge
    pi[s] pi[s+1] lies in some minimum cut (tail pi[s], head pi[s+1])."""

    def __init__(self, g, u, v, allowed=None):
        self.g, self.u, self.v = g, u, v
        c, flow, _ = mcp.maxflow(g, u, v)
        self.c = c
        self.paths = decompose(g, u, v, flow)
        assert len(self.paths) == c
        flow = flow_from_paths(g, self.paths)
        cl = residual_closures(g, flow)
        assert not (cl[u] >> v) & 1
        base = cl[u]
        self.C = [base | cl[x] for x in range(g.n)]       # smallest closed set containing u and x
        self.cand = []
        for p in self.paths:
            pos = []
            for s in range(len(p) - 1):
                t, h = p[s], p[s + 1]
                if allowed is not None and not allowed(t, h):
                    continue
                if (self.C[t] >> h) & 1 or (self.C[t] >> v) & 1:
                    continue
                pos.append(s)
            self.cand.append(pos)

    def edge(self, a, s):
        p = self.paths[a]
        return p[s], p[s + 1]

    def compat(self, a, s, b, t):
        """edges (a,s) and (b,t) lie in a common minimum cut (D1/D2)."""
        ta, ha = self.edge(a, s)
        tb, hb = self.edge(b, t)
        return not (self.C[tb] >> ha) & 1 and not (self.C[ta] >> hb) & 1


# ----------------------------------------------------------------------------------------------------------
# the CSP for a fixed sequence of chains
# ----------------------------------------------------------------------------------------------------------

def share_ok(ch, j, a, s, b, t):
    """consecutive edges j, j+1 (j counted from 1): j odd -> same head, j even -> same tail."""
    ta, ha = ch.edge(a, s)
    tb, hb = ch.edge(b, t)
    return ha == hb if j % 2 == 1 else ta == tb


def arc_consistency(ch, seq, doms):
    """seq: chain indices; doms: list of lists of positions (modified copy returned) or None if a domain empties.
    Constraints: all pairs compatible; consecutive pairs share the right end."""
    L = len(seq)
    doms = [list(d) for d in doms]
    changed = True
    while changed:
        changed = False
        for j in range(L):
            for k in range(L):
                if j == k:
                    continue
                a, b = seq[j], seq[k]
                consec = abs(j - k) == 1
                newd = []
                for s in doms[j]:
                    ok = False
                    for t in doms[k]:
                        if not ch.compat(a, s, b, t):
                            continue
                        if consec:
                            lo = min(j, k)          # 0-based index of the first of the two edges
                            if lo == j:
                                good = share_ok(ch, lo + 1, a, s, b, t)
                            else:
                                good = share_ok(ch, lo + 1, b, t, a, s)
                            if not good:
                                continue
                        ok = True
                        break
                    if ok:
                        newd.append(s)
                if len(newd) != len(doms[j]):
                    doms[j] = newd
                    changed = True
                    if not newd:
                        return None
    return doms


def max_assignment_ok(ch, seq, doms):
    """Check the max-closure claim: the largest value of every domain is a solution."""
    L = len(seq)
    pick = [max(d) for d in doms]
    for j in range(L):
        for k in range(j + 1, L):
            if not ch.compat(seq[j], pick[j], seq[k], pick[k]):
                return False, pick
            if k == j + 1 and not share_ok(ch, j + 1, seq[j], pick[j], seq[k], pick[k]):
                return False, pick
    return True, pick


def pimc_chaincsp(g, u, v, allowed=None, check_max=True, node_limit=None):
    """Decide whether some minimum u-v cut contains a u-v path (of allowed edges).
    Returns (yes, path, stats).  stats: nodes of the sequence search, c."""
    ch = Chains(g, u, v, allowed)
    stats = {"c": ch.c, "nodes": 0, "maxfail": 0}
    if u == v:
        return False, None, stats
    # first edge: tail u, i.e. position 0 of a chain
    starts = [a for a in range(ch.c) if 0 in ch.cand[a]]
    result = [None]

    def finish(seq, doms):
        # last edge must have head v
        last = seq[-1]
        dl = [s for s in doms[-1] if ch.edge(last, s)[1] == v]
        if not dl:
            return None
        d2 = arc_consistency(ch, seq, doms[:-1] + [dl])
        return d2

    def rec(seq, doms):
        stats["nodes"] += 1
        if node_limit is not None and stats["nodes"] > node_limit:
            raise RuntimeError("node limit")
        if len(seq) % 2 == 1:
            d2 = finish(seq, doms)
            if d2 is not None:
                ok, pick = max_assignment_ok(ch, seq, d2)
                if check_max and not ok:
                    stats["maxfail"] += 1
                path = [ch.edge(seq[0], pick[0])[0]]
                for a, s in zip(seq, pick):
                    t, h = ch.edge(a, s)
                    path.append(h if path[-1] == t else t)
                result[0] = path
                return True
        j = len(seq)                  # index (0-based) of the new edge; it shares with edge j-1 (1-based j)
        a = seq[-1]
        for b in range(ch.c):
            if b in seq:
                continue
            # positions on b that share the right end with some value of the last domain
            nd = []
            for t in ch.cand[b]:
                for s in doms[-1]:
                    if share_ok(ch, j, a, s, b, t):
                        nd.append(t)
                        break
            if not nd:
                continue
            d2 = arc_consistency(ch, seq + [b], doms + [nd])
            if d2 is None:
                continue
            if rec(seq + [b], d2):
                return True
        return False

    for a in starts:
        d = arc_consistency(ch, [a], [[0]])
        if d is not None and rec([a], d):
            return True, result[0], stats
    return False, None, stats


# ----------------------------------------------------------------------------------------------------------
# brute force
# ----------------------------------------------------------------------------------------------------------

def all_min_cuts(g, u, v):
    """All u-sides A (bit masks) of minimum u-v cuts, as unions of closures (Picard-Queyranne)."""
    c, flow, _ = mcp.maxflow(g, u, v)
    cl = residual_closures(g, flow)
    base = cl[u]
    cand = [x for x in range(g.n) if not (base >> x) & 1 and not (cl[x] >> v) & 1]
    res = set()
    stack = [(0, base)]
    while stack:
        i, A = stack.pop()
        while i < len(cand) and (A >> cand[i]) & 1:
            i += 1
        if i == len(cand):
            res.add(A)
            continue
        x = cand[i]
        stack.append((i + 1, A))
        stack.append((i + 1, A | cl[x]))
    return c, sorted(res)


def path_in_cut(g, u, v, A, allowed=None):
    par = {u: None}
    dq = deque([u])
    while dq:
        x = dq.popleft()
        for y, e in g.adj[x]:
            if y in par or not (((A >> x) ^ (A >> y)) & 1):
                continue
            if allowed is not None and not allowed(x, y):
                continue
            par[y] = x
            dq.append(y)
    if v not in par:
        return None
    p = [v]
    while par[p[-1]] is not None:
        p.append(par[p[-1]])
    return p[::-1]


def pimc_brute(g, u, v, allowed=None):
    c, cuts = all_min_cuts(g, u, v)
    for A in cuts:
        p = path_in_cut(g, u, v, A, allowed)
        if p is not None:
            return True, p, len(cuts)
    return False, None, len(cuts)


def path_in_some_min_cut(g, u, v, path):
    """Independent check of a witness (Lemma 6): alternate sides, closure of the evens avoids the odds."""
    c, flow, _ = mcp.maxflow(g, u, v)
    cl = residual_closures(g, flow)
    if path[0] != u or path[-1] != v or len(path) % 2 == 1:
        return False
    for a, b in zip(path, path[1:]):
        if not g.has_edge(a, b):
            return False
    A = cl[u]
    for x in path[0::2]:
        A |= cl[x]
    return all(not (A >> y) & 1 for y in path[1::2])
