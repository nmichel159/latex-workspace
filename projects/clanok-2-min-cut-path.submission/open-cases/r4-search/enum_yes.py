"""Exhaustive search for small portfolio-hard YES-instances of general ZZ + P2 at level 2 (agent r4-search).

Level 2 witness methods: G2 (2-guess both sides), LAT2, GC2 (and H1 on switch-model instances; no switch-model
instance with q <= 13 can defeat G2, see the report, so H1 is not needed here).
Facts used (proved in the report, Section 3.1):
  (a) G2 and LAT2 find a solution iff some solution down-set D lies in the family G of 'guessable' down-sets
      (g_low(D) <= 2 or g_up(D) <= 2, or D a LAT2 set); for a fixed order G does not depend on R.
  (b) For a fixed order, 'no D in G connects u, v in G_D(R)' is closed under removing edges, 'yes-instance' and P2
      are closed under adding edges.
  (c) A yes-instance defeating G2 needs a solution D with >= 3 maximal middle classes in D and >= 3 minimal middle
      classes outside D, hence >= 6 middle classes.
Method: for every preorder with u least, v greatest and m >= 6 middle classes (middle poset up to isomorphism, class
sizes and the sizes of the classes of u and v distributed up to automorphism), branch and bound over the real-edge
set R (include / exclude each strictly comparable pair other than uv) with the pruning rules
  (i) the included edges make some D in G connect -> prune (by (b) every superset is solved by a guess),
 (ii) included + undecided edges make no D outside G connect -> prune,
(iii) included + undecided edges violate P2 -> prune.
Leaves are exactly the P2 yes-instances on which G2 and LAT2 fail.  Each leaf is reduced to its orbit under the
automorphisms of the preorder (kept iff its edge mask is the least in its orbit) and tested with GC2.
Output: counts per q and configuration; instances defeating GC2 too are written to runs/enum-yes-hard-q*.jsonl.
Usage: python enum_yes.py Q [MMIN] [nolat]   (nolat: control run without LAT2, G2 only)"""
import sys
import json
import time
import itertools
import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher
from common import make_zz, to_gc, HERE
import gcert
from posets import posets, downsets_of
from portfolio import Masks, lattice2


def has_dstar(m, below):
    """some down-set S with >= 3 maximal elements and >= 3 minimal elements of the complement."""
    above = [0] * m
    for j in range(m):
        for i in range(m):
            if (below[j] >> i) & 1:
                above[i] |= 1 << j
    for S in downsets_of(m, below):
        mx = sum(1 for j in range(m) if (S >> j) & 1 and not (above[j] & S))
        comp = ((1 << m) - 1) & ~S
        mn = sum(1 for j in range(m) if (comp >> j) & 1 and not (below[j] & comp))
        if mx >= KG + 1 and mn >= KG + 1:
            return True
    return False


def poset_aut(m, below):
    G = nx.DiGraph()
    G.add_nodes_from(range(m))
    for j in range(m):
        for i in range(m):
            if (below[j] >> i) & 1:
                G.add_edge(i, j)
    return [dict(a) for a in DiGraphMatcher(G, G).isomorphisms_iter()]


def size_assignments(m, below, extra):
    """(b, t, sizes) with b + t - 2 + sum(sizes) - m = extra, sizes up to the automorphisms of the poset."""
    auts = poset_aut(m, below)
    out = []
    for b in range(1, extra + 2):
        for t in range(1, extra + 3 - b):
            rest = extra - (b - 1) - (t - 1)
            if rest < 0:
                continue
            seen = set()
            # distribute `rest` extra elements over the m classes
            for combo in itertools.combinations_with_replacement(range(m), rest):
                sizes = [1] * m
                for j in combo:
                    sizes[j] += 1
                key = min(tuple(sizes[a[j]] for j in range(m)) for a in auts)
                if key in seen:
                    continue
                seen.add(key)
                out.append((b, t, tuple(sizes)))
    return out


def build_order(m, below, b, t, sizes):
    """elements: u = 0, other bottoms, middle classes (in poset order), other tops, v = q - 1."""
    q = b + t + sum(sizes)
    cls_of = []
    idx = list(range(b, b + 0))
    elems = []
    for j in range(m):
        for _ in range(sizes[j]):
            elems.append(j)
    le = [[False] * q for _ in range(q)]
    B = list(range(b))
    M = list(range(b, b + len(elems)))
    T = list(range(b + len(elems), q))
    for x in range(q):
        for y in range(q):
            if x in B or y in T:
                le[x][y] = True
    for ix, x in enumerate(M):
        for iy, y in enumerate(M):
            jx, jy = elems[ix], elems[iy]
            if jx == jy or (below[jy] >> jx) & 1:
                le[x][y] = True
    # u = 0, v = q - 1
    return q, le


def order_aut(q, le):
    G = nx.DiGraph()
    G.add_nodes_from(range(q))
    for x in range(q):
        G.nodes[x]["c"] = 1 if x == 0 else (2 if x == q - 1 else 0)
        for y in range(q):
            if x != y and le[x][y]:
                G.add_edge(x, y)
    nm = lambda a, b: a["c"] == b["c"]   # noqa: E731
    return [dict(a) for a in DiGraphMatcher(G, G, node_match=nm).isomorphisms_iter()]


class Order:
    def __init__(self, q, le):
        self.q, self.le = q, le
        self.u, self.v = 0, q - 1
        self.pairs = [(a, b) for a in range(q) for b in range(q)
                      if le[a][b] and not le[b][a] and (a, b) != (0, q - 1)]
        self.P = len(self.pairs)
        self.pidx = {p: i for i, p in enumerate(self.pairs)}
        z0 = make_zz(q, le, [], 0, q - 1)
        import zz as _zz
        self.downs = _zz.downsets(z0)
        M = Masks(make_zz(q, le, self.pairs, 0, q - 1))
        self.M = M
        # cut masks
        self.cut = {}
        for D in self.downs:
            m = 0
            for i, (a, b) in enumerate(self.pairs):
                if (D >> a) & 1 and not (D >> b) & 1:
                    m |= 1 << i
            self.cut[D] = m
        # guessable down-sets: g_low <= 2 or g_up <= 2 (generator counts) or LAT2 sets
        self.lat = self.lat2_sets()
        self.G = []
        self.N = []
        for D in self.downs:
            if self.g_low(D) <= KG or self.g_up(D) <= KG or (USE_LAT and D in self.lat):
                self.G.append(D)
            else:
                self.N.append(D)
        # for pruning rule (i): guessable down-sets cutting each pair
        self.G_of_pair = [[D for D in self.G if (self.cut[D] >> i) & 1] for i in range(self.P)]
        # P2: incomparable pairs and their witness edge pairs
        self.p2req = []
        for x in range(q):
            for y in range(x + 1, q):
                if le[x][y] or le[y][x]:
                    continue
                opts = []
                for w in range(q):
                    if (le[w][x] and not le[x][w] and le[w][y] and not le[y][w]):
                        opts.append((1 << self.pidx[(w, x)]) | (1 << self.pidx[(w, y)]))
                    elif (le[x][w] and not le[w][x] and le[y][w] and not le[w][y]):
                        opts.append((1 << self.pidx[(x, w)]) | (1 << self.pidx[(y, w)]))
                self.p2req.append(opts)

    def g_low(self, D):
        M = self.M
        comp = M.full & ~D
        if comp == M.T:
            return 0
        mins = set()
        for x in range(self.q):
            if (comp >> x) & 1 and (M.down[x] & ~M.cls[x]) & comp == 0:
                mins.add(M.cls[x])
        return len(mins)

    def g_up(self, D):
        M = self.M
        if D == M.B:
            return 0
        maxs = set()
        for x in range(self.q):
            if (D >> x) & 1 and (M.up[x] & ~M.cls[x]) & D == 0:
                maxs.add(M.cls[x])
        return len(maxs)

    def lat2_sets(self):
        M = self.M
        basics = set()
        for a in range(M.n):
            basics.add(M.down[a])
            basics.add(M.down[a] & ~M.cls[a])
            basics.add(M.full & ~M.up[a])
            basics.add(M.full & ~(M.up[a] & ~M.cls[a]))
        basics = sorted(basics)
        cand = set(b for b in basics if M.valid(b))
        for i in range(len(basics)):
            for j in range(i + 1, len(basics)):
                for x in (basics[i] | basics[j], basics[i] & basics[j]):
                    if M.valid(x):
                        cand.add(x)
        return cand

    def connects(self, D, emask):
        m = emask & self.cut[D]
        adj = [0] * self.q
        while m:
            low = m & -m
            i = low.bit_length() - 1
            m ^= low
            a, b = self.pairs[i]
            adj[a] |= 1 << b
            adj[b] |= 1 << a
        reach = 1
        fr = 1
        v = self.v
        while fr:
            nw = 0
            x = fr
            while x:
                low = x & -x
                j = low.bit_length() - 1
                x ^= low
                nw |= adj[j]
            nw &= ~reach
            if (nw >> v) & 1:
                return True
            reach |= nw
            fr = nw
        return False

    def p2_ok(self, emask):
        for opts in self.p2req:
            if not any((emask & o) == o for o in opts):
                return False
        return True


def enumerate_order(O, auts_perm, stats, hard_out, qlabel):
    P = O.P
    full = (1 << P) - 1
    leaves = []

    def rec(i, I, U):
        stats["nodes"] = stats.get("nodes", 0) + 1
        # (ii), (iii) on I | U
        top = I | U
        if not O.p2_ok(top):
            return
        if not any(O.connects(D, top) for D in O.N):
            return
        if i == P:
            leaves.append(I)
            return
        bit = 1 << i
        U2 = U & ~bit
        # include
        ok = True
        I2 = I | bit
        for D in O.G_of_pair[i]:
            if O.connects(D, I2):
                ok = False
                break
        if ok:
            rec(i + 1, I2, U2)
        rec(i + 1, I, U2)

    rec(0, 0, full)
    # orbit reduction
    for R in leaves:
        stats["leaves_labeled"] = stats.get("leaves_labeled", 0) + 1
        canon = True
        for perm in auts_perm:
            R2 = 0
            m = R
            while m:
                low = m & -m
                j = low.bit_length() - 1
                m ^= low
                R2 |= 1 << perm[j]
            if R2 < R:
                canon = False
                break
        if not canon:
            continue
        stats["leaves"] = stats.get("leaves", 0) + 1
        edges = [O.pairs[j] for j in range(P) if (R >> j) & 1]
        z = make_zz(O.q, O.le, edges, 0, O.q - 1)
        c = gcert.certificate(to_gc(z), KG)
        if c is None:
            stats["GC_fail"] = stats.get("GC_fail", 0) + 1
            hard_out.write(json.dumps({"q": O.q, "le": [[int(b) for b in r] for r in O.le], "R": edges,
                                       "label": qlabel}) + "\n")
            hard_out.flush()
        else:
            k = "GC_%s" % c[1]
            stats[k] = stats.get(k, 0) + 1


def pair_perms(O, auts):
    out = []
    for a in auts:
        perm = [O.pidx[(a[x], a[y])] for (x, y) in O.pairs]
        out.append(perm)
    return out


USE_LAT = True
KG = 2


def main():
    """python enum_yes.py Q [MMIN] [nolat]  or  python enum_yes.py Q --m M --range A B --level K --tag TAG"""
    global USE_LAT, KG
    args = sys.argv[1:]
    Q = int(args[0])
    mlist = None
    prange = None
    tag = ""
    if "--level" in args:
        KG = int(args[args.index("--level") + 1])
    if "--m" in args:
        mlist = [int(args[args.index("--m") + 1])]
    if "--range" in args:
        i = args.index("--range")
        prange = (int(args[i + 1]), int(args[i + 2]))
    if "--tag" in args:
        tag = args[args.index("--tag") + 1]
    if "nolat" in args:
        USE_LAT = False
    if mlist is None:
        mmin = int(args[1]) if len(args) > 1 and args[1].isdigit() else 2 * KG + 2
        mlist = list(range(mmin, Q - 1))
    t0 = time.time()
    hard_out = open("%s/runs/enum-yes-hard-q%d%s%s%s.jsonl" % (HERE, Q, "" if USE_LAT else "-nolat",
                                                            "" if KG == 2 else "-L%d" % KG, tag), "w")
    total = {}
    for m in mlist:
        extra = Q - 2 - m
        Ps = [P for P in posets(m) if has_dstar(m, P)]
        print("q=%d m=%d extra=%d level=%d: %d middle posets with D*" % (Q, m, extra, KG, len(Ps)), flush=True)
        lo, hi = (0, len(Ps)) if prange is None else prange
        for pi in range(lo, min(hi, len(Ps))):
            Pz = Ps[pi]
            for (b, t, sizes) in size_assignments(m, Pz, extra):
                q, le = build_order(m, Pz, b, t, sizes)
                assert q == Q
                O = Order(q, le)
                if not O.N:
                    total["orders_no_N"] = total.get("orders_no_N", 0) + 1
                    continue
                total["orders"] = total.get("orders", 0) + 1
                auts = order_aut(q, le)
                st = {}
                enumerate_order(O, pair_perms(O, auts), st, hard_out, "m%d-p%d-b%d-t%d-%s" % (m, pi, b, t, sizes))
                for k, v in st.items():
                    total[k] = total.get(k, 0) + v
            if (pi + 1) % 20 == 0:
                print("  [%.0fs] posets %d/%d totals %s" % (time.time() - t0, pi + 1, len(Ps), total), flush=True)
    print("FINAL q=%d m=%s range=%s level=%d [%.0fs] %s" % (Q, mlist, prange, KG, time.time() - t0, total), flush=True)


if __name__ == "__main__":
    main()
