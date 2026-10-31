"""Own ZZ toolkit of agent verify-round3, written from the definitions of theory-dc.md (problem ZZ, P2) and
dc-algorithm.md (path-position CSP, AC, PC, Theorem F). No import of other agents' code.

ZZ instance: Inst(q, le, R, u, v)
  q   number of elements 0..q-1
  le  q x q numpy bool matrix, le[x, y] = (x <= y); a preorder (reflexive, transitive)
  R   list of real edges (a, b) with a < b strictly (oriented low -> high)
  u   least element, v greatest element
A zigzag is a u-v path of (Q, R), alternating up/down, starting up at u (valleys at even positions);
it is consistent if no valley is >= a peak. ZZ: does a consistent zigzag exist?
Equivalent form used here: a down-set D (u in D, v not in D) such that u, v are connected in the graph G_D of
the R-edges with exactly one end in D (= low end in D, high end outside).
"""
import itertools
import random
from collections import deque

import numpy as np


class Inst:
    def __init__(self, q, le, R, u, v, names=None):
        self.q = q
        self.le = np.array(le, dtype=bool)
        self.R = [tuple(e) for e in R]
        self.u = u
        self.v = v
        self.names = names if names is not None else [str(i) for i in range(q)]
        self._adj = None

    # ------------------------------------------------------------------ basic relations
    def lt(self, x, y):
        return self.le[x, y] and not self.le[y, x]

    def eq(self, x, y):
        return self.le[x, y] and self.le[y, x]

    def comparable(self, x, y):
        return self.le[x, y] or self.le[y, x]

    def adj(self):
        if self._adj is None:
            a = [set() for _ in range(self.q)]
            for (x, y) in self.R:
                a[x].add(y)
                a[y].add(x)
            self._adj = a
        return self._adj

    def check(self):
        """Raise AssertionError unless the instance satisfies the ZZ axioms."""
        q, le = self.q, self.le
        assert le.shape == (q, q)
        assert all(le[x, x] for x in range(q)), "not reflexive"
        li = le.astype(np.int64)
        comp = (li @ li) > 0
        assert not np.any(comp & ~le), "not transitive"
        assert all(le[self.u, x] for x in range(q)), "u not least"
        assert all(le[x, self.v] for x in range(q)), "v not greatest"
        seen = set()
        for (a, b) in self.R:
            assert self.lt(a, b), "R edge not strictly increasing: %r" % ((a, b),)
            assert frozenset((a, b)) not in seen, "duplicate R edge"
            seen.add(frozenset((a, b)))
        assert frozenset((self.u, self.v)) not in seen, "uv in R"
        return True

    def middle(self, x):
        return not self.eq(x, self.u) and not self.eq(x, self.v)

    # ------------------------------------------------------------------ P2 and witnesses
    def incomparable_pairs(self):
        q = self.q
        return [(x, y) for x in range(q) for y in range(x + 1, q) if not self.comparable(x, y)]

    def p2_witnesses(self, x, y):
        """Common R-neighbours of x and y strictly above both or strictly below both."""
        A = self.adj()
        out = []
        for w in A[x] & A[y]:
            if (self.lt(w, x) and self.lt(w, y)) or (self.lt(x, w) and self.lt(y, w)):
                out.append(w)
        return out

    def p2(self):
        return all(self.p2_witnesses(x, y) for (x, y) in self.incomparable_pairs())

    def bottom_witness_ok(self):
        A = self.adj()
        for (x, y) in self.incomparable_pairs():
            if not any(self.eq(w, self.u) for w in A[x] & A[y]):
                return False
        return True

    def top_witness_ok(self):
        A = self.adj()
        for (x, y) in self.incomparable_pairs():
            if not any(self.eq(w, self.v) for w in A[x] & A[y]):
                return False
        return True

    # ------------------------------------------------------------------ down-sets and G_D
    def downsets(self):
        """All down-sets D (as frozensets) with u in D and v not in D."""
        q, le = self.q, self.le
        # linear extension: sort by number of elements below (strictly smaller elements have fewer)
        order = sorted(range(q), key=lambda x: (int(le[:, x].sum()), x))
        out = []
        dec = {}

        def rec(i):
            if i == q:
                out.append(frozenset(x for x in dec if dec[x]))
                return
            x = order[i]
            forced_in = any(dec[y] and le[x, y] for y in dec)
            forced_out = any((not dec[y]) and le[y, x] for y in dec)
            assert not (forced_in and forced_out)
            if x == self.u:
                opts = [True]
            elif x == self.v:
                opts = [False]
            else:
                opts = [True, False]
            if forced_in:
                opts = [o for o in opts if o]
            if forced_out:
                opts = [o for o in opts if not o]
            for o in opts:
                dec[x] = o
                rec(i + 1)
                del dec[x]

        rec(0)
        return out

    def is_downset(self, D):
        for y in D:
            for x in range(self.q):
                if self.le[x, y] and x not in D:
                    return False
        return True

    def gd_connected(self, D):
        """u-v connectivity in G_D (R-edges with low end in D, high end outside)."""
        if self.u not in D or self.v in D:
            return False
        nb = [[] for _ in range(self.q)]
        for (a, b) in self.R:
            if a in D and b not in D:
                nb[a].append(b)
                nb[b].append(a)
        seen = {self.u}
        dq = deque([self.u])
        while dq:
            x = dq.popleft()
            if x == self.v:
                return True
            for y in nb[x]:
                if y not in seen:
                    seen.add(y)
                    dq.append(y)
        return False

    def gd_shortest_dist(self, D):
        if self.u not in D or self.v in D:
            return None
        nb = [[] for _ in range(self.q)]
        for (a, b) in self.R:
            if a in D and b not in D:
                nb[a].append(b)
                nb[b].append(a)
        dist = {self.u: 0}
        dq = deque([self.u])
        while dq:
            x = dq.popleft()
            for y in nb[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    dq.append(y)
        return dist, nb

    def solve_downsets(self):
        """Exact ZZ answer by enumerating all down-sets; returns (answer, witness down-set or None, #down-sets)."""
        ds = self.downsets()
        for D in ds:
            if self.gd_connected(D):
                return True, D, len(ds)
        return False, None, len(ds)

    def solve_dfs(self):
        """Exact ZZ answer by DFS over simple alternating paths with the consistency test; returns a zigzag or None."""
        le, A = self.le, self.adj()
        u, v = self.u, self.v
        path = [u]
        onpath = {u}
        valleys = [u]
        peaks = []

        def rec():
            x = path[-1]
            up = (len(path) % 2 == 1)  # next vertex at odd position = peak
            for y in A[x]:
                if y in onpath:
                    continue
                if up:
                    if not self.lt(x, y):
                        continue
                    if any(le[y, a] for a in valleys):  # some valley >= y
                        continue
                    if y == v:
                        path.append(y)
                        return True
                    path.append(y); onpath.add(y); peaks.append(y)
                    if rec():
                        return True
                    path.pop(); onpath.discard(y); peaks.pop()
                else:
                    if not self.lt(y, x):
                        continue
                    if y == v:
                        continue
                    if any(le[p, y] for p in peaks):  # y >= some peak
                        continue
                    path.append(y); onpath.add(y); valleys.append(y)
                    if rec():
                        return True
                    path.pop(); onpath.discard(y); valleys.pop()
            return False

        if rec():
            return list(path)
        return None

    def is_consistent_zigzag(self, P):
        if not P or P[0] != self.u or P[-1] != self.v or len(set(P)) != len(P) or len(P) % 2 != 0:
            return False
        A = self.adj()
        for i in range(len(P) - 1):
            if P[i + 1] not in A[P[i]]:
                return False
            if i % 2 == 0 and not self.lt(P[i], P[i + 1]):
                return False
            if i % 2 == 1 and not self.lt(P[i + 1], P[i]):
                return False
        val = P[0::2]
        pk = P[1::2]
        return not any(self.le[p, a] for a in val for p in pk)

    # ------------------------------------------------------------------ Theorem F algorithm (own implementation)
    def up_mask(self, x):
        return self.le[x, :]

    def thmF(self, dual=False, maxA=2):
        """Theorem F (iii): try every set A of at most maxA elements.
        bottom version: D_A = Q - up(A + {v}); dual: D_A = down(A + {u}).  Returns (answer, A, D_A)."""
        q = self.q
        for k in range(maxA + 1):
            for A in itertools.combinations(range(q), k):
                if not dual:
                    gen = list(A) + [self.v]
                    up = np.zeros(q, dtype=bool)
                    for a in gen:
                        up |= self.le[a, :]
                    D = frozenset(int(x) for x in np.nonzero(~up)[0])
                else:
                    gen = list(A) + [self.u]
                    dn = np.zeros(q, dtype=bool)
                    for a in gen:
                        dn |= self.le[:, a]
                    D = frozenset(int(x) for x in np.nonzero(dn)[0])
                if self.gd_connected(D):
                    return True, A, D
        return False, None, None

    # ------------------------------------------------------------------ path-position CSP, AC and PC
    def csp(self, L):
        """Domains (list of oriented edges), unary masks per position, base binary constraint matrices.
        Positions 0..L-1 here (position j here = position j+1 of dc-algorithm.md)."""
        E = list(self.R)
        m = len(E)
        le = self.le
        tails = np.array([e[0] for e in E], dtype=np.int64)
        heads = np.array([e[1] for e in E], dtype=np.int64)
        # compat[e, f] = not h_e <= t_f and not h_f <= t_e
        hle = le[np.ix_(heads, tails)]          # hle[e, f] = h_e <= t_f
        compat = ~hle & ~hle.T
        samehead = heads[:, None] == heads[None, :]
        sametail = tails[:, None] == tails[None, :]
        unary = np.ones((L, m), dtype=bool)
        unary[0] &= (tails == self.u)
        unary[L - 1] &= (heads == self.v)
        base = {}
        for i in range(L):
            for j in range(i + 1, L):
                M = compat.copy()
                if j == i + 1:
                    # dc-algorithm positions are 1-based: position i+1 odd <=> i even -> same head
                    M &= samehead if i % 2 == 0 else sametail
                M &= unary[i][:, None] & unary[j][None, :]
                base[(i, j)] = M
        return E, unary, base

    def ac(self, L):
        """Arc consistency on the base constraints; returns True if every domain stays non-empty."""
        E, unary, base = self.csp(L)
        dom = [unary[i].copy() for i in range(L)]
        changed = True
        while changed:
            changed = False
            for (i, j), M in base.items():
                Mi = M & dom[i][:, None] & dom[j][None, :]
                ni = Mi.any(axis=1) & dom[i]
                nj = Mi.any(axis=0) & dom[j]
                if (ni != dom[i]).any():
                    dom[i] = ni; changed = True
                if (nj != dom[j]).any():
                    dom[j] = nj; changed = True
                if not dom[i].any() or not dom[j].any():
                    return False, dom
        return all(d.any() for d in dom), dom

    def pc(self, L, return_net=False):
        """Strong path consistency: relations T[i, j] for all ordered pairs including i = j (diagonal = domain);
        greatest fixpoint of T[i, j] &= AND_k (T[i, k] o T[k, j]). Returns True if every relation stays non-empty."""
        E, unary, base = self.csp(L)
        m = len(E)
        T = np.zeros((L, L, m, m), dtype=bool)
        for i in range(L):
            T[i, i] = np.diag(unary[i])
        for (i, j), M in base.items():
            T[i, j] = M
            T[j, i] = M.T
        while True:
            Tf = T.astype(np.float32)
            newT = T.copy()
            for k in range(L):
                # T[i, j] &= T[i, k] o T[k, j]   (for every k, including k = i and k = j)
                prod = np.matmul(Tf[:, k][:, None, :, :], Tf[k, :][None, :, :, :]) > 0.5
                newT &= prod
            if not newT.any(axis=(2, 3)).all():
                if return_net:
                    return False, newT, E
                return False
            if (newT == T).all():
                if return_net:
                    return True, newT, E
                return True
            T = newT


# ---------------------------------------------------------------------- generators

def preorder_from_relations(q, rel, classes=None):
    """Transitive closure of reflexive relation rel (list of (x, y) meaning x <= y)."""
    le = np.eye(q, dtype=bool)
    for (x, y) in rel:
        le[x, y] = True
    if classes:
        for cl in classes:
            for x in cl:
                for y in cl:
                    le[x, y] = True
    # Warshall
    for k in range(q):
        le |= le[:, k][:, None] & le[k, :][None, :]
    return le


def random_instance(rng, nb=None, nm=None, nt=None, p_rel=0.25, p_edge=0.35, p2='repair', witness=None,
                    p_eqmid=0.0):
    """Random ZZ instance: nb elements equivalent to u (u = 0), nm middle elements, nt elements equivalent to v.
    p_rel: probability of a relation x < y between middle elements (random DAG by index order), p_eqmid: ties.
    p2: 'repair' adds common neighbours until P2 holds; witness in (None, 'bottom', 'top', 'mixed')."""
    nb = nb if nb is not None else rng.randint(1, 3)
    nm = nm if nm is not None else rng.randint(2, 8)
    nt = nt if nt is not None else rng.randint(1, 3)
    q = nb + nm + nt
    B = list(range(nb))
    M = list(range(nb, nb + nm))
    T = list(range(nb + nm, q))
    u, v = 0, q - 1
    rel = []
    for b in B:
        for x in M + T:
            rel.append((b, x))
    for x in M:
        for t in T:
            rel.append((x, t))
    for i, x in enumerate(M):
        for y in M[i + 1:]:
            if rng.random() < p_rel:
                rel.append((x, y))
    classes = [B, T]
    for i, x in enumerate(M):
        for y in M[i + 1:]:
            if rng.random() < p_eqmid:
                classes.append([x, y])
    le = preorder_from_relations(q, rel, classes)
    inst = Inst(q, le, [], u, v)
    strict = [(a, b) for a in range(q) for b in range(q) if inst.lt(a, b) and {a, b} != {u, v}]
    R = set()
    for (a, b) in strict:
        if rng.random() < p_edge * (1.0 if (a in M or b in M) else 0.5):
            R.add((a, b))
    inst = Inst(q, le, sorted(R), u, v)
    if witness in ('bottom', 'top', 'mixed'):
        for (x, y) in inst.incomparable_pairs():
            mode = witness if witness != 'mixed' else rng.choice(['bottom', 'top', 'mid'])
            if mode == 'bottom':
                w = rng.choice(B)
                R.add((w, x)); R.add((w, y))
            elif mode == 'top':
                w = rng.choice(T)
                R.add((x, w)); R.add((y, w))
            else:
                pass
        inst = Inst(q, le, sorted(R), u, v)
    if p2 == 'repair':
        for (x, y) in inst.incomparable_pairs():
            if not inst.p2_witnesses(x, y):
                below = [w for w in range(q) if inst.lt(w, x) and inst.lt(w, y)]
                above = [w for w in range(q) if inst.lt(x, w) and inst.lt(y, w)]
                cands = [(w, 'b') for w in below] + [(w, 'a') for w in above]
                w, s = rng.choice(cands)
                if s == 'b':
                    R.add((w, x)); R.add((w, y))
                else:
                    R.add((x, w)); R.add((y, w))
                inst = Inst(q, le, sorted(R), u, v)
    R.discard((u, v))
    return Inst(q, le, sorted(R), u, v)
