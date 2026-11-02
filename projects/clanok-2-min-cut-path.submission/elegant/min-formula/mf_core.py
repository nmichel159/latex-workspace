"""Exact smallest formula that separates B_P from A_P, in a free grammar over atoms (Pareto dynamic programme).

Atoms: dn x, Q - up x, S(x) = dn x - [x], T(x) = Q - (up x - [x]), EP(x), FR(x, y), ER(x, y).  A formula is a tree of unions and
intersections of atoms.  Cost = number of element slots of the tree, with multiplicity: dn x, nup x, S x, T x, EP x, FR(x, x), ER(x, x) cost 1
and FR(x, y), ER(x, y) with x != y cost 2.  (The enumeration of the algorithm needs only distinct elements, so the cost of a tree is an upper bound for
the number of distinct elements; `distinct` in the output gives that number for the tree found.)

Every atom is a down-set, so a value is determined for our purpose by the pair (X, Y) = (D cap B, D cap A).  A value (X, Y) dominates (X', Y') if X contains X' and Y
is contained in Y'.  Union and intersection are monotone for this order, so replacing a subformula by a dominating value of no larger cost never hurts,
and the programme keeps only the maximal values for each cost.  It is exact unless `cap` truncates a front (then `exact` is False).

Encoding: key = X | (C << nb), C = complement of Y in A.  Dominance is superset of keys.  Target = all ones.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
sys.path.insert(0, CHECKS)
from zz_core import Inst, bits, popcnt  # noqa: E402,F401
from zz_proof import Walk  # noqa: E402,F401


def maximal(vals):
    """Inclusion-maximal elements of a list of ints."""
    vals = sorted(set(vals), key=popcnt, reverse=True)
    out = []
    for v in vals:
        for w in out:
            if v & ~w == 0:
                break
        else:
            out.append(v)
    return out


class Measure:
    def __init__(self, I, W, strict_atoms=True, ep_atoms=True, pair_atoms=True, restrict=None):
        """restrict: optional iterable of elements allowed in atoms."""
        self.I, self.Wk = I, Walk(I, W)
        self.Bl = list(self.Wk.B)
        self.Al = list(self.Wk.A)
        self.nb, self.na = len(self.Bl), len(self.Al)
        self.fullB = (1 << self.nb) - 1
        self.fullA = (1 << self.na) - 1
        self.target = self.fullB | (self.fullA << self.nb)
        self.elts = list(restrict) if restrict is not None else list(range(I.m))
        self.strict_atoms, self.ep_atoms, self.pair_atoms = strict_atoms, ep_atoms, pair_atoms
        self.atoms = {}  # key -> (cost, descr)
        self._build()

    # ----------------------------------------------------------------- atoms
    def _add(self, key, cost, descr):
        old = self.atoms.get(key)
        if old is None or cost < old[0]:
            self.atoms[key] = (cost, descr)

    def key_of(self, D):
        """Key of a set D (mask over Q)."""
        X = 0
        for i, b in enumerate(self.Bl):
            if D >> b & 1:
                X |= 1 << i
        Y = 0
        for i, a in enumerate(self.Al):
            if D >> a & 1:
                Y |= 1 << i
        return X | ((self.fullA & ~Y) << self.nb)

    def _build(self):
        I = self.I
        T = self.Bl + self.Al
        nb = self.nb
        na = self.na
        fa = self.fullA

        def enc(bitsT):
            """bitsT: int, bit i set if T[i] is in the set."""
            return (bitsT & self.fullB) | ((fa & ~(bitsT >> nb)) << nb)

        # one-element atoms
        for x in self.elts:
            vd = vn = vs = vt = 0
            for i, t in enumerate(T):
                if I.UP[t] >> x & 1:
                    vd |= 1 << i
                if not I.UP[x] >> t & 1:
                    vn |= 1 << i
                if I.USTR[t] >> x & 1:
                    vs |= 1 << i
                if not I.USTR[x] >> t & 1:
                    vt |= 1 << i
            self._add(enc(vd), 1, ("dn", x))
            self._add(enc(vn), 1, ("nup", x))
            if self.strict_atoms:
                self._add(enc(vs), 1, ("S", x))
                self._add(enc(vt), 1, ("T", x))
            if self.ep_atoms:
                g = I.MB[x] | (I.DN[x] & ~I.CL[x])
                ve = 0
                for i, t in enumerate(T):
                    if I.DN[t] & ~g == 0:
                        ve |= 1 << i
                self._add(enc(ve), 1, ("EP", x))
        # two-element atoms, deduplicated on the projected bad sets
        topc = I.CL[I.v]
        botc = I.CL[I.u]
        upT = [I.UP[t] & ~topc for t in T]
        dnT = [I.DN[t] & ~botc for t in T]
        uniF = 0
        for s in upT:
            uniF |= s
        uniE = 0
        for s in dnT:
            uniE |= s
        repF = {}
        repE = {}
        for x in self.elts:
            repF.setdefault((I.MA[x] | I.UP[x]) & uniF, x)
            repE.setdefault((I.MB[x] | I.DN[x]) & uniE, x)
        self.nrepF, self.nrepE = len(repF), len(repE)
        lF = list(repF.items())
        lE = list(repE.items())
        nT = len(T)
        for p, (bx, x) in enumerate(lF):
            for q in range(p, len(lF)):
                if q > p and not self.pair_atoms:
                    break
                by, y = lF[q]
                bad = bx | by
                v = 0
                for i in range(nT):
                    if upT[i] & ~bad:
                        v |= 1 << i
                self._add(enc(v), 1 if p == q else 2, ("FR", x, y))
        for p, (bx, x) in enumerate(lE):
            for q in range(p, len(lE)):
                if q > p and not self.pair_atoms:
                    break
                by, y = lE[q]
                bad = bx | by
                v = 0
                for i in range(nT):
                    if not dnT[i] & ~bad:
                        v |= 1 << i
                self._add(enc(v), 1 if p == q else 2, ("ER", x, y))

    # ----------------------------------------------------------------- helpers
    def split(self, key):
        return key & self.fullB, key >> self.nb

    def fmt(self, tree):
        I = self.I
        if tree[0] in ("dn", "nup", "S", "T", "EP"):
            return "%s(%s)" % (tree[0], I.name(tree[1]))
        if tree[0] in ("FR", "ER"):
            return "%s(%s,%s)" % (tree[0], I.name(tree[1]), I.name(tree[2]))
        return "(" + (" | " if tree[0] == "U" else " & ").join(self.fmt(t) for t in tree[1:]) + ")"

    def leaves(self, tree):
        if tree[0] in ("U", "I"):
            out = []
            for t in tree[1:]:
                out += self.leaves(t)
            return out
        return [tree]

    def distinct(self, tree):
        s = set()
        for lf in self.leaves(tree):
            s.update(lf[1:])
        return len(s)

    # ----------------------------------------------------------------- free grammar
    def free(self, maxcost=14, cap=4000, verbose=False):
        """Least cost of a tree of unions and intersections.  Returns dict(cost, tree, exact, fronts)."""
        byc = {}
        for key, (c, d) in self.atoms.items():
            byc.setdefault(c, []).append(key)
        pred = {key: d for key, (c, d) in self.atoms.items()}
        best = {key: c for key, (c, d) in self.atoms.items()}
        F = {0: []}
        exact = True
        fb, nb = self.fullB, self.nb
        for k in range(1, maxcost + 1):
            cand = set(F[k - 1])
            cand.update(byc.get(k, []))
            for i in range(1, k // 2 + 1):
                Li = F[i]
                Lj = F[k - i]
                for a in Li:
                    xa, ca = a & fb, a >> nb
                    for b in Lj:
                        xb, cb = b & fb, b >> nb
                        u = (xa | xb) | ((ca & cb) << nb)
                        w = (xa & xb) | ((ca | cb) << nb)
                        if u not in best:
                            best[u] = k
                            pred[u] = ("U", a, b)
                            cand.add(u)
                        if w not in best:
                            best[w] = k
                            pred[w] = ("I", a, b)
                            cand.add(w)
                        if u == self.target or w == self.target:
                            return dict(cost=k, tree=self._tree(pred, self.target), exact=exact, fronts={j: len(F[j]) for j in F})
            cl = maximal(list(cand))
            if len(cl) > cap:
                exact = False
                cl = sorted(cl, key=self._score, reverse=True)[:cap]
            F[k] = cl
            if verbose:
                print("  cost", k, "front", len(cl), "exact", exact, flush=True)
            if self.target in cl:
                return dict(cost=k, tree=self._tree(pred, self.target), exact=exact, fronts={j: len(F[j]) for j in F})
        return dict(cost=None, tree=None, exact=exact, fronts={j: len(F[j]) for j in F})

    def _score(self, key):
        x, c = key & self.fullB, key >> self.nb
        return min(popcnt(x) / max(1, self.nb), popcnt(c) / max(1, self.na)) + 0.001 * popcnt(key)

    def _tree(self, pred, key):
        p = pred[key]
        if p[0] in ("U", "I"):
            return (p[0], self._tree(pred, p[1]), self._tree(pred, p[2]))
        return p

    # ----------------------------------------------------------------- restricted forms
    def pure(self, maxcost=20):
        """F = least cost of a union of atoms that miss A; E = least cost of an intersection of atoms that contain B."""
        fb, nb = self.fullB, self.nb
        fa = self.fullA
        Fatoms = {}
        Eatoms = {}
        for key, (c, d) in self.atoms.items():
            x, cc = key & fb, key >> nb
            if cc == fa:
                old = Fatoms.get(x)
                if old is None or c < old[0]:
                    Fatoms[x] = (c, d)
            if x == fb:
                old = Eatoms.get(cc)
                if old is None or c < old[0]:
                    Eatoms[cc] = (c, d)
        rf = self._cover(Fatoms, fb, maxcost)
        re = self._cover(Eatoms, fa, maxcost)
        return rf, re

    @staticmethod
    def _cover(atoms, full, maxcost, cap=20000):
        """Least cost cover of `full` by unions of the sets of `atoms` (dict set -> (cost, descr)).  Pareto DP on subsets."""
        byc = {}
        for s, (c, d) in atoms.items():
            byc.setdefault(c, []).append(s)
        byc = {c: maximal(v) for c, v in byc.items()}
        pred = {}
        F = {0: [0]}
        pred[0] = None
        for k in range(1, maxcost + 1):
            cand = set(F[k - 1])
            for c, L in byc.items():
                if c > k:
                    continue
                for a in F[k - c]:
                    for s in L:
                        v = a | s
                        if v not in pred:
                            pred[v] = (a, atoms[s][1])
                            cand.add(v)
            cl = maximal(list(cand))
            if len(cl) > cap:
                cl = sorted(cl, key=popcnt, reverse=True)[:cap]
            F[k] = cl
            if full in cand:
                sel = []
                v = full
                while pred[v] is not None:
                    v, d = pred[v]
                    sel.append(d)
                return k, sel
        return None, None

    def depth2(self, maxcost=16, cap=4000):
        """Least cost of a union of intersections of atoms (DNF), and of an intersection of unions (CNF, the dual)."""
        return self._dnf(maxcost, cap), self._cnf(maxcost, cap)

    def _dnf(self, maxcost, cap):
        fb, nb, fa = self.fullB, self.nb, self.fullA
        # intersections of atoms: Pareto DP on key; a conjunct is complete when its A-part is empty
        byc = {}
        for key, (c, d) in self.atoms.items():
            byc.setdefault(c, []).append(key)
        byc = {c: maximal(v) for c, v in byc.items()}
        F = {0: [fb | (0 << nb)]}  # empty intersection = Q : X = all, C = none
        pred = {F[0][0]: None}
        conj = {}  # X -> cost
        for k in range(1, maxcost + 1):
            cand = set(F[k - 1])
            for c, L in byc.items():
                if c > k:
                    continue
                for a in F[k - c]:
                    xa, ca = a & fb, a >> nb
                    for s in L:
                        xs, cs = s & fb, s >> nb
                        w = (xa & xs) | ((ca | cs) << nb)
                        if w not in pred:
                            pred[w] = (a, self.atoms[s][1])
                            cand.add(w)
            cl = maximal(list(cand))
            if len(cl) > cap:
                cl = sorted(cl, key=self._score, reverse=True)[:cap]
            F[k] = cl
            for w in cand:
                if w >> nb == fa:
                    x = w & fb
                    if x and (x not in conj or conj[x] > k):
                        conj[x] = k
            # stop early when the cover is reached within k
            atoms = {x: (c0, x) for x, c0 in conj.items()}
            r = self._cover(atoms, fb, k)
            if r[0] is not None:
                return r[0]
        return None

    def _cnf(self, maxcost, cap):
        fb, nb, fa = self.fullB, self.nb, self.fullA
        byc = {}
        for key, (c, d) in self.atoms.items():
            byc.setdefault(c, []).append(key)
        byc = {c: maximal(v) for c, v in byc.items()}
        F = {0: [(fa << nb)]}  # empty union: X = none, C = all
        pred = {F[0][0]: None}
        clause = {}
        for k in range(1, maxcost + 1):
            cand = set(F[k - 1])
            for c, L in byc.items():
                if c > k:
                    continue
                for a in F[k - c]:
                    xa, ca = a & fb, a >> nb
                    for s in L:
                        xs, cs = s & fb, s >> nb
                        w = (xa | xs) | ((ca & cs) << nb)
                        if w not in pred:
                            pred[w] = (a, self.atoms[s][1])
                            cand.add(w)
            cl = maximal(list(cand))
            if len(cl) > cap:
                cl = sorted(cl, key=self._score, reverse=True)[:cap]
            F[k] = cl
            for w in cand:
                if w & fb == fb:
                    cc = w >> nb
                    if cc and (cc not in clause or clause[cc] > k):
                        clause[cc] = k
            atoms = {x: (c0, x) for x, c0 in clause.items()}
            r = self._cover(atoms, fa, k)
            if r[0] is not None:
                return r[0]
        return None
