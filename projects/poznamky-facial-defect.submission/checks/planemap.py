"""Plane maps as rotation systems, exhaustive generation and facial-defect colorings.

A map with m edges has darts 0..2m-1; edge i has the darts 2i and 2i+1 (alpha(d) = d ^ 1).
sigma[d] is the next dart in the rotation at the origin vertex of d.
phi(d) = sigma[d ^ 1] is the next dart on the boundary walk of the face of d.
"""
from itertools import product


class PlaneMap:
    __slots__ = ("sigma", "m", "_vert", "_nv", "_faces")

    def __init__(self, sigma):
        self.sigma = list(sigma)
        self.m = len(sigma) // 2
        self._vert = None
        self._nv = None
        self._faces = None

    # ---------------------------------------------------------------- structure
    def vertices(self):
        """vert[d] = index of the origin vertex of dart d."""
        if self._vert is None:
            vert = [-1] * (2 * self.m)
            nv = 0
            for d in range(2 * self.m):
                if vert[d] < 0:
                    x = d
                    while vert[x] < 0:
                        vert[x] = nv
                        x = self.sigma[x]
                    nv += 1
            self._vert = vert
            self._nv = nv
        return self._vert

    @property
    def nv(self):
        self.vertices()
        return self._nv

    def faces(self):
        """List of boundary walks, each a list of darts."""
        if self._faces is None:
            seen = [False] * (2 * self.m)
            faces = []
            for d in range(2 * self.m):
                if not seen[d]:
                    walk = []
                    x = d
                    while not seen[x]:
                        seen[x] = True
                        walk.append(x)
                        x = self.sigma[x ^ 1]
                    faces.append(walk)
            self._faces = faces
        return self._faces

    def edges(self):
        vert = self.vertices()
        return [(vert[2 * i], vert[2 * i + 1]) for i in range(self.m)]

    def degrees(self):
        vert = self.vertices()
        deg = [0] * self.nv
        for d in range(2 * self.m):
            deg[vert[d]] += 1
        return deg

    def is_simple(self):
        seen = set()
        for (u, v) in self.edges():
            if u == v:
                return False
            key = (min(u, v), max(u, v))
            if key in seen:
                return False
            seen.add(key)
        return True

    def genus_ok(self):
        return self.nv - self.m + len(self.faces()) == 2

    # ---------------------------------------------------------------- canonical form
    def canon(self):
        """Canonical code up to orientation-preserving and -reversing isomorphism."""
        n = 2 * self.m
        sig = self.sigma
        inv = [0] * n
        for d in range(n):
            inv[sig[d]] = d
        best = None
        for s in (sig, inv):
            for root in range(n):
                label = [-1] * n
                order = [root]
                label[root] = 0
                i = 0
                code = []
                while i < len(order):
                    x = order[i]
                    i += 1
                    for y in (s[x], x ^ 1):
                        if label[y] < 0:
                            label[y] = len(order)
                            order.append(y)
                        code.append(label[y])
                if best is None or code < best:
                    best = code
        return tuple(best)

    # ---------------------------------------------------------------- extension
    def add_pendant(self, d):
        """New edge at the corner after dart d; its far end is a new vertex."""
        n = 2 * self.m
        sig = self.sigma + [0, 0]
        a, b = n, n + 1
        sig[a] = sig[d]
        sig[d] = a
        sig[b] = b
        return PlaneMap(sig)

    def add_chord(self, d1, d2):
        """New edge between the corner after d1 and the corner after d2 (same face)."""
        n = 2 * self.m
        sig = self.sigma + [0, 0]
        a, b = n, n + 1
        if d1 == d2:
            nxt = sig[d1]
            sig[d1] = a
            sig[a] = b
            sig[b] = nxt
        else:
            sig[a] = sig[d1]
            sig[d1] = a
            sig[b] = sig[d2]
            sig[d2] = b
        return PlaneMap(sig)

    def corner_face(self):
        """cf[d] = index of the face that contains the corner after dart d."""
        faces = self.faces()
        fidx = [0] * (2 * self.m)
        for i, w in enumerate(faces):
            for x in w:
                fidx[x] = i
        return [fidx[self.sigma[d]] for d in range(2 * self.m)]

    def children(self, simple=False):
        """All maps with one more edge (not reduced by isomorphism)."""
        n = 2 * self.m
        for d in range(n):
            yield self.add_pendant(d)
        cf = self.corner_face()
        vert = self.vertices()
        if simple:
            adj = set()
            for (u, v) in self.edges():
                adj.add((u, v))
                adj.add((v, u))
        for d1 in range(n):
            for d2 in range(d1, n):
                if cf[d1] != cf[d2]:
                    continue
                if simple:
                    u, v = vert[d1], vert[d2]
                    if u == v or (u, v) in adj:
                        continue
                yield self.add_chord(d1, d2)


def single_edge():
    return PlaneMap([0, 1])


def single_loop():
    return PlaneMap([1, 0])


def generate(max_m, simple=False, verbose=False):
    """levels[m] = dict canon -> PlaneMap for all connected plane maps with m edges."""
    level = {}
    for g in ([single_edge()] if simple else [single_edge(), single_loop()]):
        level[g.canon()] = g
    levels = {1: level}
    for m in range(2, max_m + 1):
        nxt = {}
        for g in level.values():
            for h in g.children(simple=simple):
                c = h.canon()
                if c not in nxt:
                    nxt[c] = h
        levels[m] = nxt
        level = nxt
        if verbose:
            print("m =", m, "maps:", len(nxt), flush=True)
    return levels


# -------------------------------------------------------------------- colorings
def edge_constraints(g, variant="P"):
    """Facial adjacency pairs and facial k-edge paths of the map.

    Returns (pairs, runs) where runs[k] is the set of tuples of k consecutive edges
    of a boundary walk, k = 2, 3, ...; pairs = runs[2].
    variant 'P': the k edges form a path (k + 1 distinct vertices);
    variant 'W': the k edges are distinct (a trail).
    """
    vert = g.vertices()
    runs = {}
    for walk in g.faces():
        L = len(walk)
        for k in (2, 3, 4):
            S = runs.setdefault(k, set())
            for i in range(L):
                ds = [walk[(i + j) % L] for j in range(k)]
                es = [d >> 1 for d in ds]
                if len(set(es)) < k:
                    continue
                if variant == "P" and k >= 3:
                    vs = [vert[d] for d in ds] + [vert[ds[-1] ^ 1]]
                    if len(set(vs)) < k + 1:
                        continue
                t = tuple(es)
                r = t[::-1]
                S.add(min(t, r))
    return runs


def vertex_constraints(g):
    """Facial vertex paths: tuples of k consecutive distinct vertices of a boundary walk."""
    vert = g.vertices()
    runs = {}
    for walk in g.faces():
        L = len(walk)
        vs_walk = [vert[d] for d in walk]
        for k in (2, 3, 4):
            S = runs.setdefault(k, set())
            for i in range(L):
                vs = [vs_walk[(i + j) % L] for j in range(k)]
                if len(set(vs)) < k:
                    continue
                t = tuple(vs)
                S.add(min(t, t[::-1]))
    return runs


def solve(nvars, forb, defects, fixed=None, count=False, limit=None):
    """Search for a coloring of variables 0..nvars-1 with colors 0..len(defects)-1.

    forb[k] = iterable of k-tuples of variables; a color with defect d must not be constant
    on any (d+1)-tuple. fixed = dict var -> color or var -> collection of allowed colors.
    Backtracking with unit propagation and smallest-domain-first branching.
    Returns a coloring (list) or None; with count=True the number of colorings (up to limit).
    """
    ncol = len(defects)
    cons = []          # (color, tuple of vars)
    for c in range(ncol):
        k = defects[c] + 1
        for t in forb.get(k, ()):
            cons.append((c, tuple(t)))
    watch = [[[] for _ in range(ncol)] for _ in range(nvars)]
    for ci, (c, t) in enumerate(cons):
        for v in t:
            watch[v][c].append(ci)
    full = (1 << ncol) - 1
    dom = [full] * nvars
    if fixed:
        for v, a in fixed.items():
            if isinstance(a, int):
                dom[v] = 1 << a
            else:
                mask = 0
                for x in a:
                    mask |= 1 << x
                dom[v] = mask
    popc = [bin(x).count("1") for x in range(full + 1)]
    single = {1 << c: c for c in range(ncol)}
    trail = []
    result = [0]
    found = [None]

    def propagate(queue):
        # queue: vars whose domain became a single color
        while queue:
            v = queue.pop()
            c = single[dom[v]]
            for ci in watch[v][c]:
                t = cons[ci][1]
                bit = 1 << c
                free = -1
                nfree = 0
                for w in t:
                    if dom[w] != bit:
                        nfree += 1
                        free = w
                        if nfree > 1:
                            break
                if nfree == 0:
                    return False
                if nfree == 1 and dom[free] & bit:
                    trail.append((free, dom[free]))
                    dom[free] &= ~bit
                    if dom[free] == 0:
                        return False
                    if dom[free] in single:
                        queue.append(free)
        return True

    def rec():
        best = -1
        bs = 99
        for v in range(nvars):
            s = popc[dom[v]]
            if 1 < s < bs:
                bs = s
                best = v
                if s == 2:
                    break
        if best < 0:
            result[0] += 1
            if found[0] is None:
                found[0] = [single[x] for x in dom]
            return (not count) or (limit is not None and result[0] >= limit)
        d0 = dom[best]
        for c in range(ncol):
            if d0 & (1 << c):
                mark = len(trail)
                trail.append((best, dom[best]))
                dom[best] = 1 << c
                if propagate([best]):
                    if rec():
                        return True
                while len(trail) > mark:
                    w, old = trail.pop()
                    dom[w] = old
        return False

    init = [v for v in range(nvars) if dom[v] in single]
    if all(dom[v] for v in range(nvars)) and propagate(init):
        rec()
    if count:
        return result[0]
    return found[0]


def edge_colorable(g, defects, variant="P", **kw):
    return solve(g.m, edge_constraints(g, variant), defects, **kw)


def vertex_colorable(g, defects, **kw):
    return solve(g.nv, vertex_constraints(g), defects, **kw)


def describe(g):
    vert = g.vertices()
    rot = {}
    for d in range(2 * g.m):
        v = vert[d]
        if v in rot:
            continue
        cyc = []
        x = d
        while True:
            cyc.append((x >> 1, vert[x ^ 1]))
            x = g.sigma[x]
            if x == d:
                break
        rot[v] = cyc
    faces = [[(d >> 1) for d in w] for w in g.faces()]
    return {"n": g.nv, "m": g.m, "edges": g.edges(), "rotation": rot, "faces(edges)": faces}
