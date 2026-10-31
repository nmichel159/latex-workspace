"""Library of agent r5-hard (round 6): instance builder in general switch form and analysis of shortest valid paths.

Builder `Inst`: named nodes and switches, sides as Python sets, a strict order given by generating pairs (y < x),
middle edges y - x (y < x) with a private node in F_y and E_x.  `build()` returns a gcore.Gen (r5-core, read-only
import) whose order is the reflexive-transitive closure of the generating pairs.

Analysis `analyse(G)`: number of solutions (enumeration of down-sets), all shortest valid paths, and for each of them
the skeleton (A, B, N_E, N_F), the bad pairs of r5-core.md Section 6.4, their vertex cover, the LP cover numbers by
the cheap tools of Corollary 6.5' (gstar.cover_numbers), and the member-star costs used by Proposition M of
r5-hard.md (catches of F#_a in B for a in A, of E#_b in A for b in B).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
for _d in ("r5-core",):
    _p = os.path.join(OC, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gcore                                   # noqa: E402  (r5-core, read-only)
from gcore import Gen, bits, popcount, closure_le   # noqa: E402
import gstar                                   # noqa: E402
from gstar import Stars, Skel                  # noqa: E402


class Inst:
    def __init__(self):
        self.nodes = {}
        self.sw = {}
        self.swnames = []
        self.E = []
        self.F = []
        self.lt = set()
        self.medge = {}

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def switch(self, name):
        if name not in self.sw:
            self.sw[name] = len(self.swnames)
            self.swnames.append(name)
            self.E.append(set())
            self.F.append(set())
        return self.sw[name]

    def addE(self, w, nodename):
        self.E[self.switch(w)].add(self.node(nodename))

    def addF(self, w, nodename):
        self.F[self.switch(w)].add(self.node(nodename))

    def less(self, y, x):
        self.lt.add((self.switch(y), self.switch(x)))

    def edge(self, y, x):
        """middle edge y - x with y < x (the relation is added too)"""
        self.less(y, x)
        z = self.node(("med", y, x))
        self.F[self.switch(y)].add(z)
        self.E[self.switch(x)].add(z)
        self.medge[z] = (self.switch(y), self.switch(x))

    def build(self, s="s", t="t"):
        m = len(self.swnames)
        le = [[a == b for b in range(m)] for a in range(m)]
        for (a, b) in self.lt:
            le[a][b] = True
        le = closure_le(le)
        for a in range(m):
            for b in range(m):
                if a != b and le[a][b] and le[b][a]:
                    raise ValueError("tie created: %s %s" % (self.swnames[a], self.swnames[b]))
        N = len(self.nodes)
        Em = [sum(1 << x for x in e) for e in self.E]
        Fm = [sum(1 << x for x in f) for f in self.F]
        return Gen(N, Em, Fm, le, self.nodes[s], self.nodes[t], medge=self.medge, names=list(self.swnames))


def side_name(G, i):
    return ("E" if not i & 1 else "F") + str(G.names[i >> 1] if G.names else i >> 1)


def member_star_costs(G, S, K):
    """For a in A: catches of F#_a in B (Proposition M); for b in B: catches of E#_b in A."""
    ca = {a: popcount(S.NFstar[a] & K.B & ~(1 << a)) for a in bits(K.A)}
    cb = {b: popcount(S.NEstar[b] & K.A & ~(1 << b)) for b in bits(K.B)}
    return ca, cb


def tca_m(G, S, K, dist=9):
    """Least cost of Proposition M: min over pairs a1, a2 in A with |pos| difference >= dist of
    |B & (NF(F#a1) | NF(F#a2))| and dually for B; also the all-anchor options (A or B within an interval of
    length < dist: cost 0 with |A| resp. |B| anchors).  Returns (costF, costE)."""
    pos = K.pos
    res = []
    for kind in (1, 0):
        mem = bits(K.A) if kind == 1 else bits(K.B)
        best = None
        ps = [pos[w] for w in mem]
        if ps and max(ps) - min(ps) < dist:
            best = 0
        for i, a1 in enumerate(mem):
            for a2 in mem[i + 1:]:
                if abs(pos[a1] - pos[a2]) < dist:
                    continue
                if kind == 1:
                    c = popcount((S.NFstar[a1] | S.NFstar[a2]) & K.B)
                else:
                    c = popcount((S.NEstar[a1] | S.NEstar[a2]) & K.A)
                if best is None or c < best:
                    best = c
        res.append(best)
    return tuple(res)


def describe_M(G, S, K, a1, a2, kind=1):
    """The description of Proposition M (kind 1: F-description with tools F#a1, F#a2, E-anchors up(a1), up(a2),
    flips B & U'; kind 0 dually).  Returns the down-set D."""
    full = (1 << G.m) - 1
    if kind == 1:
        U = S.NFstar[a1] | S.NFstar[a2]
        Sx = G.up[a1] | G.up[a2]
        fnon = sum(1 << w for w in range(G.m) if G.F[w])
        gen = (fnon & ~U & ~Sx) | (K.B & U)
        D = 0
        for w in bits(gen):
            D |= G.dn[w]
        return D
    U = S.NEstar[a1] | S.NEstar[a2]
    Sx = G.dn[a1] | G.dn[a2]
    enon = sum(1 << w for w in range(G.m) if G.E[w])
    gen = (enon & ~U & ~Sx) | (K.A & U)
    up = 0
    for w in bits(gen):
        up |= G.up[w]
    return full & ~up


def analyse(G, maxpaths=50, lp=True, verbose=True, out=print):
    sols = G.brute() if G.m <= 26 else None
    length, P0 = G.shortest()
    paths = G.all_shortest(limit=maxpaths, length=length) if length else []
    S = Stars(G)
    rep = dict(m=G.m, N=G.N, p2bad=len(G.p2_bad()), nsol=None if sols is None else len(sols), length=length,
               npaths=len(paths), paths=[])
    for P in paths:
        K = Skel(G, P)
        _, cls = gstar.classify(G, P, S, K)
        bad = cls["bad"]
        vc = gstar.min_vertex_cover_bip(bad) if bad else 0
        tau = gstar.cover_numbers(G, P, S, K) if lp else (None, None)
        ca, cb = member_star_costs(G, S, K)
        tm = tca_m(G, S, K)
        pr = dict(path=[side_name(G, i) for i in P], A=popcount(K.A), B=popcount(K.B), NE=popcount(K.NE),
                  NF=popcount(K.NF), bad=len(bad), vc=vc, tauE=tau[0], tauF=tau[1],
                  incomp_fail=len(cls["incomp_fail"]), tcaF=tm[0], tcaE=tm[1],
                  catchF=sorted(ca.values()), catchE=sorted(cb.values()))
        rep["paths"].append(pr)
    if verbose:
        out("m=%d N=%d P2-violations=%d solutions=%s shortest=%s #shortest=%d" %
            (rep["m"], rep["N"], rep["p2bad"], rep["nsol"], rep["length"], rep["npaths"]))
        for pr in rep["paths"][:3]:
            out("  path " + " ".join(pr["path"]))
            out("    |A|=%d |B|=%d |NE|=%d |NF|=%d bad=%d vc=%d tauE=%s tauF=%s incomp_fail=%d" %
                (pr["A"], pr["B"], pr["NE"], pr["NF"], pr["bad"], pr["vc"], pr["tauE"], pr["tauF"],
                 pr["incomp_fail"]))
            out("    Prop. M cost: F-kind %s, E-kind %s; catches F#a: %s; catches E#b: %s" %
                (pr["tcaF"], pr["tcaE"], pr["catchF"], pr["catchE"]))
    return rep
