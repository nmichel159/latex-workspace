"""Proposition X (iii) and Theorem Y (iii) of r4-general.md: lower bounds for the neighbourhood generators of
Theorem NG, by exhaustive search over small triples on the ZZ form of the families (own builders, families.py).

ZZ form of a switch-form instance (own conversion): every node n becomes a bottom b_n and a top t_n with the edge
b_n t_n, the bottom of node s is u and the top of node t is v; E_w -> edges b_n w, F_w -> edges w t_n; the order on
the switches as given; bottoms ~ u, tops ~ v.

NG (peak side): G = (Gamma + N^-(Pi)) - down(Y + {u}), D = Q - up(G + {v}).
Valley side (dual): G' = (Gamma' + N^+(Pi')) - up(Y' + {v}), D' = down(G' + {u}).
A triple succeeds iff its down-set contains a solution; the families have a unique solution D*, and the bottoms are
always in D, the tops never (when G is non-empty), so success iff D restricted to the switches equals D*.
Usage: python ng_check.py LMAX KMAX"""
import itertools
import sys
from families import xfam, yfam


class ZZForm:
    def __init__(self, G, intended):
        N, m = G.N, G.m
        # element ids: switches 0..m-1, bottoms m..m+N-1, tops m+N..m+2N-1
        self.m, self.N = m, N
        self.q = m + 2 * N
        bot = lambda n: m + n
        top = lambda n: m + N + n
        self.u, self.v = bot(G.s), top(G.t)
        q = self.q
        up = [0] * q
        down = [0] * q
        allbot = sum(1 << bot(n) for n in range(N))
        alltop = sum(1 << top(n) for n in range(N))
        for w in range(m):
            up[w] = alltop | sum(1 << z for z in range(m) if G.le[w][z])
            down[w] = allbot | sum(1 << z for z in range(m) if G.le[z][w])
        for n in range(N):
            up[bot(n)] = (1 << q) - 1
            down[bot(n)] = allbot
            up[top(n)] = alltop
            down[top(n)] = (1 << q) - 1
        self.up, self.down = up, down
        self.lower_nb = [0] * q   # R-neighbours strictly below
        self.upper_nb = [0] * q
        for n in range(N):
            self.upper_nb[bot(n)] |= 1 << top(n)
            self.lower_nb[top(n)] |= 1 << bot(n)
        for w in range(m):
            for n in range(N):
                if (G.E[w] >> n) & 1:
                    self.lower_nb[w] |= 1 << bot(n)
                    self.upper_nb[bot(n)] |= 1 << w
                if (G.F[w] >> n) & 1:
                    self.upper_nb[w] |= 1 << top(n)
                    self.lower_nb[top(n)] |= 1 << w
        self.Dstar = sum(1 << w for w in range(m) if intended[G.names[w]] == 1)
        self.swmask = (1 << m) - 1
        # N^-(x) for a single pin x: elements with an R-neighbour x strictly above them = lower_nb[x]
        self.allmask = (1 << q) - 1

    def upc(self, S):
        o = 0
        for x in range(self.q):
            if (S >> x) & 1:
                o |= self.up[x]
        return o

    def downc(self, S):
        o = 0
        for x in range(self.q):
            if (S >> x) & 1:
                o |= self.down[x]
        return o

    def peak_ok(self, Gam, Pi, Y):
        Nm = 0
        for x in Pi:
            Nm |= self.lower_nb[x]
        G0 = sum(1 << x for x in Gam) | Nm
        G = G0 & ~self.downc(sum(1 << y for y in Y) | (1 << self.u))
        D = self.allmask & ~self.upc(G | (1 << self.v))
        return (D & self.swmask) == self.Dstar and G != 0

    def valley_ok(self, Gam, Pi, Y):
        Np = 0
        for x in Pi:
            Np |= self.upper_nb[x]
        G0 = sum(1 << x for x in Gam) | Np
        G = G0 & ~self.upc(sum(1 << y for y in Y) | (1 << self.v))
        D = self.downc(G | (1 << self.u))
        return (D & self.swmask) == self.Dstar and not (D >> self.v) & 1

    def peak_ok_freeY(self, Gam, Pi):
        """Best Y (= D*, see the header of the report): success iff every switch outside D* is above an element of
        (Gamma + N^-(Pi)) outside D*."""
        Nm = 0
        for x in Pi:
            Nm |= self.lower_nb[x]
        G0 = (sum(1 << x for x in Gam) | Nm) & ~(self.downc(self.Dstar) | self.down[self.u])
        D = self.allmask & ~self.upc(G0 | (1 << self.v))
        return (D & self.swmask) == self.Dstar and G0 != 0

    def valley_ok_freeY(self, Gam, Pi):
        Np = 0
        for x in Pi:
            Np |= self.upper_nb[x]
        notD = self.swmask & ~self.Dstar
        G0 = (sum(1 << x for x in Gam) | Np) & ~(self.upc(notD) | self.up[self.v])
        D = self.downc(G0 | (1 << self.u))
        return (D & self.swmask) == self.Dstar and not (D >> self.v) & 1


def min_triple(Z, budget, with_Y=True):
    """Least total size of a successful triple (peak or valley side) up to `budget`; None if none."""
    els = list(range(Z.q))
    for size in range(0, budget + 1):
        for a in range(size + 1):
            for b in range(size - a + 1):
                c = size - a - b
                if not with_Y and c:
                    continue
                for Gam in itertools.combinations(els, a):
                    for Pi in itertools.combinations(els, b):
                        if with_Y:
                            for Y in itertools.combinations(els, c):
                                if Z.peak_ok(Gam, Pi, Y) or Z.valley_ok(Gam, Pi, Y):
                                    return size, (Gam, Pi, Y)
                        else:
                            if Z.peak_ok_freeY(Gam, Pi) or Z.valley_ok_freeY(Gam, Pi):
                                return size, (Gam, Pi)
    return None


def main():
    LMAX, KMAX = int(sys.argv[1]), int(sys.argv[2])
    for L in range(2, LMAX + 1):
        G, it = xfam(L)
        Z = ZZForm(G, it)
        bound = L // 2
        r = min_triple(Z, bound - 1)
        print("X_%d: q = %d; claimed bound |Gamma|+|Pi|+|Y| >= %d; successful triple of size <= %d: %s" % (
            L, Z.q, bound, bound - 1, r))
        sys.stdout.flush()
    for k in range(2, KMAX + 1):
        for contact in (False, True):
            G, it = yfam(k, contact)
            Z = ZZForm(G, it)
            bound = (k + 1) // 2
            r = min_triple(Z, bound - 1, with_Y=False)
            r2 = min_triple(Z, bound + 1, with_Y=False)
            print("%s_%d: q = %d; claimed bound |Gamma|+|Pi| >= %d (Y free); below the bound: %s; least found: %s" % (
                "Y'" if contact else "Y", k, Z.q, bound, r, r2[0] if r2 else None))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
