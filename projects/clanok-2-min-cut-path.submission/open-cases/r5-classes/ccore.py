"""Core of agent r5-classes: 2CH with classes (+ P2).

Instance: nodes 0..N-1, terminals s != t, switches w = 0..n-1 with node sets E_w, F_w (bit masks; 0 = empty)
and a class cl[w].  A mode vector gives every class one mode (0 = E, 1 = F); every switch of the class picks the
side of that mode.  Yes-instance iff s and t are connected in the hypergraph of the picked sides.
P2 (classes): for switches w, v of DIFFERENT classes, E_w & E_v != 0 or F_w & F_v != 0.

Sides: sid = 2*w + typ (typ 0 = E, 1 = F), only for non-empty node sets.  Pi(sid) = the non-empty sides of the
opposite type of all switches of the class of sid (the conflict family).  A *valid path*: sides X_1 .. X_r, s in X_1,
t in X_r, consecutive sides meet, sides pairwise distinct, no two sides of one class with different types.  A
*valid walk*: consecutive sides equal or meeting, no conflicting pair.  Yes iff a valid path (walk) exists.

Written from the definitions of r5-brief.md section 3 (no import of other agents' code).
"""
import itertools
import random
from collections import deque


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def orbits(it):
    m = 0
    for x in it:
        m |= 1 << x
    return m


def popcount(m):
    return bin(m).count("1")


class Inst:
    def __init__(self, N, s, t, sw, cl):
        self.N, self.s, self.t = N, s, t
        self.sw = [(int(E), int(F)) for E, F in sw]
        self.cl = list(cl)
        self.n = len(self.sw)
        assert len(self.cl) == self.n
        self.classes = sorted(set(self.cl))
        self.cidx = {c: i for i, c in enumerate(self.classes)}
        self.k = len(self.classes)
        self.members = {c: [w for w in range(self.n) if self.cl[w] == c] for c in self.classes}
        self.sides = [2 * w + ty for w in range(self.n) for ty in (0, 1) if self.sw[w][ty]]
        self.sideset = set(self.sides)
        self.mask = {i: self.sw[i >> 1][i & 1] for i in self.sides}
        self.scls = {i: self.cl[i >> 1] for i in self.sides}
        self.adj = {i: [] for i in self.sides}
        S = self.sides
        for a in range(len(S)):
            for b in range(a + 1, len(S)):
                if self.mask[S[a]] & self.mask[S[b]]:
                    self.adj[S[a]].append(S[b])
                    self.adj[S[b]].append(S[a])
        self.has_s = {i: bool((self.mask[i] >> s) & 1) for i in S}
        self.has_t = {i: bool((self.mask[i] >> t) & 1) for i in S}
        # conflict family: sides of the class of i with the other type
        self.Pi = {}
        for i in S:
            c, ty = self.scls[i], i & 1
            self.Pi[i] = frozenset(2 * w + (1 - ty) for w in self.members[c] if self.sw[w][1 - ty])
        # class groups Omega(c, ty): all non-empty sides of class c with type ty
        self.Omega = {(c, ty): frozenset(2 * w + ty for w in self.members[c] if self.sw[w][ty])
                      for c in self.classes for ty in (0, 1)}

    # ---------------------------------------------------------------------------------------------------- misc
    def to_json(self):
        return {"N": self.N, "s": self.s, "t": self.t, "sw": [[bits(E), bits(F)] for E, F in self.sw],
                "cl": self.cl}

    @staticmethod
    def from_json(d):
        sw = [(sum(1 << x for x in E), sum(1 << x for x in F)) for E, F in d["sw"]]
        return Inst(d["N"], d["s"], d["t"], sw, d["cl"])

    def fmt(self):
        return "N=%d s=%d t=%d " % (self.N, self.s, self.t) + " ".join(
            "[w%d c%s: E=%s F=%s]" % (w, self.cl[w], bits(E), bits(F)) for w, (E, F) in enumerate(self.sw))

    def sname(self, i):
        return "%s%d" % ("EF"[i & 1], i >> 1)

    def conflict(self, i, j):
        return self.scls[i] == self.scls[j] and (i & 1) != (j & 1)

    def N_of(self, ty, z):
        """N_ty[Z]: all sides of type ty meeting the side z (contains z if z has type ty)."""
        Z = self.mask[z]
        return frozenset(i for i in self.sides if (i & 1) == ty and self.mask[i] & Z)


# -------------------------------------------------------------------------------------------------------- P2
def p2_missing(inst):
    out = []
    sw, cl = inst.sw, inst.cl
    for w in range(inst.n):
        for v in range(w + 1, inst.n):
            if cl[w] != cl[v] and not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                out.append((w, v))
    return out


def p2_ok(inst):
    sw, cl = inst.sw, inst.cl
    for w in range(inst.n):
        for v in range(w + 1, inst.n):
            if cl[w] != cl[v] and not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                return False
    return True


# -------------------------------------------------------------------------------------------------- solvers
def connected_masks(masks, s, t):
    if s == t:
        return True
    comp = 1 << s
    rest = [h for h in masks if h]
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


def picked_masks(inst, modes):
    """modes: dict class -> 0/1"""
    return [inst.sw[w][modes[inst.cl[w]]] for w in range(inst.n)]


def brute(inst):
    """A connecting mode dict, or None.  Exponential in the number of classes."""
    if inst.s == inst.t:
        return {c: 0 for c in inst.classes}
    for mask in range(1 << inst.k):
        modes = {c: (mask >> j) & 1 for j, c in enumerate(inst.classes)}
        if connected_masks(picked_masks(inst, modes), inst.s, inst.t):
            return modes
    return None


def all_solutions(inst):
    out = []
    for mask in range(1 << inst.k):
        modes = {c: (mask >> j) & 1 for j, c in enumerate(inst.classes)}
        if connected_masks(picked_masks(inst, modes), inst.s, inst.t):
            out.append(modes)
    return out


def exact(inst):
    """Exact answer by DFS over valid paths with state (current side, partial class assignment)."""
    if inst.s == inst.t:
        return True
    seen = set()
    stack = []
    for i in inst.sides:
        if inst.has_s[i]:
            st = (i, frozenset([(inst.scls[i], i & 1)]))
            if st not in seen:
                seen.add(st)
                stack.append(st)
    while stack:
        cur, asg = stack.pop()
        if inst.has_t[cur]:
            return True
        for j in inst.adj[cur]:
            c, ty = inst.scls[j], j & 1
            if (c, 1 - ty) in asg:
                continue
            st = (j, asg | {(c, ty)})
            if st not in seen:
                seen.add(st)
                stack.append(st)
    return False


def dist_to_t(inst):
    INF = 10 ** 9
    d = {i: INF for i in inst.sides}
    q = deque()
    for i in inst.sides:
        if inst.has_t[i]:
            d[i] = 0
            q.append(i)
    while q:
        i = q.popleft()
        for j in inst.adj[i]:
            if d[j] == INF:
                d[j] = d[i] + 1
                q.append(j)
    return d


def shortest_valid_paths(inst, limit=None, maxlen=None):
    """(L, list of all shortest valid paths) or (None, []).  Level L searches only paths whose non-consecutive
    members are disjoint, with s only in the first and t only in the last member; every shortest valid path has
    these properties and every path found is valid, so the first level with a path gives all shortest ones."""
    assert inst.s != inst.t
    dt = dist_to_t(inst)
    INF = 10 ** 9
    starts = [i for i in inst.sides if inst.has_s[i]]
    if not starts or min(dt[i] for i in starts) >= INF:
        return None, []
    top = maxlen if maxlen is not None else len(inst.sides)
    mask = inst.mask
    for L in range(1, top + 1):
        found = []
        path = []
        asg = {}

        def rec(last):
            kk = len(path)
            if kk == L:
                if inst.has_t[last]:
                    found.append(tuple(path))
                return limit is not None and len(found) >= limit
            if inst.has_t[last]:
                return False
            for y in inst.adj[last]:
                if inst.has_s[y]:
                    continue
                if kk + 1 + dt[y] > L:
                    continue
                if inst.has_t[y] and kk + 1 < L:
                    continue
                c, ty = inst.scls[y], y & 1
                if asg.get(c, ty) != ty:
                    continue
                if y in path:
                    continue
                ok = True
                for z in path[:-1]:
                    if mask[z] & mask[y]:
                        ok = False
                        break
                if not ok:
                    continue
                path.append(y)
                new = c not in asg
                if new:
                    asg[c] = ty

                stop = rec(y)
                if new:
                    del asg[c]
                path.pop()
                if stop:
                    return True
            return False

        for x in starts:
            if 1 + dt[x] > L:
                continue
            path.append(x)
            asg[inst.scls[x]] = x & 1
            stop = rec(x)
            del asg[inst.scls[x]]
            path.pop()
            if stop:
                break
        if found:
            return L, found
    return None, []


def is_valid_path(inst, P):
    if not P or not inst.has_s[P[0]] or not inst.has_t[P[-1]]:
        return False
    for a in range(len(P) - 1):
        if not (inst.mask[P[a]] & inst.mask[P[a + 1]]):
            return False
    if len(set(P)) != len(P):
        return False
    tys = {}
    for x in P:
        c, ty = inst.scls[x], x & 1
        if tys.setdefault(c, ty) != ty:
            return False
    return True


def is_valid_walk(inst, W):
    if not W or not inst.has_s[W[0]] or not inst.has_t[W[-1]]:
        return False
    for a in range(len(W) - 1):
        if W[a] != W[a + 1] and not (inst.mask[W[a]] & inst.mask[W[a + 1]]):
            return False
    tys = {}
    for x in W:
        c, ty = inst.scls[x], x & 1
        if tys.setdefault(c, ty) != ty:
            return False
    return True


# ------------------------------------------------------------------------------------- certificate search
def csearch(inst, K, B, want_walk=True):
    """Search of Theorem 5 with class conflict families (brief A5).

    A walk Y_1 .. Y_m is admissible if for every j: (i) Pi(Y_j) is contained in K; (ii) the pair
    (class(Y_j), other type) is not stored; a member lying in K stores (class, type); (iii) at most B stored pairs.
    Sound for every K and B: a conflicting pair Y_i, Y_j (i < j) has Y_j in Pi(Y_i) and Y_i in Pi(Y_j), both in K by
    (i), so (class, type(Y_i)) is stored at step i and Y_j is refused at step j.
    Returns an admissible walk (list of sides) or None."""
    K = frozenset(K)
    okside = {i: inst.Pi[i] <= K for i in inst.sides}

    def allowed(y, stored):
        if not okside[y]:
            return None
        c, ty = inst.scls[y], y & 1
        if (c, 1 - ty) in stored:
            return None
        if y in K and (c, ty) not in stored:
            ns = stored | {(c, ty)}
            if len(ns) > B:
                return None
            return ns
        return stored

    par = {}
    q = deque()
    for y in inst.sides:
        if not inst.has_s[y]:
            continue
        ns = allowed(y, frozenset())
        if ns is None:
            continue
        st = (y, ns)
        if st not in par:
            par[st] = None
            q.append(st)
    while q:
        st = q.popleft()
        y, stored = st
        if inst.has_t[y]:
            if not want_walk:
                return True
            walk = []
            cur = st
            while cur is not None:
                walk.append(cur[0])
                cur = par[cur]
            return walk[::-1]
        for z in inst.adj[y]:
            ns = allowed(z, stored)
            if ns is None:
                continue
            nst = (z, ns)
            if nst not in par:
                par[nst] = st
                q.append(nst)
    return None


def storage(inst, P, K):
    """number of distinct (class, type) pairs of members of P lying in K"""
    return len({(inst.scls[x], x & 1) for x in P if x in K})


def needed(inst, P):
    """the set of sides a certificate of P must contain: union of Pi(X) over members X of P"""
    out = set()
    for x in P:
        out |= inst.Pi[x]
    return frozenset(out)


# ----------------------------------------------------------------------------------- propagation, contraction
def component(inst, fixed, start):
    """node mask of the component of `start` in the hypergraph of the sides picked by the fixed classes"""
    comp = 1 << start
    hs = [inst.sw[w][fixed[inst.cl[w]]] for w in range(inst.n) if inst.cl[w] in fixed]
    hs = [h for h in hs if h]
    changed = True
    while changed:
        changed = False
        keep = []
        for h in hs:
            if h & comp:
                comp |= h
                changed = True
            else:
                keep.append(h)
        hs = keep
    return comp


def propagate(inst, fixed):
    """Forced-exit propagation from s and from t (r4-general.md section 7.3, with classes).
    fixed: dict class -> mode (modified copy returned).  Returns (status, fixed) with status 'refuted', 'solved'
    (s, t connected by fixed sides) or 'open'.  Sound: every mode added is a mode of every solution extending the
    input assignment."""
    fixed = dict(fixed)
    while True:
        progress = False
        for start, other in ((inst.s, inst.t), (inst.t, inst.s)):
            comp = component(inst, fixed, start)
            if (comp >> other) & 1:
                return "solved", fixed
            exits = set()
            for i in inst.sides:
                c = inst.scls[i]
                if c in fixed:
                    continue
                m = inst.mask[i]
                if m & comp and m & ~comp:
                    exits.add((c, i & 1))
            if not exits:
                return "refuted", fixed
            if len(exits) == 1:
                (c, ty), = exits
                fixed[c] = ty
                progress = True
        if not progress:
            return "open", fixed


def prune(inst, fixed=None, max_rounds=1000):
    """Failed-literal probing on top of propagate.  Returns (status, fixed)."""
    fixed = dict(fixed or {})
    st, fixed = propagate(inst, fixed)
    if st != "open":
        return st, fixed
    for _ in range(max_rounds):
        changed = False
        for c in inst.classes:
            if c in fixed:
                continue
            res = []
            for ty in (0, 1):
                f2 = dict(fixed)
                f2[c] = ty
                st2, _ = propagate(inst, f2)
                res.append(st2)
            if res[0] == "refuted" and res[1] == "refuted":
                return "refuted", fixed
            if res[0] == "refuted" or res[1] == "refuted":
                fixed[c] = 1 if res[0] == "refuted" else 0
                st, fixed = propagate(inst, fixed)
                if st != "open":
                    return st, fixed
                changed = True
        if not changed:
            break
    return "open", fixed


def contract(inst, fixed):
    """Contract the sides picked by fixed classes (each to one node); keep the free switches.  Returns the new
    instance and the node map.  s-t connectivity is kept for every mode vector of the free classes."""
    par = list(range(inst.N))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for w in range(inst.n):
        c = inst.cl[w]
        if c in fixed:
            ns = bits(inst.sw[w][fixed[c]])
            for x in ns[1:]:
                rx, r0 = find(x), find(ns[0])
                if rx != r0:
                    par[rx] = r0
    roots = {}
    nmap = {}
    for x in range(inst.N):
        r = find(x)
        if r not in roots:
            roots[r] = len(roots)
        nmap[x] = roots[r]
    sw, cl = [], []
    for w in range(inst.n):
        if inst.cl[w] in fixed:
            continue
        E, F = inst.sw[w]
        sw.append((orbits(nmap[x] for x in bits(E)), orbits(nmap[x] for x in bits(F))))
        cl.append(inst.cl[w])
    return Inst(len(roots), nmap[inst.s], nmap[inst.t], sw, cl), nmap


def normalize_blobs(inst):
    """Blob form: every T-side of a class is replaced by the union of its connected component among the T-sides of
    that class; identical switches of one class are merged.  Answer and P2 are kept."""
    sw = [list(x) for x in inst.sw]
    for c in inst.classes:
        mem = inst.members[c]
        for ty in (0, 1):
            ms = [inst.sw[w][ty] for w in mem]
            # components among non-empty masks
            comp = list(range(len(mem)))

            def f(x):
                while comp[x] != x:
                    comp[x] = comp[comp[x]]
                    x = comp[x]
                return x
            for a in range(len(mem)):
                for b in range(a + 1, len(mem)):
                    if ms[a] & ms[b]:
                        ra, rb = f(a), f(b)
                        if ra != rb:
                            comp[ra] = rb
            union = {}
            for a in range(len(mem)):
                union[f(a)] = union.get(f(a), 0) | ms[a]
            for a in range(len(mem)):
                if ms[a]:
                    sw[mem[a]][ty] = union[f(a)]
    seen = set()
    nsw, ncl = [], []
    for w in range(inst.n):
        key = (inst.cl[w], sw[w][0], sw[w][1])
        if key in seen:
            continue
        seen.add(key)
        nsw.append(tuple(sw[w]))
        ncl.append(inst.cl[w])
    return Inst(inst.N, inst.s, inst.t, nsw, ncl)


# ---------------------------------------------------------------------------------------------- generators
def p2_repair(rng, N, sw, cl, fresh=0.5):
    """for every cross-class pair violating P2 add a node to both E-sides or both F-sides (fresh with prob.)"""
    sw = [list(x) for x in sw]
    NN = N
    pairs = [(w, v) for w in range(len(sw)) for v in range(w + 1, len(sw)) if cl[w] != cl[v]]
    rng.shuffle(pairs)
    for w, v in pairs:
        if (sw[w][0] & sw[v][0]) or (sw[w][1] & sw[v][1]):
            continue
        if rng.random() < fresh:
            z = NN
            NN += 1
        else:
            z = rng.randrange(NN)
        ty = rng.randrange(2)
        sw[w][ty] |= 1 << z
        sw[v][ty] |= 1 << z
    return NN, [tuple(x) for x in sw]


def random_instance(rng, N, n, k, pe, pf, fresh=0.5, p2=True):
    cl = [rng.randrange(k) for _ in range(n)]
    sw = [(sum(1 << x for x in range(N) if rng.random() < pe), sum(1 << x for x in range(N) if rng.random() < pf))
          for _ in range(n)]
    NN = N
    if p2:
        NN, sw = p2_repair(rng, N, sw, cl, fresh)
    return Inst(NN, 0, 1, sw, cl)


if __name__ == "__main__":
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    rng = random.Random(seed)
    stats = {"yes": 0, "no": 0, "bad": 0, "p2": 0}
    for it in range(count):
        N = rng.randint(3, 8)
        n = rng.randint(2, 9)
        k = rng.randint(1, min(n, 6))
        inst = random_instance(rng, N, n, k, rng.choice([0.15, 0.25, 0.35]), rng.choice([0.15, 0.25, 0.35]),
                               fresh=rng.random(), p2=rng.random() < 0.7)
        b = brute(inst) is not None
        e = exact(inst)
        stats["p2"] += p2_ok(inst)
        L, paths = shortest_valid_paths(inst)
        ok = (b == e) and ((L is not None) == b)
        for P in paths:
            ok &= is_valid_path(inst, P)
        # full search with K = all sides, B = everything: exact
        W = csearch(inst, inst.sides, 10 ** 9)
        ok &= ((W is not None) == b)
        if W is not None:
            ok &= is_valid_walk(inst, W)
        # random K, B never accept a no-instance; accepted walks valid
        for _ in range(4):
            K = [i for i in inst.sides if rng.random() < 0.6]
            W = csearch(inst, K, rng.randint(0, 4))
            if W is not None:
                ok &= is_valid_walk(inst, W)
        nb = normalize_blobs(inst)
        ok &= ((brute(nb) is not None) == b)
        if p2_ok(inst):
            ok &= p2_ok(nb)
        st, fx = prune(inst)
        if st == "refuted":
            ok &= not b
        if st == "solved":
            ok &= b
        if b:
            sol = brute(inst)
        if st == "open" and b:
            ci, _ = contract(inst, fx)
            ok &= (brute(ci) is not None)
        if not ok:
            stats["bad"] += 1
            print("BAD", inst.fmt())
        stats["yes" if b else "no"] += 1
    print(stats)


# ------------------------------------------------------------------------------------------ relaxed probing
def relaxed_connected(inst, fixed):
    """s-t connectivity in the hypergraph of the sides picked by fixed classes plus ALL sides of free classes
    (conflicts among free classes ignored): a superset of every picked hypergraph extending `fixed`."""
    masks = []
    for w in range(inst.n):
        c = inst.cl[w]
        if c in fixed:
            masks.append(inst.sw[w][fixed[c]])
        else:
            masks.append(inst.sw[w][0])
            masks.append(inst.sw[w][1])
    return connected_masks(masks, inst.s, inst.t)


def relaxed_prune(inst, fixed=None, max_rounds=1000):
    """Failed-literal probing with the relaxed connectivity test (sound), interleaved with propagate.
    Returns (status, fixed)."""
    fixed = dict(fixed or {})
    st, fixed = propagate(inst, fixed)
    if st != "open":
        return st, fixed
    for _ in range(max_rounds):
        changed = False
        for c in inst.classes:
            if c in fixed:
                continue
            res = []
            for ty in (0, 1):
                f2 = dict(fixed)
                f2[c] = ty
                st2, f3 = propagate(inst, f2)
                if st2 == "open" and not relaxed_connected(inst, f3):
                    st2 = "refuted"
                res.append(st2)
            if res[0] == "refuted" and res[1] == "refuted":
                return "refuted", fixed
            if res[0] == "refuted" or res[1] == "refuted":
                fixed[c] = 1 if res[0] == "refuted" else 0
                st, fixed = propagate(inst, fixed)
                if st != "open":
                    return st, fixed
                if not relaxed_connected(inst, fixed):
                    return "refuted", fixed
                changed = True
        if not changed:
            break
    return "open", fixed
