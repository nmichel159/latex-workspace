"""2CH with classes + P2 (r5-classes.md §1), written from the definitions of the report (no import of r5-classes/).

Instance: N nodes (bit masks), terminals s != t, switches w with node masks E[w], F[w], class cls[w].
A mode vector gives every class a type (0 = E, 1 = F); every switch picks the side of the mode of its class.
Yes iff s, t connected in the hypergraph of the picked sides.
Side id: 2w = E-side, 2w + 1 = F-side; a side exists only if its mask is non-empty.
Valid path: sides X_1..X_r, s in X_1, t in X_r, consecutive sides meet, distinct switches, no two sides of switches
of one class with different types.
P2 (classes): switches of different classes have E_w & E_v != 0 or F_w & F_v != 0.
"""
import itertools
import random
from collections import deque


def bits(x):
    i = 0
    while x:
        if x & 1:
            yield i
        x >>= 1
        i += 1


class CInst:
    def __init__(self, N, E, F, cls, s, t):
        self.N, self.E, self.F, self.cls, self.s, self.t = N, list(E), list(F), list(cls), s, t
        self.m = len(E)
        self.classes = sorted(set(cls))
        self.cidx = {c: i for i, c in enumerate(self.classes)}
        self.nc = len(self.classes)
        self.members = {c: [w for w in range(self.m) if cls[w] == c] for c in self.classes}
        self.sides = [i for w in range(self.m) for i in (2 * w, 2 * w + 1) if self.mask(i)]
        self.sideset = set(self.sides)
        self.adj = {i: [] for i in self.sides}
        for a, b in itertools.combinations(self.sides, 2):
            if self.mask(a) & self.mask(b):
                self.adj[a].append(b)
                self.adj[b].append(a)

    def mask(self, i):
        return self.F[i >> 1] if i & 1 else self.E[i >> 1]

    def side_cls(self, i):
        return self.cls[i >> 1]

    def to_json(self):
        return {"N": self.N, "E": [sorted(bits(x)) for x in self.E], "F": [sorted(bits(x)) for x in self.F],
                "cls": self.cls, "s": self.s, "t": self.t}

    @staticmethod
    def from_json(d):
        E = [sum(1 << b for b in x) for x in d["E"]]
        F = [sum(1 << b for b in x) for x in d["F"]]
        return CInst(d["N"], E, F, d["cls"], d["s"], d["t"])


# ----------------------------------------------------------------------------------------------------------------
def connects(I, modes):
    """modes: dict class -> 0/1 (every class).  True iff s, t connected by the picked sides."""
    if I.s == I.t:
        return True
    picked = [I.F[w] if modes[I.cls[w]] else I.E[w] for w in range(I.m)]
    picked = [p for p in picked if p]
    C = 1 << I.s
    changed = True
    while changed:
        changed = False
        rest = []
        for p in picked:
            if p & C:
                if p & ~C:
                    C |= p
                    changed = True
            else:
                rest.append(p)
        picked = rest
        if (C >> I.t) & 1:
            return True
    return bool((C >> I.t) & 1)


def brute(I):
    sols = []
    for v in itertools.product((0, 1), repeat=I.nc):
        modes = {c: v[I.cidx[c]] for c in I.classes}
        if connects(I, modes):
            sols.append(modes)
    return sols


def p2_ok(I):
    for w, v in itertools.combinations(range(I.m), 2):
        if I.cls[w] != I.cls[v] and not (I.E[w] & I.E[v]) and not (I.F[w] & I.F[v]):
            return False
    return True


def p2_violations(I):
    return [(w, v) for w, v in itertools.combinations(range(I.m), 2)
            if I.cls[w] != I.cls[v] and not (I.E[w] & I.E[v]) and not (I.F[w] & I.F[v])]


def is_valid_path(I, P):
    if not P or not (I.mask(P[0]) >> I.s) & 1 or not (I.mask(P[-1]) >> I.t) & 1:
        return False
    for a, b in zip(P, P[1:]):
        if not (I.mask(a) & I.mask(b)):
            return False
    ws = [i >> 1 for i in P]
    if len(set(ws)) != len(ws):
        return False
    ty = {}
    for i in P:
        c = I.side_cls(i)
        if ty.setdefault(c, i & 1) != (i & 1):
            return False
    return True


def is_valid_walk(I, W):
    """sides may repeat; no two sides of one class with different types"""
    if not W or not (I.mask(W[0]) >> I.s) & 1 or not (I.mask(W[-1]) >> I.t) & 1:
        return False
    for a, b in zip(W, W[1:]):
        if a != b and not (I.mask(a) & I.mask(b)):
            return False
    ty = {}
    for i in W:
        if ty.setdefault(I.side_cls(i), i & 1) != (i & 1):
            return False
    return True


def shortest_len(I):
    """length of a shortest valid path (BFS over (side, committed E classes, committed F classes)); None if none."""
    q = deque()
    seen = set()
    for i in I.sides:
        if (I.mask(i) >> I.s) & 1:
            c = I.cidx[I.side_cls(i)]
            st = (i, (1 << c) if not (i & 1) else 0, (1 << c) if (i & 1) else 0)
            if st not in seen:
                seen.add(st)
                q.append((st, 1))
    while q:
        (i, ce, cf), d = q.popleft()
        if (I.mask(i) >> I.t) & 1:
            return d
        for j in I.adj[i]:
            c = I.cidx[I.side_cls(j)]
            if j & 1:
                if (ce >> c) & 1:
                    continue
                st = (j, ce, cf | (1 << c))
            else:
                if (cf >> c) & 1:
                    continue
                st = (j, ce | (1 << c), cf)
            if st not in seen:
                seen.add(st)
                q.append((st, d + 1))
    return None


def all_shortest(I, cap=10 ** 6):
    """all shortest valid paths (tuples of side ids)."""
    L = shortest_len(I)
    if L is None:
        return []
    # side-graph distance to a side containing t (lower bound)
    dist = {i: None for i in I.sides}
    q = deque()
    for i in I.sides:
        if (I.mask(i) >> I.t) & 1:
            dist[i] = 1
            q.append(i)
    while q:
        i = q.popleft()
        for j in I.adj[i]:
            if dist[j] is None:
                dist[j] = dist[i] + 1
                q.append(j)
    out = []

    def rec(path, usedw, ty):
        if len(out) >= cap:
            return
        i = path[-1]
        if len(path) == L:
            if (I.mask(i) >> I.t) & 1:
                out.append(tuple(path))
            return
        for j in I.adj[i]:
            if dist[j] is None or len(path) + dist[j] > L:
                continue
            w = j >> 1
            if w in usedw:
                continue
            c = I.side_cls(j)
            if c in ty and ty[c] != (j & 1):
                continue
            newc = c not in ty
            if newc:
                ty[c] = j & 1
            usedw.add(w)
            path.append(j)
            rec(path, usedw, ty)
            path.pop()
            usedw.discard(w)
            if newc:
                del ty[c]

    for i in I.sides:
        if (I.mask(i) >> I.s) & 1 and dist[i] is not None and dist[i] <= L:
            rec([i], {i >> 1}, {I.side_cls(i): i & 1})
    return out


# ----------------------------------------------------------------------------------------------------------------
# certificate framework (§2a)
def omega(I, c, tau):
    """Omega(C, tau): the non-empty tau-sides of the switches of class c"""
    return frozenset(2 * w + tau for w in I.members[c] if I.mask(2 * w + tau))


def nbhd(I, tau, Zmask):
    """N_tau[Z]: tau-sides meeting the node mask Zmask"""
    return frozenset(2 * w + tau for w in range(I.m) if (I.E[w] if tau == 0 else I.F[w]) & Zmask)


def sigma(I, tau, U, Phi=()):
    """sigma_U^Phi: class -> mode; mode 1 - tau iff Omega(C, tau) <= U, then flip Phi"""
    modes = {}
    for c in I.classes:
        modes[c] = (1 - tau) if omega(I, c, tau) <= U else tau
    for c in Phi:
        modes[c] = 1 - modes[c]
    return modes


def picks_path(I, modes, P):
    return all(modes[I.side_cls(i)] == (i & 1) for i in P)


def desc(I, f, g, e, want=False):
    """DESC(f, g, e) of §2a: both tau, every union of <= f sets N_tau[Z] (Z a side) and <= g class groups or single
    tau-sides, every flip set of <= e classes.  Sound by construction (accepts only a connecting mode vector)."""
    tried = set()
    for tau in (0, 1):
        Nsets = {}
        for z in I.sides:
            Nsets.setdefault(nbhd(I, tau, I.mask(z)), z)
        Nlist = list(Nsets.items())
        groups = [(omega(I, c, tau), ('G', c)) for c in I.classes if omega(I, c, tau)]
        groups += [(frozenset([i]), ('S', i)) for i in I.sides if (i & 1) == tau]
        for a in range(f + 1):
            for comb in itertools.combinations(Nlist, a):
                base = frozenset().union(*[x[0] for x in comb]) if comb else frozenset()
                for b in range(g + 1):
                    for gcomb in itertools.combinations(groups, b):
                        U = base.union(*[x[0] for x in gcomb]) if gcomb else base
                        key = (tau, U)
                        if key in tried:
                            continue
                        tried.add(key)
                        m0 = sigma(I, tau, U)
                        for ee in range(e + 1):
                            for Phi in itertools.combinations(I.classes, ee):
                                mo = dict(m0)
                                for c in Phi:
                                    mo[c] = 1 - mo[c]
                                if connects(I, mo):
                                    if want:
                                        return True, (tau, [x[1] for x in comb], [x[1] for x in gcomb], Phi, mo)
                                    return True
    return (False, None) if want else False


# ----------------------------------------------------------------------------------------------------------------
# A5: search of Theorem 5 with class conflict families
def a5_search(I, K, B, want_walk=False):
    """Walk Y_1..Y_m: (i) Pi(Y_j) = opposite-type sides of class(Y_j) contained in K; (ii) (class, other type) not
    stored; a member in K stores (class, type); (iii) at most B stored pairs."""
    K = frozenset(K)
    Pi = {i: omega(I, I.side_cls(i), 1 - (i & 1)) for i in I.sides}

    def allowed(y, st):
        if not Pi[y] <= K:
            return None
        c, ty = I.side_cls(y), y & 1
        if (c, 1 - ty) in st:
            return None
        if y in K and (c, ty) not in st:
            ns = st | {(c, ty)}
            if len(ns) > B:
                return None
            return ns
        return st

    par = {}
    q = deque()
    for y in I.sides:
        if (I.mask(y) >> I.s) & 1:
            ns = allowed(y, frozenset())
            if ns is not None and (y, ns) not in par:
                par[(y, ns)] = None
                q.append((y, ns))
    while q:
        st = q.popleft()
        y, S = st
        if (I.mask(y) >> I.t) & 1:
            if not want_walk:
                return True
            walk = []
            cur = st
            while cur is not None:
                walk.append(cur[0])
                cur = par[cur]
            return walk[::-1]
        for z in I.adj[y]:
            ns = allowed(z, S)
            if ns is None:
                continue
            nst = (z, ns)
            if nst not in par:
                par[nst] = st
                q.append(nst)
    return None if want_walk else False


# ----------------------------------------------------------------------------------------------------------------
# generators
def repair_p2(rng, N, E, F, cls, fresh_prob=0.5, extra_nodes=None):
    """add nodes until P2 holds between switches of different classes; returns new N"""
    m = len(E)
    pairs = [(w, v) for w, v in itertools.combinations(range(m), 2) if cls[w] != cls[v]]
    rng.shuffle(pairs)
    for w, v in pairs:
        if (E[w] & E[v]) or (F[w] & F[v]):
            continue
        side = rng.randrange(2)
        if rng.random() < fresh_prob or N == 0:
            z = N
            N += 1
        else:
            pool = extra_nodes if extra_nodes else list(range(N))
            z = rng.choice(pool)
        if side == 0:
            E[w] |= 1 << z
            E[v] |= 1 << z
        else:
            F[w] |= 1 << z
            F[v] |= 1 << z
    return N


def rand_inst(rng, m, nn, ncls, dens=0.3, fresh_prob=0.6):
    """random sides over nn nodes (s = 0, t = 1), random class partition, P2 repaired by node additions"""
    E = [0] * m
    F = [0] * m
    for w in range(m):
        for z in range(nn):
            if rng.random() < dens:
                E[w] |= 1 << z
            if rng.random() < dens:
                F[w] |= 1 << z
    cls = [rng.randrange(ncls) for _ in range(m)]
    N = repair_p2(rng, nn, E, F, cls, fresh_prob)
    return CInst(N, E, F, cls, 0, 1)


def planted_inst(rng, r, nmates, ncls, extra=3, dens=0.15, fresh_prob=0.8, private_p2=True):
    """planted path of length r: positions with classes of one type, path nodes y_i, s in X_1, t in X_r; mates in
    the classes of the path; random noise; P2 repaired with fresh (private) nodes."""
    # classes and types
    ctype = {}
    pos_cls = []
    for a in range(r):
        c = rng.randrange(ncls)
        if c not in ctype:
            ctype[c] = rng.randrange(2)
        pos_cls.append(c)
    m = r + nmates
    cls = pos_cls + [rng.choice(list(ctype)) if rng.random() < 0.8 else ncls + rng.randrange(2) for _ in range(nmates)]
    E = [0] * m
    F = [0] * m
    N = 2  # s = 0, t = 1
    path_side = []
    for a in range(r):
        path_side.append(ctype[pos_cls[a]])
    def add(w, ty, z):
        if ty == 0:
            E[w] |= 1 << z
        else:
            F[w] |= 1 << z
    add(0, path_side[0], 0)
    add(r - 1, path_side[r - 1], 1)
    for a in range(r - 1):
        add(a, path_side[a], N)
        add(a + 1, path_side[a + 1], N)
        N += 1
    # extra nodes with random membership
    base = N
    for _ in range(extra):
        z = N
        N += 1
        for w in range(m):
            for ty in (0, 1):
                if rng.random() < dens:
                    add(w, ty, z)
    # mates' sides: random
    for w in range(r, m):
        for ty in (0, 1):
            if rng.random() < 0.5:
                z = N
                N += 1
                add(w, ty, z)
    N = repair_p2(rng, N, E, F, cls, fresh_prob, extra_nodes=list(range(base, N)) or None)
    return CInst(N, E, F, cls, 0, 1)
