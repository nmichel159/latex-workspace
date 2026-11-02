"""Hub-free planted instances.  Differences from zz_design: no hub elements, so near highs (near lows) do not meet above (below), and FR(x, x), ER(x, x) are not automatically
atoms of the right type; contacts use private witnesses; highs need not lie above lows.

Core elements carry a word position p = 0..r-1, typ 'E' (high) or 'F' (low), class cls[p].  strict: set of (low class, high class).
mA: set of (e, f), positions: e and f meet above (f in C(e)), through a private witness tied with v.
mB: set of (f, e), positions: e and f meet below (e in C'(f)), through a private witness tied with u.
Links on the walk: E-E through a low filler tied with u, F-F through a high filler tied with v, F-E by a direct edge if strict, otherwise through two fillers.
extra_gap[p] (optional) = number of additional filler pairs between p and p + 1.
Highs at walk distance >= 4 meet above by a private witness (if not tied), lows at walk distance >= 4 meet below by a private witness (if not tied).
Pairs at walk distance 2 meet below (highs) or above (lows) by the walk itself, or get a witness if their link does not give that.
"""
import json
import random

from mf_core import Inst, bits


class Abs:
    def __init__(self, word):
        self.word = list(word)
        self.cls = list(range(len(word)))
        self.strict = set()
        self.mA = set()
        self.mB = set()
        self.left = 1   # low fillers before the first core element: the walk starts u, ...
        self.right = 1

    def copy(self):
        d = Abs(self.word)
        d.cls = list(self.cls)
        d.strict = set(self.strict)
        d.mA = set(self.mA)
        d.mB = set(self.mB)
        d.left, d.right = self.left, self.right
        return d

    def to_json(self):
        return dict(word="".join(self.word), cls=self.cls, strict=sorted(self.strict), mA=sorted(self.mA), mB=sorted(self.mB))

    @staticmethod
    def from_json(o):
        d = Abs(o["word"])
        d.cls = list(o["cls"])
        d.strict = {tuple(x) for x in o["strict"]}
        d.mA = {tuple(x) for x in o["mA"]}
        d.mB = {tuple(x) for x in o["mB"]}
        return d

    def E(self):
        return [p for p in range(len(self.word)) if self.word[p] == "E"]

    def F(self):
        return [p for p in range(len(self.word)) if self.word[p] == "F"]

    def is_strict(self, f, e):
        return (self.cls[f], self.cls[e]) in self.strict

    def tie(self, p, q):
        c1, c2 = self.cls[p], self.cls[q]
        self.cls = [c1 if c == c2 else c for c in self.cls]
        self.strict = {(c1 if x == c2 else x, c1 if y == c2 else y) for x, y in self.strict}

    def repair(self):
        """Every non-strict cross pair gets a contact, chosen at random if missing: keeps P2 in the abstract model."""
        for e in self.E():
            for f in self.F():
                if not self.is_strict(f, e) and (e, f) not in self.mA and (f, e) not in self.mB:
                    return False
        return True

    def build(self):
        names = []
        kind = []

        def new(nm, kd):
            names.append(nm)
            kind.append(kd)
            return len(names) - 1

        u = new("u", "B")
        v = new("v", "T")
        r = len(self.word)
        el = [new("%s%d" % (self.word[p], p), "c") for p in range(r)]
        typ = {el[p]: self.word[p] for p in range(r)}
        typ[u] = "F"
        typ[v] = "E"
        cl = {el[p]: self.cls[p] for p in range(r)}
        edges = set()
        seq = [u]

        def strict_rel(lo, hi):
            if kind[lo] == "B" and kind[hi] != "B":
                return True
            if kind[hi] == "T" and kind[lo] != "T":
                return True
            if kind[lo] == "c" and kind[hi] == "c":
                return (cl[lo], cl[hi]) in self.strict
            return False

        def link(x, y):
            tx, ty = typ[x], typ[y]
            if tx == ty == "E":
                t = new("t%d" % len(names), "B")
                edges.add((t, x))
                edges.add((t, y))
                seq.append(t)
            elif tx == ty == "F":
                s = new("s%d" % len(names), "T")
                edges.add((x, s))
                edges.add((y, s))
                seq.append(s)
            elif tx == "F":
                if strict_rel(x, y):
                    edges.add((x, y))
                else:
                    s = new("s%d" % len(names), "T")
                    t = new("t%d" % len(names), "B")
                    edges.add((x, s))
                    edges.add((t, s))
                    edges.add((t, y))
                    seq.extend([s, t])
            else:
                if strict_rel(y, x):
                    edges.add((y, x))
                else:
                    t = new("t%d" % len(names), "B")
                    s = new("s%d" % len(names), "T")
                    edges.add((t, x))
                    edges.add((t, s))
                    edges.add((y, s))
                    seq.extend([t, s])

        cur = u
        for p in range(r):
            link(cur, el[p])
            seq.append(el[p])
            cur = el[p]
        link(cur, v)
        seq.append(v)
        pos = {x: i for i, x in enumerate(seq)}
        # meets: contacts with private witnesses
        for e, f in self.mA:
            w = new("w%d_%d" % (e, f), "T")
            edges.add((el[e], w))
            edges.add((el[f], w))
        for f, e in self.mB:
            z = new("z%d_%d" % (f, e), "B")
            edges.add((z, el[e]))
            edges.add((z, el[f]))
        # highs and lows
        Es = self.E()
        Fs = self.F()
        for i, p in enumerate(Es):
            for q in Es[i + 1:]:
                if self.cls[p] == self.cls[q]:
                    continue
                dist = abs(pos[el[p]] - pos[el[q]])
                if dist >= 4 or not (set(self._lows_between(seq, pos[el[p]], pos[el[q]], edges, el[p], el[q]))):
                    w = new("wE%d_%d" % (p, q), "T")
                    edges.add((el[p], w))
                    edges.add((el[q], w))
        for i, p in enumerate(Fs):
            for q in Fs[i + 1:]:
                if self.cls[p] == self.cls[q]:
                    continue
                dist = abs(pos[el[p]] - pos[el[q]])
                if dist >= 4 or not (set(self._lows_between(seq, pos[el[p]], pos[el[q]], edges, el[p], el[q]))):
                    z = new("zF%d_%d" % (p, q), "B")
                    edges.add((z, el[p]))
                    edges.add((z, el[q]))
        m = len(names)
        Tm = sum(1 << x for x in range(m) if kind[x] == "T")
        ALL = (1 << m) - 1
        up = [0] * m
        byc = {}
        for x, c in cl.items():
            byc[c] = byc.get(c, 0) | (1 << x)
        above = {}
        for lo, hi in self.strict:
            above[lo] = above.get(lo, 0) | byc.get(hi, 0)
        for x in range(m):
            if kind[x] == "B":
                up[x] = ALL
            elif kind[x] == "T":
                up[x] = Tm
            else:
                up[x] = Tm | byc[cl[x]] | above.get(cl[x], 0)
        I = Inst(m, up, edges, u, v, names)
        I.kind = kind
        I.el = el
        return I, seq

    @staticmethod
    def _lows_between(seq, i, j, edges, x, y):
        """Element between two walk neighbours at distance 2 that gives them a common neighbour by the walk."""
        if abs(i - j) != 2:
            return []
        return [seq[min(i, j) + 1]]


def block(n, k, X, rng=None):
    """E^n F^k: columns < X are marked below in all rows, columns >= X are marked above in all rows."""
    d = Abs("E" * n + "F" * k)
    Es, Fs = d.E(), d.F()
    for i, e in enumerate(Es):
        for j, f in enumerate(Fs):
            if j >= X:
                d.mA.add((e, f))
            else:
                d.mB.add((f, e))
    return d


def rand_abs(rng, r=None, pstrict=0.3, pA=0.5):
    r = r or rng.randint(8, 16)
    word = "".join(rng.choice("EF") for _ in range(r))
    if rng.random() < 0.6:
        n = rng.randint(3, r - 3)
        word = "E" * n + "F" * (r - n)
    d = Abs(word)
    for e in d.E():
        for f in d.F():
            x = rng.random()
            if x < pstrict:
                d.strict.add((d.cls[f], d.cls[e]))
            elif rng.random() < pA:
                d.mA.add((e, f))
            else:
                d.mB.add((f, e))
    return d


def mutate(d, rng):
    """One random change, in place; keeps every cross pair marked or strict."""
    Es, Fs = d.E(), d.F()
    if not Es or not Fs:
        return "none"
    kind = rng.choice(["flip", "flip", "flip", "strict", "unstrict", "addA", "addB", "rmA", "rmB", "tieE", "tieF", "swapword", "line", "line"])
    e, f = rng.choice(Es), rng.choice(Fs)
    if kind == "flip":
        if (e, f) in d.mA:
            d.mA.discard((e, f))
            d.mB.add((f, e))
        elif (f, e) in d.mB:
            d.mB.discard((f, e))
            d.mA.add((e, f))
        else:
            return "none"
    elif kind == "strict":
        if d.is_strict(f, e):
            return "none"
        d.strict.add((d.cls[f], d.cls[e]))
    elif kind == "unstrict":
        if not d.is_strict(f, e):
            return "none"
        d.strict.discard((d.cls[f], d.cls[e]))
        for x in Fs:
            for y in Es:
                if d.cls[x] == d.cls[f] and d.cls[y] == d.cls[e] and (y, x) not in d.mA and (x, y) not in d.mB:
                    if rng.random() < 0.5:
                        d.mA.add((y, x))
                    else:
                        d.mB.add((x, y))
    elif kind == "addA":
        d.mA.add((e, f))
    elif kind == "addB":
        d.mB.add((f, e))
    elif kind == "rmA":
        if (e, f) not in d.mA:
            return "none"
        d.mA.discard((e, f))
        if not d.is_strict(f, e) and (f, e) not in d.mB:
            d.mB.add((f, e))
    elif kind == "rmB":
        if (f, e) not in d.mB:
            return "none"
        d.mB.discard((f, e))
        if not d.is_strict(f, e) and (e, f) not in d.mA:
            d.mA.add((e, f))
    elif kind == "tieE":
        if len(Es) < 2:
            return "none"
        x, y = rng.sample(Es, 2)
        if d.cls[x] == d.cls[y]:
            return "none"
        d.tie(x, y)
        _fix_ties(d)
    elif kind == "tieF":
        if len(Fs) < 2:
            return "none"
        x, y = rng.sample(Fs, 2)
        if d.cls[x] == d.cls[y]:
            return "none"
        d.tie(x, y)
        _fix_ties(d)
    elif kind == "swapword":
        return "none"
    elif kind == "line":
        # a whole row or column changes
        if rng.random() < 0.5:
            t = rng.choice(["A", "B"])
            for g in Fs:
                if d.is_strict(g, e):
                    continue
                d.mA.discard((e, g))
                d.mB.discard((g, e))
                if t == "A":
                    d.mA.add((e, g))
                else:
                    d.mB.add((g, e))
        else:
            t = rng.choice(["A", "B"])
            for g in Es:
                if d.is_strict(f, g):
                    continue
                d.mA.discard((g, f))
                d.mB.discard((f, g))
                if t == "A":
                    d.mA.add((g, f))
                else:
                    d.mB.add((f, g))
    return kind


def _fix_ties(d):
    for e in d.E():
        for f in d.F():
            if not d.is_strict(f, e) and (e, f) not in d.mA and (f, e) not in d.mB:
                d.mA.add((e, f))


def dump_json(d, path, **extra):
    o = d.to_json()
    o.update(extra)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(o, fh)
