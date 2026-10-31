"""Core routines of agent r4-switch for 2CH (+ P2).

Instance: (N, E, F, s, t) as in dc-hardness/twoch.py: nodes 0..N-1, E[w], F[w] bit masks (0 = empty side).
Side id: sid = 2*w + typ (typ 0 = E, 1 = F); partner = sid ^ 1.
A valid path: sequence of sides from a side containing s to a side containing t, consecutive sides meet, no two
sides of one switch.  The instance is a yes-instance iff a valid path exists.

Contents:
  side tables, side graph;
  exact solvers: brute force over modes (small n) and a BFS over valid paths (shortest valid paths);
  PC of the side CSP (positions x sides);
  P2 test, random P2 instances.
"""
import itertools
import random
from collections import deque

import numpy as np


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def popcount(m):
    return bin(m).count("1")


def side_mask(inst, sid):
    N, E, F, s, t = inst
    w, typ = sid >> 1, sid & 1
    return F[w] if typ else E[w]


def side_ids(inst):
    N, E, F, s, t = inst
    out = []
    for w in range(len(E)):
        if E[w]:
            out.append(2 * w)
        if F[w]:
            out.append(2 * w + 1)
    return out


def side_graph(inst):
    """adj[sid] = set of sids meeting sid (sid itself excluded)."""
    S = side_ids(inst)
    m = {i: side_mask(inst, i) for i in S}
    adj = {i: set() for i in S}
    for a in range(len(S)):
        for b in range(a + 1, len(S)):
            if m[S[a]] & m[S[b]]:
                adj[S[a]].add(S[b])
                adj[S[b]].add(S[a])
    return adj


def p2_ok(inst):
    N, E, F, s, t = inst
    n = len(E)
    return all((E[i] & E[l]) or (F[i] & F[l]) for i in range(n) for l in range(i + 1, n))


def p2_violations(inst):
    N, E, F, s, t = inst
    n = len(E)
    return [(i, l) for i in range(n) for l in range(i + 1, n) if not ((E[i] & E[l]) or (F[i] & F[l]))]


def connected(N, hyper, s, t):
    if s == t:
        return True
    comp = 1 << s
    rest = [h for h in hyper if h]
    changed = True
    while changed:
        changed = False
        keep = []
        for h in rest:
            if h & comp:
                comp |= h
                changed = True
            else:
                keep.append(h)
        rest = keep
        if (comp >> t) & 1:
            return True
    return bool((comp >> t) & 1)


def brute(inst):
    """Mode vector (bit w = 1: F-mode) connecting s and t, or None."""
    N, E, F, s, t = inst
    n = len(E)
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            return mask
    return None


def all_solutions(inst):
    N, E, F, s, t = inst
    n = len(E)
    out = []
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            out.append(mask)
    return out


def shortest_valid_paths(inst, limit=None, maxlen=None):
    """BFS over valid paths (states: current side, set of used sides).  Returns (length, list of paths) with all
    shortest valid paths (side-id tuples), or (None, []) if there is none.  Exponential in the worst case."""
    N, E, F, s, t = inst
    adj = side_graph(inst)
    S = list(adj)
    m = {i: side_mask(inst, i) for i in S}
    layer = {}
    for i in S:
        if (m[i] >> s) & 1:
            layer[(i, frozenset([i]))] = [(i,)]
    length = 1
    while layer:
        found = []
        for (cur, used), paths in layer.items():
            if (m[cur] >> t) & 1:
                found.extend(paths)
        if found:
            return length, found
        if maxlen is not None and length >= maxlen:
            return None, []
        nxt = {}
        for (cur, used), paths in layer.items():
            for j in adj[cur]:
                if j in used or (j ^ 1) in used:
                    continue
                # shortest paths are induced: skip j adjacent to an earlier side other than cur
                key = (j, used | {j})
                lst = nxt.setdefault(key, [])
                for p in paths:
                    if limit is None or len(lst) < limit:
                        if all(not (m[x] & m[j]) for x in p[:-1]):
                            lst.append(p + (j,))
        nxt = {k: v for k, v in nxt.items() if v}
        layer = nxt
        length += 1
    return None, []


def exact(inst):
    """Exact answer by BFS over valid induced paths (no limit on n, exponential in the worst case)."""
    N, E, F, s, t = inst
    if s == t:
        return True
    adj = side_graph(inst)
    m = {i: side_mask(inst, i) for i in adj}
    # DFS with a visited set of (cur, used) states
    seen = set()
    stack = []
    for i in adj:
        if (m[i] >> s) & 1:
            st = (i, frozenset([i]))
            seen.add(st)
            stack.append(st)
    while stack:
        cur, used = stack.pop()
        if (m[cur] >> t) & 1:
            return True
        for j in adj[cur]:
            if j in used or (j ^ 1) in used:
                continue
            st = (j, used | {j})
            if st not in seen:
                seen.add(st)
                stack.append(st)
    return False


def is_valid_walk(inst, walk):
    N, E, F, s, t = inst
    if not walk:
        return False
    used = set(walk)
    if any((i ^ 1) in used for i in used):
        return False
    m = [side_mask(inst, i) for i in walk]
    if not ((m[0] >> s) & 1 and (m[-1] >> t) & 1):
        return False
    return all(m[a] & m[a + 1] or walk[a] == walk[a + 1] for a in range(len(walk) - 1))


# ------------------------------------------------------------------------------------------------ PC (side CSP)

def pc_side(inst, L=None, return_R=False, max_sweeps=100000):
    """Strong path consistency of the side CSP: positions 0..L-1, values = non-empty sides; consecutive positions
    hold equal or meeting sides that are not partners; any two positions hold non-partner sides; position 0 contains
    s, position L-1 contains t.  Walks may repeat sides, so for L >= number of switches the CSP is exact.
    Returns True iff the PC closure is non-empty (PC does not refute)."""
    N, E, F, s, t = inst
    if s == t:
        return True
    S = side_ids(inst)
    D = len(S)
    if D == 0:
        return False
    if L is None:
        L = max(1, len(set(i >> 1 for i in S)))
    idx = {sid: k for k, sid in enumerate(S)}
    m = [side_mask(inst, i) for i in S]
    adjm = np.zeros((D, D), dtype=bool)
    nonp = np.ones((D, D), dtype=bool)
    for a in range(D):
        for b in range(D):
            if S[a] ^ 1 == S[b]:
                nonp[a, b] = False
            if a == b or (m[a] & m[b]):
                adjm[a, b] = True
    cons = adjm & nonp
    dom = np.ones((L, D), dtype=bool)
    for a in range(D):
        if not (m[a] >> s) & 1:
            dom[0, a] = False
        if not (m[a] >> t) & 1:
            dom[L - 1, a] = False
    if L == 1:
        ok = bool(dom[0].any())
        return (ok, None) if return_R else ok
    R = np.zeros((L, L, D, D), dtype=bool)
    for i in range(L):
        R[i, i] = np.diag(dom[i])
        for j in range(L):
            if i == j:
                continue
            base = cons if abs(i - j) == 1 else nonp
            R[i, j] = base & dom[i][:, None] & dom[j][None, :]
    ok = _pc_closure(R, max_sweeps)
    return (ok, R) if return_R else ok


def _pc_closure(R, max_sweeps=100000):
    L = R.shape[0]
    Rf = R.astype(np.float32)
    for sweep in range(max_sweeps):
        changed = False
        for l in range(L):
            A = Rf[:, l]
            B = Rf[l, :]
            C = np.matmul(A[:, None], B[None, :]) > 0.5
            newR = R & C
            if not np.array_equal(newR, R):
                changed = True
                R[...] = newR
                Rf = R.astype(np.float32)
                diag = R[np.arange(L), np.arange(L)]
                if not diag.any(axis=(1, 2)).all():
                    return False
        if not changed:
            break
    diag = R[np.arange(L), np.arange(L)]
    if not diag.any(axis=(1, 2)).all():
        return False
    return bool(R.any(axis=(2, 3)).all())


# ------------------------------------------------------------------------------------------------ generators

def random_p2_instance(rng, N, n, pe, pf, s=0, t=1):
    """Random sides, then every pair violating P2 gets a new shared node in E or in F (coin flip)."""
    E = [sum(1 << x for x in range(N) if rng.random() < pe) for _ in range(n)]
    F = [sum(1 << x for x in range(N) if rng.random() < pf) for _ in range(n)]
    NN = N
    for i in range(n):
        for l in range(i + 1, n):
            if not ((E[i] & E[l]) or (F[i] & F[l])):
                z = NN
                NN += 1
                if rng.random() < 0.5:
                    E[i] |= 1 << z
                    E[l] |= 1 << z
                else:
                    F[i] |= 1 << z
                    F[l] |= 1 << z
    return (NN, E, F, s, t)


def p2_repair_existing(rng, inst, p_new=0.3):
    """Repair P2 by adding, for each violating pair, either an existing node to both E-sides / both F-sides
    or a new node (probability p_new)."""
    N, E, F, s, t = inst
    E, F = list(E), list(F)
    n = len(E)
    NN = N
    pairs = [(i, l) for i in range(n) for l in range(i + 1, n)]
    rng.shuffle(pairs)
    for i, l in pairs:
        if (E[i] & E[l]) or (F[i] & F[l]):
            continue
        typ = rng.random() < 0.5
        if rng.random() < p_new:
            z = NN
            NN += 1
        else:
            z = rng.randrange(NN)
        if typ:
            E[i] |= 1 << z
            E[l] |= 1 << z
        else:
            F[i] |= 1 << z
            F[l] |= 1 << z
    return (NN, E, F, s, t)


def fmt(inst):
    N, E, F, s, t = inst
    return "N=%d s=%d t=%d " % (N, s, t) + " ".join(
        "[%d: E=%s F=%s]" % (i, bits(E[i]), bits(F[i])) for i in range(len(E)))
