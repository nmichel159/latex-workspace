"""Theorem A of dc-algorithm.md (FPT in c), own implementation from the text (agent verify-round3).

Graph: n vertices 0..n-1, edge list (parallel edges allowed), terminals u != v. Steps:
 1. unit-capacity max flow on the undirected graph (own BFS augmenting paths, net flow per edge in {-1, 0, 1});
 2. decomposition into c simple directed u-v paths (chains), flow cycles cancelled; the flow is rebuilt from the chains;
 3. residual digraph of the rebuilt flow; C(x) = Reach(u) | Reach(x) if v is not in it (smallest minimum side with x);
 4. cuttable positions; for every sequence of distinct chains (depth-first, arc consistency on every prefix), the CSP
    of Theorem A (Good between all pairs, same head / same tail between consecutive, tail u first, head v last);
    by Lemma A4 the largest remaining values form a solution (checked every time).
Reference: brute force over all vertex sets A (u in A, v not in A, |delta(A)| = c), u-v connectivity in delta(A).
Also checked on every instance: Lemma A1 (every minimum cut meets every chain in a prefix and in one edge),
Lemma A2 (Good_ab closed under componentwise max and min), Lemma A3 (same head / same tail strictly increasing),
and the Helly property behind the correctness step (the solution's edges lie in the cut of the union of C(tails)).
"""
import itertools
import random
import sys
import time
from collections import deque, defaultdict


def max_flow(n, edges, u, v):
    f = [0] * len(edges)
    inc = defaultdict(list)
    for e, (a, b) in enumerate(edges):
        inc[a].append(e)
        inc[b].append(e)
    val = 0
    while True:
        prev = {u: None}
        dq = deque([u])
        while dq and v not in prev:
            x = dq.popleft()
            for e in inc[x]:
                a, b = edges[e]
                if a == b:
                    continue
                y = b if x == a else a
                # residual from x to y: orientation a->b positive
                r = (1 - f[e]) if x == a else (1 + f[e])
                if r > 0 and y not in prev:
                    prev[y] = (x, e)
                    dq.append(y)
        if v not in prev:
            return val, f
        y = v
        while prev[y] is not None:
            x, e = prev[y]
            a, b = edges[e]
            f[e] += 1 if x == a else -1
            y = x
        val += 1


def chains_from_flow(n, edges, f, u, v):
    out = defaultdict(list)
    for e, (a, b) in enumerate(edges):
        if f[e] == 1:
            out[a].append((e, b))
        elif f[e] == -1:
            out[b].append((e, a))
    paths = []
    while out[u]:
        pv, pe = [u], []
        pos = {u: 0}
        x = u
        while x != v:
            e, y = out[x].pop()
            if y in pos:
                k = pos[y]
                for z in pv[k + 1:]:
                    del pos[z]
                pv = pv[:k + 1]
                pe = pe[:k]
                x = y
                continue
            pv.append(y)
            pe.append(e)
            pos[y] = len(pv) - 1
            x = y
        paths.append((pv, pe))
    g = [0] * len(edges)
    for pv, pe in paths:
        for i, e in enumerate(pe):
            a, b = edges[e]
            g[e] += 1 if pv[i] == a else -1
    return paths, g


def residual_reach(n, edges, g, src):
    inc = defaultdict(list)
    for e, (a, b) in enumerate(edges):
        inc[a].append(e)
        inc[b].append(e)
    seen = {src}
    dq = deque([src])
    while dq:
        x = dq.popleft()
        for e in inc[x]:
            a, b = edges[e]
            if a == b:
                continue
            y = b if x == a else a
            r = (1 - g[e]) if x == a else (1 + g[e])
            if r > 0 and y not in seen:
                seen.add(y)
                dq.append(y)
    return seen


def cut_value(edges, A):
    return sum(1 for (a, b) in edges if (a in A) != (b in A))


def brute_pimc(n, edges, u, v, c):
    others = [x for x in range(n) if x not in (u, v)]
    cuts = []
    found = False
    for k in range(len(others) + 1):
        for S in itertools.combinations(others, k):
            A = set(S) | {u}
            if cut_value(edges, A) != c:
                continue
            cuts.append(frozenset(A))
            adj = defaultdict(set)
            for (a, b) in edges:
                if (a in A) != (b in A):
                    adj[a].add(b)
                    adj[b].add(a)
            seen = {u}
            dq = deque([u])
            while dq:
                x = dq.popleft()
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        dq.append(y)
            if v in seen:
                found = True
    return found, cuts


class ThmA:
    def __init__(self, n, edges, u, v):
        self.n, self.edges, self.u, self.v = n, edges, u, v
        self.c, f = max_flow(n, edges, u, v)
        self.paths, self.g = chains_from_flow(n, edges, f, u, v)
        assert len(self.paths) == self.c
        ru = residual_reach(n, edges, self.g, u)
        assert v not in ru
        self.C = {}
        for x in range(n):
            S = ru | residual_reach(n, edges, self.g, x)
            if v not in S:
                self.C[x] = frozenset(S)
        # chains as vertex lists; cuttable positions
        self.ch = [pv for pv, pe in self.paths]
        self.cut_pos = []
        for pv in self.ch:
            ps = []
            for s in range(len(pv) - 1):
                if pv[s] in self.C and pv[s + 1] not in self.C[pv[s]]:
                    ps.append(s)
            self.cut_pos.append(ps)
        self.nodes = 0

    def good(self, a, s, b, t):
        pa, pb = self.ch[a], self.ch[b]
        return pa[s + 1] not in self.C[pb[t]] and pb[t + 1] not in self.C[pa[s]]

    def rel(self, j, a, s, b, t):
        """Binary constraint between position j (chain a, pos s) and position j+1 (chain b, pos t); j 1-based."""
        pa, pb = self.ch[a], self.ch[b]
        if j % 2 == 1:
            return pa[s + 1] == pb[t + 1]
        return pa[s] == pb[t]

    def ac(self, seq, final):
        L = len(seq)
        dom = []
        for j, a in enumerate(seq):
            d = list(self.cut_pos[a])
            if j == 0:
                d = [s for s in d if self.ch[a][s] == self.u]
            if final and j == L - 1:
                d = [s for s in d if self.ch[a][s + 1] == self.v]
            dom.append(d)
        if any(not d for d in dom):
            return None

        def ok(i, si, j, sj):
            a, b = seq[i], seq[j]
            if not self.good(a, si, b, sj):
                return False
            if j == i + 1 and not self.rel(i + 1, a, si, b, sj):
                return False
            if i == j + 1 and not self.rel(j + 1, b, sj, a, si):
                return False
            return True

        changed = True
        while changed:
            changed = False
            for i in range(L):
                for j in range(L):
                    if i == j:
                        continue
                    nd = [si for si in dom[i] if any(ok(i, si, j, sj) for sj in dom[j])]
                    if len(nd) != len(dom[i]):
                        dom[i] = nd
                        changed = True
                    if not nd:
                        return None
        return dom, ok

    def solve(self):
        """Returns (answer, list of (chain, position) or None, lemmaA4_ok)."""
        k = self.c
        a4 = [True]

        def rec(seq):
            self.nodes += 1
            r = self.ac(seq, final=False)
            if r is None:
                return None
            if len(seq) % 2 == 1:
                rf = self.ac(seq, final=True)
                if rf is not None:
                    dom, ok = rf
                    sol = [max(d) for d in dom]
                    L = len(seq)
                    if not all(ok(i, sol[i], j, sol[j]) for i in range(L) for j in range(L) if i != j):
                        a4[0] = False
                    return list(zip(seq, sol))
            for b in range(k):
                if b in seq:
                    continue
                res = rec(seq + [b])
                if res is not None:
                    return res
            return None

        for a in range(k):
            res = rec([a])
            if res is not None:
                return True, res, a4[0]
        return False, None, a4[0]

    # ----------------------------------------------------------------- lemma checks
    def check_lemmas(self, cuts):
        bad = []
        # A1: every minimum side meets every chain in a prefix and in exactly one cut edge
        for A in cuts:
            for pv in self.ch:
                inA = [x in A for x in pv]
                k = inA.index(False)
                if any(inA[k:]) or not all(inA[:k]):
                    bad.append("A1 prefix")
            nc = cut_value(self.edges, A)
            flow_cut = sum(1 for pv in self.ch for s in range(len(pv) - 1) if (pv[s] in A) and (pv[s + 1] not in A))
            if flow_cut != nc:
                bad.append("A1 edge count")
        # closures = smallest minimum sides
        for x, Cx in self.C.items():
            cand = [A for A in cuts if x in A]
            if not cand or min(cand, key=len) != Cx or any(not Cx <= A for A in cand):
                bad.append("closure")
        for x in range(self.n):
            if x not in self.C and any(x in A for A in cuts):
                bad.append("closure missing")
        # A2, A3
        k = self.c
        for a in range(k):
            for b in range(k):
                if a == b:
                    continue
                P = [(s, t) for s in self.cut_pos[a] for t in self.cut_pos[b]]
                G = set((s, t) for (s, t) in P if self.good(a, s, b, t))
                # Good = "in a common minimum cut" (Helly pairwise form) by brute force
                for (s, t) in P:
                    e1 = (self.ch[a][s], self.ch[a][s + 1]); e2 = (self.ch[b][t], self.ch[b][t + 1])
                    common = any(e1[0] in A and e1[1] not in A and e2[0] in A and e2[1] not in A for A in cuts)
                    if common != ((s, t) in G):
                        bad.append("A2 characterisation")
                for x in G:
                    for y in G:
                        if (max(x[0], y[0]), max(x[1], y[1])) not in G or (min(x[0], y[0]), min(x[1], y[1])) not in G:
                            bad.append("A2 closure")
                for kind in ("head", "tail"):
                    if kind == "head":
                        Rl = sorted((s, t) for (s, t) in P if self.ch[a][s + 1] == self.ch[b][t + 1])
                    else:
                        Rl = sorted((s, t) for (s, t) in P if self.ch[a][s] == self.ch[b][t])
                    for i in range(len(Rl) - 1):
                        if not (Rl[i][0] < Rl[i + 1][0] and Rl[i][1] < Rl[i + 1][1]):
                            bad.append("A3 " + kind)
        return bad

    def check_witness(self, sol, cuts):
        """The solution's edges lie in one minimum cut (union of C(tails)) and form a u-v walk."""
        tails = [self.ch[a][s] for a, s in sol]
        heads = [self.ch[a][s + 1] for a, s in sol]
        A = set()
        for t in tails:
            A |= self.C[t]
        if any(h in A for h in heads) or cut_value(self.edges, A) != self.c:
            return False
        walk = [tails[0]]
        for j in range(len(sol)):
            walk.append(heads[j] if j % 2 == 0 else tails[j])
        # walk: t1 h1 t2 h3 t4 ... ; check consecutive equalities
        for j in range(len(sol) - 1):
            if (j + 1) % 2 == 1 and heads[j] != heads[j + 1]:
                return False
            if (j + 1) % 2 == 0 and tails[j] != tails[j + 1]:
                return False
        return tails[0] == self.u and heads[-1] == self.v


def rand_graph(rng, n, p, multi=False):
    while True:
        edges = []
        for a in range(n):
            for b in range(a + 1, n):
                if rng.random() < p:
                    edges.append((a, b))
                    if multi and rng.random() < 0.25:
                        edges.append((a, b))
        # connected?
        adj = defaultdict(set)
        for a, b in edges:
            adj[a].add(b); adj[b].add(a)
        seen = {0}
        dq = deque([0])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); dq.append(y)
        if len(seen) == n:
            return edges


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "yes": 0, "mismatch": 0, "lemma_bad": 0, "a4_bad": 0, "witness_bad": 0, "maxnodes": 0,
          "maxc": 0, "multi": 0, "len": {}}
    t0 = time.time()
    for it in range(count):
        n = rng.randint(4, 12)
        multi = rng.random() < 0.3
        edges = rand_graph(rng, n, rng.choice([0.3, 0.45, 0.6, 0.8]), multi)
        u, v = rng.sample(range(n), 2)
        T = ThmA(n, edges, u, v)
        ans_b, cuts = brute_pimc(n, edges, u, v, T.c)
        ans, sol, a4 = T.solve()
        st["inst"] += 1; st["yes"] += ans_b; st["multi"] += multi
        st["maxnodes"] = max(st["maxnodes"], T.nodes); st["maxc"] = max(st["maxc"], T.c)
        if ans != ans_b:
            st["mismatch"] += 1
            print("MISMATCH", n, edges, u, v, ans, ans_b, flush=True)
        if not a4:
            st["a4_bad"] += 1
        if ans and not T.check_witness(sol, cuts):
            st["witness_bad"] += 1
            print("WITNESS", n, edges, u, v, sol, flush=True)
        if ans:
            st["len"][len(sol)] = st["len"].get(len(sol), 0) + 1
        bad = T.check_lemmas(cuts)
        if bad:
            st["lemma_bad"] += 1
            print("LEMMA", set(bad), n, edges, u, v, flush=True)
    print(st, "(%.0fs)" % (time.time() - t0))
    print("violations:", st["mismatch"] + st["lemma_bad"] + st["a4_bad"] + st["witness_bad"])
