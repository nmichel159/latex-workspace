"""Core library of the referee checks: instances of ZZ (def:zz-zz), walks (def:zz-valid), atoms and formulas (def:pa-atoms).

Written from the text of main.tex only.  Elements are 0..m-1, sets are integer bit masks.
UP[x] = up(x), DN[x] = down(x), LO[x] = lower neighbours in R, HI[x] = upper neighbours in R.
A walk is a list of elements together with the label of its first position; lists run in either direction.
"""
INF = 10 ** 9


class ClaimFail(Exception):
    """A statement of the text failed on a concrete instance."""


class Budget(Exception):
    """The exact solver exceeded its state budget."""


def chk(cond, msg):
    if not cond:
        raise ClaimFail(msg)


def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def popcnt(x):
    return bin(x).count("1")


class Inst:
    """(Q, <=, R, u, v).  up: list of masks with up[x] = {y : x <= y}; edges: pairs (a, b) with a < b."""

    def __init__(self, m, up, edges, u, v, names=None):
        self.m, self.u, self.v = m, u, v
        self.ALL = (1 << m) - 1
        self.UP = list(up)
        self.DN = [0] * m
        for x in range(m):
            for y in bits(self.UP[x]):
                self.DN[y] |= 1 << x
        self.CL = [self.UP[x] & self.DN[x] for x in range(m)]
        self.USTR = [self.UP[x] & ~self.CL[x] for x in range(m)]
        self.DSTR = [self.DN[x] & ~self.CL[x] for x in range(m)]
        self.edges = set(edges)
        self.LO = [0] * m
        self.HI = [0] * m
        for a, b in self.edges:
            self.HI[a] |= 1 << b
            self.LO[b] |= 1 << a
        self.MB = [0] * m
        self.MA = [0] * m
        for x in range(m):
            for z in bits(self.LO[x]):
                self.MB[x] |= self.HI[z]
            for z in bits(self.HI[x]):
                self.MA[x] |= self.LO[z]
        self.names = names
        self._dist = None

    def name(self, x):
        return self.names[x] if self.names else str(x)

    # ------------------------------------------------------------- order
    def leq(self, x, y):
        return bool(self.UP[x] >> y & 1)

    def lt(self, x, y):
        return bool(self.USTR[x] >> y & 1)

    def tied(self, x, y):
        return bool(self.CL[x] >> y & 1)

    def inc(self, x, y):
        return not self.leq(x, y) and not self.leq(y, x)

    def up(self, S):
        r = 0
        for x in bits(S):
            r |= self.UP[x]
        return r

    def dn(self, S):
        r = 0
        for x in bits(S):
            r |= self.DN[x]
        return r

    def is_downset(self, D):
        return self.dn(D) == D

    # ------------------------------------------------------------- definitions
    def validate(self):
        """All requirements of def:zz-zz."""
        m = self.m
        for x in range(m):
            chk(self.UP[x] >> x & 1, "preorder: reflexive")
            for y in bits(self.UP[x]):
                chk(self.UP[y] & ~self.UP[x] == 0, "preorder: transitive")
            chk(self.leq(self.u, x) and self.leq(x, self.v), "u <= x <= v")
        chk(self.lt(self.u, self.v), "u < v")
        for a, b in self.edges:
            chk(self.lt(a, b), "edge with a < b")

    def p2(self):
        for x in range(self.m):
            inc = self.ALL & ~self.UP[x] & ~self.DN[x]
            if inc & ~(self.MB[x] | self.MA[x]):
                return False
        return True

    def p2_violations(self):
        out = []
        for x in range(self.m):
            inc = self.ALL & ~self.UP[x] & ~self.DN[x] & ~(self.MB[x] | self.MA[x])
            for y in bits(inc):
                if x < y:
                    out.append((x, y))
        return out

    def connected_in_GD(self, D):
        """u and v connected in G_D."""
        reach = 1 << self.u
        stack = [self.u]
        while stack:
            x = stack.pop()
            if D >> x & 1:
                nb = self.HI[x] & ~D
            else:
                nb = self.LO[x] & D
            new = nb & ~reach
            reach |= new
            for y in bits(new):
                stack.append(y)
        return bool(reach >> self.v & 1)

    def dist_in_GD(self, D):
        """Length of a shortest u-v path of G_D, or None."""
        reach = 1 << self.u
        cur = [self.u]
        k = 0
        while cur:
            if reach >> self.v & 1:
                return k
            k += 1
            nxt = []
            for x in cur:
                nb = (self.HI[x] & ~D) if D >> x & 1 else (self.LO[x] & D)
                new = nb & ~reach
                reach |= new
                nxt.extend(bits(new))
            cur = nxt
        return None

    def downsets(self):
        """All down-sets D with u in D and v not in D."""
        start = self.DN[self.u]
        seen = {start}
        stack = [start]
        while stack:
            D = stack.pop()
            for x in bits(self.ALL & ~D):
                E = D | self.DN[x]
                if not E >> self.v & 1 and E not in seen:
                    seen.add(E)
                    stack.append(E)
        return seen

    # ------------------------------------------------------------- walks
    def label_of(self, W):
        """Labels (list of 'L', 'H') of a sequence with the ends u and v; the end u is low."""
        if W[0] == self.u:
            first = "L"
        elif W[0] == self.v:
            first = "H"
        else:
            raise ClaimFail("walk does not start at u or v")
        return [first if i % 2 == 0 else ("H" if first == "L" else "L") for i in range(len(W))]

    def is_walk(self, W, labels=None):
        """def:zz-valid: the ends are u and v, labels alternate, the end u is low, the end v is high, every consecutive pair is
        an edge with its lower end at the low position."""
        if len(W) < 2:
            return False
        if {W[0], W[-1]} != {self.u, self.v}:
            return False
        if labels is None:
            labels = self.label_of(W)
        for i in range(len(W)):
            if W[i] == self.u and i in (0, len(W) - 1) and labels[i] != "L":
                return False
            if W[i] == self.v and i in (0, len(W) - 1) and labels[i] != "H":
                return False
        for i in range(len(W) - 1):
            if labels[i] == labels[i + 1]:
                return False
            lo, hi = (W[i], W[i + 1]) if labels[i] == "L" else (W[i + 1], W[i])
            if (lo, hi) not in self.edges:
                return False
        return True

    def is_valid_walk(self, W, labels=None):
        if not self.is_walk(W, labels):
            return False
        if labels is None:
            labels = self.label_of(W)
        highs = [W[i] for i in range(len(W)) if labels[i] == "H"]
        lows = [W[i] for i in range(len(W)) if labels[i] == "L"]
        for h in highs:
            for l in lows:
                if self.leq(h, l):
                    return False
        return True

    def dist_to_v(self):
        """Lower bound on the remaining length from (x, label) to v, ignoring validity.  Index 2x = x low, 2x + 1 = x high."""
        if self._dist is None:
            d = [INF] * (2 * self.m)
            d[2 * self.v + 1] = 0
            cur = [2 * self.v + 1]
            k = 0
            while cur:
                k += 1
                nxt = []
                for st in cur:
                    x, hi = st >> 1, st & 1
                    if hi:
                        # previous element is low and has x as an upper neighbour
                        for y in bits(self.LO[x]):
                            if d[2 * y] == INF:
                                d[2 * y] = k
                                nxt.append(2 * y)
                    else:
                        for y in bits(self.HI[x]):
                            if d[2 * y + 1] == INF:
                                d[2 * y + 1] = k
                                nxt.append(2 * y + 1)
                cur = nxt
            self._dist = d
        return self._dist

    def shortest_walk(self, bound=None, budget=None):
        """Exact: a shortest valid walk from u to v of length < bound (or None).  Layered BFS over states (x, label, Up, Dn), where
        Up = up-closure of the highs, Dn = down-closure of the lows, with dominance on (Up, Dn)."""
        dist = self.dist_to_v()
        states = []
        seen = {}
        layer = []

        def push(st, U, Dn, par, k):
            if dist[st] >= INF:
                return
            if bound is not None and k + dist[st] >= bound:
                return
            lst = seen.setdefault(st, [])
            for (u0, d0) in lst:
                if u0 & ~U == 0 and d0 & ~Dn == 0:
                    return
            lst[:] = [(u0, d0) for (u0, d0) in lst if not (U & ~u0 == 0 and Dn & ~d0 == 0)]
            lst.append((U, Dn))
            states.append((st, U, Dn, par))
            layer.append(len(states) - 1)

        push(2 * self.u, 0, self.DN[self.u], None, 0)
        k = 0
        target = 2 * self.v + 1
        while layer:
            for i in layer:
                if states[i][0] == target:
                    out = []
                    j = i
                    while j is not None:
                        out.append(states[j][0] >> 1)
                        j = states[j][3]
                    return out[::-1]
            cur = layer
            layer = []
            k += 1
            for i in cur:
                st, U, Dn, _ = states[i]
                x, hi = st >> 1, st & 1
                if hi:
                    for y in bits(self.LO[x]):
                        if U >> y & 1:
                            continue
                        push(2 * y, U, Dn | self.DN[y], i, k)
                else:
                    for y in bits(self.HI[x]):
                        if Dn >> y & 1:
                            continue
                        push(2 * y + 1, U | self.UP[y], Dn, i, k)
                if budget is not None and len(states) > budget:
                    raise Budget()
        return None

    def all_shortest(self, q, cap=50):
        """Valid walks from u to v with exactly q edges, at most cap of them (DFS with the distance bound)."""
        dist = self.dist_to_v()
        out = []
        nodes = [0]

        def rec(path, hi, U, Dn):
            nodes[0] += 1
            if len(out) >= cap or nodes[0] > 200000:
                return
            x = path[-1]
            k = len(path) - 1
            if k == q:
                if x == self.v and hi:
                    out.append(list(path))
                return
            if hi:
                for y in bits(self.LO[x]):
                    if not U >> y & 1 and k + 1 + dist[2 * y] <= q:
                        path.append(y)
                        rec(path, 0, U, Dn | self.DN[y])
                        path.pop()
            else:
                for y in bits(self.HI[x]):
                    if not Dn >> y & 1 and k + 1 + dist[2 * y + 1] <= q:
                        path.append(y)
                        rec(path, 1, U | self.UP[y], Dn)
                        path.pop()

        rec([self.u], 0, 0, self.DN[self.u])
        return out

    # ------------------------------------------------------------- atoms, def:pa-atoms
    def FR(self, x, y):
        g = self.ALL & ~(self.MA[x] | self.MA[y] | self.UP[x] | self.UP[y])
        return self.dn(g)

    def ER(self, x, y):
        g = self.ALL & ~(self.MB[x] | self.MB[y] | self.DN[x] | self.DN[y])
        return self.ALL & ~self.up(g)

    def EP(self, x):
        g = self.ALL & ~(self.MB[x] | (self.DN[x] & ~self.CL[x]))
        return self.ALL & ~self.up(g)

    def F_formula(self, xs, S, Sp):
        """xs = list of pairs, at most three, the third (if given as third entry) also carries the EP term; None omits a pair.
        S, Sp are masks."""
        chk(popcnt(S) <= 19 and popcnt(Sp) <= 6, "F-formula: sizes")
        D = self.dn(S)
        for i, pr in enumerate(xs):
            if pr is None:
                continue
            D |= self.FR(*pr)
            if i == 2:
                D |= (self.EP(pr[0]) | self.EP(pr[1])) & ~self.up(Sp)
        return D

    def E_formula(self, xs, S):
        chk(popcnt(S) <= 16, "E-formula: sizes")
        chk(len([p for p in xs if p is not None]) <= 4, "E-formula: at most four pairs")
        D = self.ALL
        for pr in xs:
            if pr is not None:
                D &= self.ER(*pr)
        return D & ~self.up(S)

    # ------------------------------------------------------------- transforms
    def reversed_instance(self):
        """(Q, >=, R, v, u)."""
        return Inst(self.m, list(self.DN), [(b, a) for a, b in self.edges], self.v, self.u, self.names)


def rev_walk(W):
    return list(W)[::-1]
