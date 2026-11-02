"""Layer algorithm for pairs with c(u,v) = 2 (proposed replacement of Section 4), brute force, generators.

A graph is a list of sets: adj[x] = set of neighbours of x, vertices 0..n-1.
No import from checks/; everything here is independent of the article's programs.
"""
import random
from collections import deque


# ---------- basic graph functions ----------

def edges_of(adj):
    return [(x, y) for x in range(len(adj)) for y in adj[x] if x < y]


def ek(x, y):
    return (x, y) if x < y else (y, x)


def bfs(adj, s, removed=frozenset(), allowed=None):
    """Distances from s in G minus the edges in removed, inside the vertex set allowed."""
    dist = {s: 0}
    par = {s: None}
    dq = deque([s])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y in dist:
                continue
            if allowed is not None and y not in allowed:
                continue
            if ek(x, y) in removed:
                continue
            dist[y] = dist[x] + 1
            par[y] = x
            dq.append(y)
    return dist, par


def path_from_par(par, t):
    out = []
    while t is not None:
        out.append(t)
        t = par[t]
    return out[::-1]


def connected(adj, s, t, removed=frozenset(), allowed=None):
    dist, _ = bfs(adj, s, removed, allowed)
    return t in dist


def is_connected_graph(adj):
    return len(bfs(adj, 0)[0]) == len(adj)


def flow(adj, u, v, limit, rng=None, removed=frozenset()):
    """Ford-Fulkerson with unit capacities on an undirected graph, at most `limit` augmentations.

    Returns (value, H), H = dict mapping an edge key to (tail, head) for the edges carrying flow.
    """
    H = {}
    val = 0
    while val < limit:
        # search in the residual graph
        par = {u: None}
        dq = deque([u])
        while dq and v not in par:
            x = dq.popleft()
            nb = list(adj[x])
            if rng is not None:
                rng.shuffle(nb)
            for y in nb:
                if y in par or ek(x, y) in removed:
                    continue
                k = ek(x, y)
                # residual arc x->y exists unless the edge already carries flow x->y
                if k in H and H[k] == (x, y):
                    continue
                par[y] = x
                dq.append(y)
        if v not in par:
            break
        y = v
        while par[y] is not None:
            x = par[y]
            k = ek(x, y)
            if k in H:  # flow y->x is cancelled
                assert H[k] == (y, x)
                del H[k]
            else:
                H[k] = (x, y)
            y = x
        val += 1
    return val, H


def cut_value(adj, x, y, limit=10**9):
    return flow(adj, x, y, limit)[0]


# ---------- the residual digraph and its strong components ----------

def residual_out(adj, H):
    """D: both arcs for an edge outside H, only the arc head->tail for an edge of H."""
    out = [[] for _ in adj]
    for x in range(len(adj)):
        for y in adj[x]:
            k = ek(x, y)
            if k in H and H[k] == (x, y):
                continue  # edge x->y of H has only the arc y->x
            out[x].append(y)
    return out


def tarjan(out):
    """Strong components in the order of Tarjan: a component comes after all components it reaches.

    So no arc leads from an earlier to a later component, exactly the order the text asks for.
    """
    n = len(out)
    index = [None] * n
    low = [0] * n
    onstack = [False] * n
    st = []
    comps = []
    cnt = 0
    for root in range(n):
        if index[root] is not None:
            continue
        work = [(root, 0)]
        index[root] = low[root] = cnt
        cnt += 1
        st.append(root)
        onstack[root] = True
        while work:
            x, i = work[-1]
            if i < len(out[x]):
                work[-1] = (x, i + 1)
                y = out[x][i]
                if index[y] is None:
                    index[y] = low[y] = cnt
                    cnt += 1
                    st.append(y)
                    onstack[y] = True
                    work.append((y, 0))
                elif onstack[y]:
                    low[x] = min(low[x], index[y])
            else:
                work.pop()
                if work:
                    p = work[-1][0]
                    low[p] = min(low[p], low[x])
                if low[x] == index[x]:
                    c = []
                    while True:
                        z = st.pop()
                        onstack[z] = False
                        c.append(z)
                        if z == x:
                            break
                    comps.append(c)
    return comps


def random_linear_extension(comps, out, rng):
    """Another order of the components with no arc from an earlier to a later one."""
    k = len(comps)
    cid = {}
    for i, c in enumerate(comps):
        for x in c:
            cid[x] = i
    succ = [set() for _ in range(k)]  # i -> j if an arc from comp i to comp j
    for x in range(len(out)):
        for y in out[x]:
            if cid[x] != cid[y]:
                succ[cid[x]].add(cid[y])
    remaining = set(range(k))
    order = []
    placed = set()
    while remaining:
        avail = [i for i in remaining if succ[i] <= placed]
        i = rng.choice(avail)
        order.append(i)
        placed.add(i)
        remaining.discard(i)
    return [comps[i] for i in order]


def push_random_cycle(adj, H, rng):
    """Change H along a random directed cycle of D: another flow of the same value, maybe with cycles."""
    out = residual_out(adj, H)
    n = len(adj)
    start = rng.randrange(n)
    # random walk in D until a vertex repeats
    seen = {start: 0}
    walk = [start]
    x = start
    for _ in range(4 * n):
        if not out[x]:
            return H
        y = rng.choice(out[x])
        if len(walk) >= 2 and y == walk[-2]:
            # a 2-cycle on an edge outside H is not a cycle of the flow network; try another arc
            others = [z for z in out[x] if z != walk[-2]]
            if not others:
                return H
            y = rng.choice(others)
        if y in seen:
            cyc = walk[seen[y]:] + [y]
            H2 = dict(H)
            for a, b in zip(cyc, cyc[1:]):
                k = ek(a, b)
                if k in H2:
                    assert H2[k] == (b, a)
                    del H2[k]
                else:
                    H2[k] = (a, b)
            return H2
        seen[y] = len(walk)
        walk.append(y)
        x = y
    return H


def check_flow(adj, H, u, v, val):
    bal = [0] * len(adj)
    for (a, b) in H.values():
        bal[a] += 1
        bal[b] -= 1
    for x in range(len(adj)):
        want = val if x == u else (-val if x == v else 0)
        assert bal[x] == want, "unbalanced flow"


# ---------- the layer algorithm ----------

class Layers:
    """Layers X_0..X_t, heads and tails, squares."""

    def __init__(self, adj, u, v, H, comps):
        self.adj, self.u, self.v, self.H = adj, u, v, H
        self.comps = comps
        self.t = len(comps) - 1
        self.cid = {}
        for i, c in enumerate(comps):
            for x in c:
                self.cid[x] = i
        assert self.cid[u] == 0 and self.cid[v] == self.t and self.t >= 1, "u or v in a wrong layer"
        self.enter = [[] for _ in comps]
        self.leave = [[] for _ in comps]
        self.boundary = []
        for k, (a, b) in H.items():
            if self.cid[a] != self.cid[b]:
                assert self.cid[a] < self.cid[b], "an edge of H goes backwards"
                self.leave[self.cid[a]].append((a, b))
                self.enter[self.cid[b]].append((a, b))
        # every edge of G between different layers carries flow
        for x, y in edges_of(adj):
            if self.cid[x] != self.cid[y]:
                assert ek(x, y) in H
        for j in range(1, self.t):
            assert len(self.enter[j]) == len(self.leave[j]) and len(self.enter[j]) in (1, 2)
        assert len(self.enter[0]) == 0 and len(self.leave[self.t]) == 0
        assert len(self.leave[0]) == 2 and len(self.enter[self.t]) == 2

    def is_square(self, j):
        return j == 0 or j == self.t or len(self.enter[j]) == 2

    def squares(self):
        return [j for j in range(self.t + 1) if self.is_square(j)]

    def entries(self, j):
        if j == 0:
            return [(self.u, self.u)]
        a, b = [e[1] for e in self.enter[j]]
        return [(a, b), (b, a)]

    def exits(self, j):
        if j == self.t:
            return [(self.v, self.v)]
        a, b = [e[0] for e in self.leave[j]]
        return [(a, b), (b, a)]

    def side(self, j):
        """A_j as a set."""
        s = set()
        for i in range(j + 1):
            s |= set(self.comps[i])
        return s


def make_layers(adj, u, v, rng=None, shuffle_order=False, cycles=0):
    val, H = flow(adj, u, v, 3, rng)
    if val != 2:
        return val, None
    for _ in range(cycles):
        H = push_random_cycle(adj, H, rng)
    check_flow(adj, H, u, v, 2)
    out = residual_out(adj, H)
    comps = tarjan(out)
    if shuffle_order:
        comps = random_linear_extension(comps, out, rng)
    return 2, Layers(adj, u, v, H, comps)


def solve(adj, u, v, rng=None, shuffle_order=False, cycles=0, mutation=None):
    """The proposed algorithm. Returns a dict with keys:
    outcome: 'c1', 'c3', 'found', 'none', 'record'
    value, path (the cut-path as a set of edges), pair.
    """
    val, L = make_layers(adj, u, v, rng, shuffle_order, cycles)
    du, pu = bfs(adj, u)
    dv, pv = bfs(adj, v)
    d = du[v]
    if val == 1:
        return dict(outcome='c1', value=d, cutpath=path_edges(path_from_par(pu, v)))
    if val >= 3:
        return dict(outcome='c3')
    recorded = None
    tests = 0
    for j in L.squares():
        X = set(L.comps[j])
        ents = L.entries(j)
        exs = L.exits(j)
        if mutation == 'no_swap':  # deliberately wrong: only one order of the terminals
            ents, exs = ents[:1], exs[:1]
        if mutation == 'first_square' and j != L.squares()[0]:  # deliberately wrong
            continue
        for (x, al) in ents:
            for (y, be) in exs:
                if x == y or al == be:
                    continue
                l = d - du[x] - dv[y]
                if l >= 3:
                    recorded = (x, y)
                cands = []
                if l == 1 and y in adj[x]:
                    cands.append([x, y])
                elif l == 2:
                    _, par = bfs(adj, al, allowed=X)
                    q = path_from_par(par, be)
                    qe = list(zip(q, q[1:]))
                    ws = set()
                    for a, b in qe:
                        if a == x:
                            ws.add(b)
                        if b == x:
                            ws.add(a)
                        if mutation != 'x_only':  # 'x_only' is deliberately wrong
                            if a == y:
                                ws.add(b)
                            if b == y:
                                ws.add(a)
                    assert len(ws) <= 4
                    for w in ws:
                        if w in (x, y):
                            continue
                        if w in adj[x] and w in adj[y]:
                            cands.append([x, w, y])
                for p in cands:
                    tests += 1
                    rem = frozenset(ek(a, b) for a, b in zip(p, p[1:]))
                    if not connected(adj, al, be, rem, X):
                        Rx = path_from_par(pu, x)
                        Ry = path_from_par(pv, y)[::-1]
                        R = Rx + p[1:] + Ry[1:]
                        return dict(outcome='found', value=d, cutpath=path_edges(R), rpath=R,
                                    square=j, terminals=(x, al, y, be), tests=tests, trace=p)
    R = path_from_par(pu, v)
    C = {k for k, (a, b) in L.H.items() if L.cid[a] == 0 and L.cid[b] != 0}
    cp = path_edges(R) | C
    if recorded is not None:
        return dict(outcome='record', pair=recorded, cutpath=cp, value=None, tests=tests)
    return dict(outcome='none', value=d + 1, cutpath=cp, tests=tests)


def path_edges(p):
    return {ek(a, b) for a, b in zip(p, p[1:])}


# ---------- brute force, independent of everything above except flow() ----------

def simple_paths(adj, u, v, maxlen):
    """All simple u-v paths with at most maxlen edges."""
    dv, _ = bfs(adj, v)
    if u not in dv:
        return
    path = [u]
    onpath = {u}

    def rec(x):
        if x == v:
            yield list(path)
            return
        if len(path) - 1 >= maxlen:
            return
        for y in adj[x]:
            if y in onpath or y not in dv:
                continue
            if len(path) + dv[y] > maxlen:
                continue
            path.append(y)
            onpath.add(y)
            yield from rec(y)
            path.pop()
            onpath.discard(y)

    yield from rec(u)


def brute_cp(adj, u, v):
    """cp(u,v) = min over simple u-v paths P of |P| + c_{G minus P}(u,v). No lemma of the article used."""
    best = 10 ** 9
    du, _ = bfs(adj, u)
    # iterative deepening on the path length, stop when the length reaches best
    for L in range(du[v], len(adj)):
        if L >= best:
            break
        for P in simple_paths(adj, u, v, L):
            if len(P) - 1 != L:
                continue
            rem = frozenset(path_edges(P))
            if not connected(adj, u, v, rem):
                extra = 0
            else:
                extra = flow(adj, u, v, 10 ** 9, removed=rem)[0]
            best = min(best, L + extra)
            if best == du[v]:
                return best
    return best


def brute_brute_cp(adj, u, v):
    """Enumeration of all edge subsets, for very small graphs only: the definition itself."""
    E = edges_of(adj)
    m = len(E)
    best = 10 ** 9
    for mask in range(1 << m):
        k = bin(mask).count('1')
        if k >= best:
            continue
        S = [E[i] for i in range(m) if mask >> i & 1]
        inS = [set() for _ in adj]
        for a, b in S:
            inS[a].add(b)
            inS[b].add(a)
        if not connected(inS, u, v):
            continue
        if connected(adj, u, v, frozenset(S)):
            continue
        best = k
    return best


def in_dc(adj):
    n = len(adj)
    for x in range(n):
        dx, _ = bfs(adj, x)
        for y in range(x + 1, n):
            if dx[y] >= 3 and flow(adj, x, y, 3)[0] >= 3:
                return False
    return True


def check_cutpath(adj, u, v, S):
    """S contains a u-v path and a u-v cut."""
    inS = [set() for _ in adj]
    for a, b in S:
        assert b in adj[a]
        inS[a].add(b)
        inS[b].add(a)
    return connected(inS, u, v) and not connected(adj, u, v, frozenset(S))


# ---------- generators ----------

def random_connected(rng, verts, extra):
    """Edges of a random connected graph on verts with extra further edges."""
    verts = list(verts)
    rng.shuffle(verts)
    E = set()
    for i in range(1, len(verts)):
        E.add(ek(verts[i], verts[rng.randrange(i)]))
    for _ in range(extra):
        if len(verts) >= 2:
            a, b = rng.sample(verts, 2)
            E.add(ek(a, b))
    return E


def small_diameter(rng, verts, extra):
    """Connected graph with a hub: diameter at most two."""
    verts = list(verts)
    rng.shuffle(verts)
    E = set()
    for x in verts[1:]:
        E.add(ek(verts[0], x))
    for _ in range(extra):
        if len(verts) >= 2:
            a, b = rng.sample(verts, 2)
            E.add(ek(a, b))
    return E


def build(n, E):
    adj = [set() for _ in range(n)]
    for a, b in E:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def gen_sparse(rng, nmax=11):
    n = rng.randint(3, nmax)
    E = random_connected(rng, range(n), rng.randint(0, n + 2))
    return build(n, E)


def gen_chain(rng, kind=None, pend=True):
    """A chain of blocks joined by two routes, routes through links, with pendant parts and ears.

    kind 'any': blocks are random connected graphs. 'hub': blocks of diameter at most two.
    'bridge': blocks made of two parts joined by one or two edges (yes-biased).
    """
    kind = kind or rng.choice(['any', 'hub', 'bridge', 'tiny'])
    blocks = rng.randint(1, 4)
    E = set()
    nxt = 0
    blk = []

    def new(k):
        nonlocal nxt
        r = list(range(nxt, nxt + k))
        nxt += k
        return r

    for b in range(blocks):
        size = rng.randint(1, 5) if kind != 'tiny' else rng.randint(1, 3)
        vs = new(size)
        if kind == 'hub':
            E |= small_diameter(rng, vs, rng.randint(0, 2))
        elif kind == 'bridge' and size >= 2:
            cut = rng.randint(1, size - 1)
            l, r = vs[:cut], vs[cut:]
            E |= random_connected(rng, l, rng.randint(0, 2))
            E |= random_connected(rng, r, rng.randint(0, 2))
            for _ in range(rng.randint(1, 2)):
                E.add(ek(rng.choice(l), rng.choice(r)))
        else:
            E |= random_connected(rng, vs, rng.randint(0, 3))
        blk.append(vs)

    def route(a, b):
        # one route from a to b: an edge, or through links
        cur = a
        for _ in range(rng.choice([0, 0, 0, 1, 1, 2])):
            lk = new(rng.choice([1, 1, 1, 2]))
            E.update(random_connected(rng, lk, rng.randint(0, 1)))
            E.add(ek(cur, rng.choice(lk)))
            cur = rng.choice(lk)
        if cur != b:
            E.add(ek(cur, b))

    for b in range(blocks - 1):
        for _ in range(2):
            route(rng.choice(blk[b]), rng.choice(blk[b + 1]))
    u = new(1)[0]
    v = new(1)[0]
    # u and v may be joined to the first and last block by two routes
    for _ in range(2):
        route(u, rng.choice(blk[0]))
        route(rng.choice(blk[-1]), v)
    n0 = nxt
    if pend:
        # pendant trees and small pendant graphs by a bridge
        for _ in range(rng.choice([0, 0, 1, 1, 2])):
            at = rng.randrange(n0)
            vs = new(rng.randint(1, 3))
            E |= random_connected(rng, vs, rng.randint(0, 1))
            E.add(ek(at, rng.choice(vs)))
        # ears: a small graph joined by exactly two edges to two vertices
        for _ in range(rng.choice([0, 0, 1, 1])):
            a, b = rng.randrange(n0), rng.randrange(n0)
            vs = new(rng.randint(1, 2))
            E |= random_connected(rng, vs, 0)
            if a == b and len(vs) == 1:
                b = (a + 1) % n0
            E.add(ek(a, rng.choice(vs)))
            E.add(ek(b, rng.choice(vs)))
    E = {e for e in E if e[0] != e[1]}
    adj = build(nxt, E)
    return adj, u, v


SEEDS = [
    # G_a of the article
    (6, [(0, 2), (0, 4), (4, 3), (2, 3), (2, 5), (5, 1), (3, 1)], 0, 1),
    # G_a^+ of the article
    (7, [(0, 2), (0, 4), (4, 3), (2, 3), (2, 5), (5, 1), (3, 1), (6, 0), (6, 3)], 0, 1),
    # G_1 of the article: u=0, v=9, 1..8
    (10, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 6), (2, 4), (4, 5), (5, 7), (6, 7), (6, 8), (7, 9), (8, 9)], 0, 9),
    # G_1'
    (11, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 6), (2, 4), (4, 5), (5, 7), (6, 7), (6, 8), (7, 9), (8, 9), (10, 6), (10, 7)], 0, 9),
]


def gen_mutant(rng):
    """A seed graph of the article with random additions and removals."""
    n, E, u, v = rng.choice(SEEDS)
    E = set(ek(a, b) for a, b in E)
    for _ in range(rng.randint(0, 3)):
        op = rng.random()
        if op < 0.4:
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b:
                E.add(ek(a, b))
        elif op < 0.7 and E:
            E.discard(rng.choice(sorted(E)))
        elif op < 0.85:
            a = rng.randrange(n)
            E.add((a, n))
            n += 1
        else:
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b:
                E.add((a, n))
                E.add((b, n))
                n += 1
    return build(n, E), u, v


def sample_instance(rng, nmax=11, gens=('sparse', 'chain', 'mutant')):
    """A connected graph with a pair u,v with c(u,v) = 2 and at most 16 vertices; returns None if rejected."""
    g = rng.choice(gens)
    if g == 'sparse':
        adj = gen_sparse(rng, nmax)
        n = len(adj)
        u, v = rng.sample(range(n), 2)
    elif g == 'chain':
        adj, u, v = gen_chain(rng)
    else:
        adj, u, v = gen_mutant(rng)
    if len(adj) > 16 or not is_connected_graph(adj):
        return None
    if u == v or flow(adj, u, v, 3)[0] != 2:
        return None
    return g, adj, u, v
