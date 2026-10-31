"""Referee rv-r7-desc: own library, written from the definitions of qp-proof.md (Def. 1.7, 1.8, 4.1, 5.1) and r7-desc.md
Section 2.2.  Does not import anything of open-cases/r7-desc/ or of the other agents' libraries.

Instance: m switches, preorder (bit masks UP, DN), node masks E[w], F[w], terminals s, t, middle edges (z, w, p), z < w,
private node p in F[z] and E[w] only.  A side is an integer: 2w = E_w, 2w + 1 = F_w.  Positions on a path are 1..r.
"""
import json
from collections import Counter


class ClaimFail(Exception):
    pass


class Budget(Exception):
    pass


def chk(c, msg):
    if not c:
        raise ClaimFail(msg)


def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def popcnt(x):
    return bin(x).count("1")


class Inst:
    def __init__(self, m, le, E, F, s, t, nn, me):
        self.m, self.s, self.t, self.nn = m, s, t, nn
        self.E, self.F = list(E), list(F)
        self.me = [tuple(e) for e in me]
        self.le = [[bool(x) for x in row] for row in le]
        self.ALL = (1 << m) - 1
        self.UP = [0] * m
        self.DN = [0] * m
        for i in range(m):
            for j in range(m):
                if le[i][j]:
                    self.UP[i] |= 1 << j
                    self.DN[j] |= 1 << i
        self.CL = [self.UP[i] & self.DN[i] for i in range(m)]
        self.USTR = [self.UP[i] & ~self.CL[i] for i in range(m)]   # strictly above
        self.DSTR = [self.DN[i] & ~self.CL[i] for i in range(m)]   # strictly below
        self.nodeE = [0] * nn
        self.nodeF = [0] * nn
        for w in range(m):
            for n in bits(E[w]):
                self.nodeE[n] |= 1 << w
            for n in bits(F[w]):
                self.nodeF[n] |= 1 << w
        self.LMN = [0] * m
        self.UMN = [0] * m
        for z, w, p in self.me:
            self.LMN[w] |= 1 << z
            self.UMN[z] |= 1 << w
        self.Enon = sum(1 << w for w in range(m) if E[w])
        self.Fnon = sum(1 << w for w in range(m) if F[w])
        # stars (Def. 4.1): E#_w = E_w + {rho(z,w') : z in LMN(w), (z,w') a middle edge}; F#_w dually
        byz = [0] * m       # private nodes of the middle edges (z, *)
        byw = [0] * m       # private nodes of the middle edges (*, w)
        for z, w, p in self.me:
            byz[z] |= 1 << p
            byw[w] |= 1 << p
        self.Estar = []
        self.Fstar = []
        for w in range(m):
            x = E[w]
            for z in bits(self.LMN[w]):
                x |= byz[z]
            self.Estar.append(x)
            y = F[w]
            for z in bits(self.UMN[w]):
                y |= byw[z]
            self.Fstar.append(y)
        self.NEs = [self.NE(z) for z in self.Estar]
        self.NFs = [self.NF(z) for z in self.Fstar]
        self._adj = None
        self._dist = None

    # ---------------------------------------------------------------- basic
    def validate(self):
        m = self.m
        for i in range(m):
            chk(self.UP[i] >> i & 1, "reflexive")
            for j in bits(self.UP[i]):
                chk(self.UP[j] & ~self.UP[i] == 0, "transitive")
        for z, w, p in self.me:
            chk(self.USTR[z] >> w & 1, "middle edge not strict")
            chk(self.F[z] >> p & 1 and self.E[w] >> p & 1, "private node missing")
            chk(self.nodeE[p] == 1 << w and self.nodeF[p] == 1 << z, "private node not private")
        return True

    def comparable(self, x, y):
        return bool(self.UP[x] >> y & 1 or self.DN[x] >> y & 1)

    def leq(self, x, y):
        return bool(self.UP[x] >> y & 1)

    def lt(self, x, y):
        return bool(self.USTR[x] >> y & 1)

    def NE(self, Z):
        r = 0
        for n in bits(Z):
            r |= self.nodeE[n]
        return r

    def NF(self, Z):
        r = 0
        for n in bits(Z):
            r |= self.nodeF[n]
        return r

    def p2_pair(self, x, y):
        return bool(self.E[x] & self.E[y] or self.F[x] & self.F[y] or self.LMN[x] & self.LMN[y]
                    or self.UMN[x] & self.UMN[y])

    def p2(self):
        for x in range(self.m):
            for y in range(x + 1, self.m):
                if not self.comparable(x, y) and not self.p2_pair(x, y):
                    return False
        return True

    def up(self, S):
        r = 0
        for x in bits(S):
            r |= self.UP[x]
        return r

    def down(self, S):
        r = 0
        for x in bits(S):
            r |= self.DN[x]
        return r

    def is_downset(self, D):
        return self.down(D) == D

    def side(self, sd):
        return self.E[sd >> 1] if sd & 1 == 0 else self.F[sd >> 1]

    def connects(self, D):
        """D connects s and t (Def. 1.8)."""
        if self.s == self.t:
            return True
        sides = [self.F[w] if D >> w & 1 else self.E[w] for w in range(self.m)]
        sides = [x for x in sides if x]
        reach = 1 << self.s
        tb = 1 << self.t
        changed = True
        while changed:
            changed = False
            rest = []
            for x in sides:
                if x & reach:
                    if x & ~reach:
                        reach |= x
                        changed = True
                else:
                    rest.append(x)
            sides = rest
            if reach & tb:
                return True
        return bool(reach & tb)

    # ---------------------------------------------------------------- side graph
    def adj(self):
        if self._adj is None:
            ns = [0] * self.nn
            for sd in range(2 * self.m):
                for n in bits(self.side(sd)):
                    ns[n] |= 1 << sd
            self._ns = ns
            a = []
            for sd in range(2 * self.m):
                x = 0
                for n in bits(self.side(sd)):
                    x |= ns[n]
                a.append(x & ~(1 << sd))
            self._adj = [list(bits(x)) for x in a]
        return self._adj

    def dist_to_t(self):
        """Number of further sides needed from each side to a side containing t, ignoring conflicts (lower bound)."""
        if self._dist is None:
            adj = self.adj()
            INF = 10 ** 9
            d = [INF] * (2 * self.m)
            cur = [sd for sd in range(2 * self.m) if self.side(sd) >> self.t & 1]
            for sd in cur:
                d[sd] = 0
            k = 0
            while cur:
                k += 1
                nxt = []
                for x in cur:
                    for y in adj[x]:
                        if d[y] == INF:
                            d[y] = k
                            nxt.append(y)
                cur = nxt
            self._dist = d
        return self._dist

    def conflict(self, s1, s2):
        if s1 & 1 == s2 & 1:
            return False
        e, f = (s1, s2) if s1 & 1 == 0 else (s2, s1)
        return self.leq(e >> 1, f >> 1)

    def is_valid_path(self, P):
        if not P:
            return False
        if not self.side(P[0]) >> self.s & 1 or not self.side(P[-1]) >> self.t & 1:
            return False
        sw = [x >> 1 for x in P]
        if len(set(sw)) != len(sw):
            return False
        for i in range(len(P) - 1):
            if not self.side(P[i]) & self.side(P[i + 1]):
                return False
        for i in range(len(P)):
            for j in range(i + 1, len(P)):
                if self.conflict(P[i], P[j]):
                    return False
        return True

    def shortest(self, bound=None, budget=None):
        """A shortest valid walk (= valid path) with fewer than `bound` sides, or None.  Layered BFS over states
        (side, Up, Dn) with dominance: Up = up-closure of the E-sides used, Dn = down-closure of the F-sides used."""
        adj = self.adj()
        dist = self.dist_to_t()
        s, t = self.s, self.t
        seen = {}
        states = []    # (side, Up, Dn, parent)
        layer = []

        def push(sd, U, Dn, par, k):
            if bound is not None and k + dist[sd] >= bound:
                return
            if dist[sd] >= 10 ** 9:
                return
            lst = seen.setdefault(sd, [])
            for (u0, d0) in lst:
                if u0 & ~U == 0 and d0 & ~Dn == 0:
                    return
            lst[:] = [(u0, d0) for (u0, d0) in lst if not (U & ~u0 == 0 and Dn & ~d0 == 0)]
            lst.append((U, Dn))
            states.append((sd, U, Dn, par))
            layer.append(len(states) - 1)

        def walk(i):
            out = []
            while i is not None:
                out.append(states[i][0])
                i = states[i][3]
            return out[::-1]

        for sd in range(2 * self.m):
            if self.side(sd) >> s & 1:
                w = sd >> 1
                if sd & 1 == 0:
                    push(sd, self.UP[w], 0, None, 1)
                else:
                    push(sd, 0, self.DN[w], None, 1)
        k = 1
        while layer:
            for i in layer:
                if self.side(states[i][0]) >> t & 1:
                    return walk(i)
            cur = layer
            layer = []
            k += 1
            for i in cur:
                sd, U, Dn, _ = states[i]
                for y in adj[sd]:
                    w = y >> 1
                    if y & 1 == 0:
                        if Dn >> w & 1:
                            continue
                        push(y, U | self.UP[w], Dn, i, k)
                    else:
                        if U >> w & 1:
                            continue
                        push(y, U, Dn | self.DN[w], i, k)
                if budget is not None and len(states) > budget:
                    raise Budget()
        return None

    def all_shortest(self, r, cap=None):
        """All valid paths with exactly r sides (r = shortest length)."""
        adj = self.adj()
        dist = self.dist_to_t()
        out = []

        def rec(path, U, Dn):
            if cap is not None and len(out) >= cap:
                return
            sd = path[-1]
            if len(path) == r:
                if self.side(sd) >> self.t & 1:
                    out.append(list(path))
                return
            for y in adj[sd]:
                if len(path) + 1 + dist[y] > r:
                    continue
                w = y >> 1
                if y in path:
                    continue
                if y & 1 == 0:
                    if Dn >> w & 1:
                        continue
                    path.append(y)
                    rec(path, U | self.UP[w], Dn)
                    path.pop()
                else:
                    if U >> w & 1:
                        continue
                    path.append(y)
                    rec(path, U, Dn | self.DN[w])
                    path.pop()

        for sd in range(2 * self.m):
            if self.side(sd) >> self.s & 1 and 1 + dist[sd] <= r:
                w = sd >> 1
                if sd & 1 == 0:
                    rec([sd], self.UP[w], 0)
                else:
                    rec([sd], 0, self.DN[w])
        return out

    # ---------------------------------------------------------------- exact over down-sets (tiny)
    def downsets(self):
        m = self.m
        seen = {0}
        stack = [0]
        while stack:
            D = stack.pop()
            for x in range(m):
                if not D >> x & 1:
                    D2 = D | self.DN[x]
                    if D2 not in seen:
                        seen.add(D2)
                        stack.append(D2)
        return seen

    def exact_downsets(self):
        """(yes, shortest r) by enumeration of all down-sets (Def. 1.8, Lemma 3.4); r = None if none or s = t only."""
        best = None
        yes = self.s == self.t
        for D in self.downsets():
            sides = [self.F[w] if D >> w & 1 else self.E[w] for w in range(self.m)]
            reach = 1 << self.s
            tb = 1 << self.t
            k = 0
            used = [False] * self.m
            found = None
            while True:
                k += 1
                new = 0
                for w in range(self.m):
                    if not used[w] and sides[w] & reach:
                        used[w] = True
                        new |= sides[w]
                if not new:
                    break
                reach |= new
                if new & tb:
                    # a picked side containing t reached with k sides
                    found = k
                    break
            if found is not None:
                yes = True
                if best is None or found < best:
                    best = found
        return yes, best

    # ---------------------------------------------------------------- atoms (r7-desc.md 2.2, 3)
    def FR(self, a1, a2):
        Ux = self.NFs[a1] | self.NFs[a2]
        Pi = self.UP[a1] | self.UP[a2]
        return self.down(self.Fnon & ~Ux & ~Pi)

    def ER(self, b1, b2):
        Ux = self.NEs[b1] | self.NEs[b2]
        Pi = self.DN[b1] | self.DN[b2]
        return self.ALL & ~self.up(self.Enon & ~Ux & ~Pi)

    def EP(self, a):
        Gam = self.Enon & ~self.NEs[a] & ~self.DSTR[a]
        return self.ALL & ~self.up(Gam)

    def FP(self, h):
        Gam = self.Fnon & ~self.NFs[h] & ~self.USTR[h]
        return self.down(Gam)

    # ---------------------------------------------------------------- transforms, io
    def reversed_st(self):
        return Inst(self.m, self.le, self.E, self.F, self.t, self.s, self.nn, self.me)

    def op(self):
        m = self.m
        le = [[self.le[j][i] for j in range(m)] for i in range(m)]
        return Inst(m, le, self.F, self.E, self.s, self.t, self.nn, [(w, z, p) for (z, w, p) in self.me])

    def dump(self, path, extra=None):
        d = {"m": self.m, "le": [[int(b) for b in row] for row in self.le], "E": [hex(x) for x in self.E],
             "F": [hex(x) for x in self.F], "s": self.s, "t": self.t, "nn": self.nn,
             "me": [list(e) for e in self.me], "extra": extra or {}}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f)


def conv(x):
    return int(x, 16) if isinstance(x, str) else int(x)


def inst_from_json(d):
    """General switch form JSON: r7-lb format (m, le, E, F, s, t, nn, me) or r5-core format (medge, N)."""
    if "medge" in d:
        E = [int(x) for x in d["E"]]
        F = [int(x) for x in d["F"]]
        me = [(int(v[0]), int(v[1]), int(p)) for p, v in d["medge"].items()]
        return Inst(len(E), d["le"], E, F, d["s"], d["t"], d["N"], me)
    return Inst(d["m"], d["le"], [conv(x) for x in d["E"]], [conv(x) for x in d["F"]], d["s"], d["t"], d["nn"],
                [tuple(e) for e in d["me"]])


def inst_from_zz(n, le, R, u, v):
    """Own implementation of Construction 3.1 of qp-proof.md (preorder le, real edges R, u least, v greatest)."""
    cu = [x for x in range(n) if le[x][u] and le[u][x]]
    cv = [x for x in range(n) if le[x][v] and le[v][x]]
    if set(cu) & set(cv):
        return None
    Mset = [x for x in range(n) if x not in cu and x not in cv]
    idx = {x: i for i, x in enumerate(Mset)}
    uf = {x: x for x in cu + cv}

    def find(x):
        while uf[x] != x:
            uf[x] = uf[uf[x]]
            x = uf[x]
        return x

    edges = []
    for a, b in R:
        if not le[a][b] or le[b][a]:
            a, b = b, a
        edges.append((a, b))
    for a, b in edges:
        if a in uf and b in uf:
            uf[find(a)] = find(b)
    comp = {}
    for x in cu + cv:
        comp.setdefault(find(x), len(comp))
    node = {x: comp[find(x)] for x in cu + cv}
    nn = len(comp)
    m = len(Mset)
    E = [0] * m
    F = [0] * m
    me = []
    for a, b in edges:
        if a in uf and b in uf:
            continue
        if a in uf:             # a in [u], b in M
            E[idx[b]] |= 1 << node[a]
        elif b in uf:           # a in M, b in [v]
            F[idx[a]] |= 1 << node[b]
        else:
            p = nn
            nn += 1
            F[idx[a]] |= 1 << p
            E[idx[b]] |= 1 << p
            me.append((idx[a], idx[b], p))
    le2 = [[bool(le[x][y]) for y in Mset] for x in Mset]
    return Inst(m, le2, E, F, node[u], node[v], nn, me)


def path_rev(P):
    return list(P)[::-1]


def path_op(P):
    return [x ^ 1 for x in P]


def new_stats():
    return Counter()
