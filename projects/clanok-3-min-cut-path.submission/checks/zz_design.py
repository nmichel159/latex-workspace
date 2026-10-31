"""Planted direct ZZ instances that reach Stage 1 and the Shapes of thm:pa-formulas.

The layouts adapt the designs of open-cases/verify/rv-r7-desc/design.py and run_planted.py from the switch form to the direct form:
- 'E' members are highs of the walk, 'F' members are lows; E-fillers are tied with v, F-fillers are tied with u;
- a contact "b in S(a)" is a top element w_b, tied with v, with the edges b w_b and a w_b;
- a contact "a in T(b)" is a bottom element t_a, tied with u, with the edges t_a a and t_a b;
- the hub top element lies above all core highs (they meet above), the hub bottom element below all core lows (they meet below);
- consecutive members of the walk are joined by a filler (same type), by a direct edge (strict low < high) or by two fillers.
Core highs are pairwise incomparable unless tied, core lows likewise, and `strict` lists pairs (low class, high class).
"""
from zz_core import Inst


class Design:
    def __init__(self):
        self.word = []
        self.role = []
        self.cls = []
        self.ncls = 0
        self.S = {}
        self.T = {}
        self.strict = set()
        self.wS = set()
        self.wT = set()

    def add(self, typ, cls=None):
        if cls is None:
            cls = self.ncls
            self.ncls += 1
        self.word.append(typ)
        self.role.append("core")
        self.cls.append(cls)
        if typ == "E":
            self.S[len(self.word)] = set()
        else:
            self.T[len(self.word)] = set()
        return len(self.word)

    def fill(self, typ, k=1):
        for _ in range(k):
            self.word.append(typ)
            self.role.append("fill")
            self.cls.append(-1 if typ == "E" else -2)
        return len(self.word)

    def tie(self, p, q):
        c1, c2 = self.cls[p - 1], self.cls[q - 1]
        self.cls = [c1 if c == c2 else c for c in self.cls]
        self.strict = {(c1 if x == c2 else x, c1 if y == c2 else y) for x, y in self.strict}

    def set_strict(self, b, a):
        self.strict.add((self.cls[b - 1], self.cls[a - 1]))

    def unset_strict(self, b, a):
        self.strict.discard((self.cls[b - 1], self.cls[a - 1]))

    def is_strict(self, b, a):
        return (self.cls[b - 1], self.cls[a - 1]) in self.strict

    def copy(self):
        d = Design()
        d.word, d.role, d.cls = list(self.word), list(self.role), list(self.cls)
        d.ncls = self.ncls
        d.S = {k: set(v) for k, v in self.S.items()}
        d.T = {k: set(v) for k, v in self.T.items()}
        d.strict = set(self.strict)
        d.wS, d.wT = set(self.wS), set(self.wT)
        d.info = getattr(self, "info", {})
        return d

    def build(self):
        names = []
        kind = []     # 'B' bottom class, 'T' top class, 'c' core

        def new(nm, kd):
            names.append(nm)
            kind.append(kd)
            return len(names) - 1

        u = new("u", "B")
        v = new("v", "T")
        r = len(self.word)
        el = {}
        for p in range(1, r + 1):
            if self.role[p - 1] == "core":
                el[p] = new("%s%d" % (self.word[p - 1], p), "c")
            elif self.word[p - 1] == "E":
                el[p] = new("fE%d" % p, "T")
            else:
                el[p] = new("fF%d" % p, "B")
        typ = {el[p]: self.word[p - 1] for p in el}
        typ[u] = "F"
        typ[v] = "E"
        cl = {el[p]: self.cls[p - 1] for p in el if self.role[p - 1] == "core"}

        def strict_rel(lo, hi):
            kl, kh = kind[lo], kind[hi]
            if kl == "B" and kh != "B":
                return True
            if kh == "T" and kl != "T":
                return True
            if kl == "c" and kh == "c":
                return (cl[lo], cl[hi]) in self.strict
            return False

        edges = set()
        seq = [u]
        lab = ["L"]

        def link(x, y):
            tx, ty = typ[x], typ[y]
            if tx == ty == "E":
                t = new("t%d" % len(names), "B")
                edges.add((t, x))
                edges.add((t, y))
                seq.append(t)
                lab.append("L")
            elif tx == ty == "F":
                s = new("s%d" % len(names), "T")
                edges.add((x, s))
                edges.add((y, s))
                seq.append(s)
                lab.append("H")
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
                    lab.extend(["H", "L"])
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
                    lab.extend(["L", "H"])

        cur = u
        for p in range(1, r + 1):
            link(cur, el[p])
            seq.append(el[p])
            lab.append("H" if self.word[p - 1] == "E" else "L")
            cur = el[p]
        link(cur, v)
        seq.append(v)
        lab.append("H")

        tophub = new("hubT", "T")
        bothub = new("hubB", "B")
        wtop = {}
        tbot = {}
        for p, st in self.S.items():
            if self.role[p - 1] == "fill":
                continue
            a = el[p]
            edges.add((a, tophub))
            for g in st:
                b = el[g]
                if (p, g) in self.wS:
                    w = new("w%d_%d" % (p, g), "T")
                    edges.add((a, w))
                    edges.add((b, w))
                else:
                    if g not in wtop:
                        wtop[g] = new("w%d" % g, "T")
                        edges.add((b, wtop[g]))
                    edges.add((a, wtop[g]))
        for p, st in self.T.items():
            if self.role[p - 1] == "fill":
                continue
            b = el[p]
            edges.add((bothub, b))
            for q in st:
                a = el[q]
                if (p, q) in self.wT:
                    t = new("z%d_%d" % (p, q), "B")
                    edges.add((t, a))
                    edges.add((t, b))
                else:
                    if q not in tbot:
                        tbot[q] = new("t%d" % q, "B")
                        edges.add((tbot[q], a))
                    edges.add((tbot[q], b))
        m = len(names)
        Tm = sum(1 << x for x in range(m) if kind[x] == "T")
        ALL = (1 << m) - 1
        up = [0] * m
        byc = {}
        for x, c in cl.items():
            byc.setdefault(c, 0)
            byc[c] |= 1 << x
        above = {}
        for lo, hi in self.strict:
            above.setdefault(lo, 0)
            above[lo] |= byc.get(hi, 0)
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


def zipper(p, q, seed_strict=None, naux=6, buf=3, end=2, contact_a=None):
    """Layout: A* (naux tied highs), e_0, buffer, core a_1..a_p, buffer, f_0, buffer, zipper x_j v_j y_j (x_j, y_j tied lows, v_j in the class of
    A*), buffer, f_1, B* (naux tied lows).  S: A*, e_0, v_j touch all x_j, y_j; a_i touch f_0, f_1, all x_j, y_j.  T: x_j, y_j touch e_0, v_j; f_0,
    f_1 touch e_0; B* touch all a_i.  A*, e_0, v_j are above all lows; f_0, f_1, B* are below all a_i."""
    d = Design()
    d.fill("F", 1)
    aux = d.add("E")
    Astar = [aux] + [d.add("E", cls=d.cls[aux - 1]) for _ in range(naux - 1)]
    auxc = d.cls[aux - 1]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", buf)
    Apos = [d.add("E") for _ in range(p)]
    d.fill("F", buf)
    f0 = d.add("F")
    d.fill("E", buf)
    H, Vs = [], []
    for j in range(q):
        x = d.add("F")
        vj = d.add("E", cls=auxc)
        y = d.add("F", cls=d.cls[x - 1])
        H.append((x, y))
        Vs.append(vj)
    d.fill("E", buf)
    f1 = d.add("F")
    b0 = d.add("F")
    Bstar = [b0] + [d.add("F", cls=d.cls[b0 - 1]) for _ in range(naux - 1)]
    d.fill("F", end)
    hpos = [z for pr in H for z in pr]
    for a in Astar + Vs + [e0]:
        d.S[a] = set(hpos)
    for i, a in enumerate(Apos):
        st = {f0, f1}
        for j, (x, y) in enumerate(H):
            if contact_a is None or contact_a(i, j):
                st |= {x, y}
        d.S[a] = st
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Apos)
    for (x, y), vj in zip(H, Vs):
        d.T[x] = {e0, vj}
        d.T[y] = {e0, vj}
    allb = [f0, f1] + hpos + Bstar
    for b in allb:
        for a in Astar + [e0]:
            d.set_strict(b, a)
    for a in Apos:
        for b in [f0, f1] + Bstar:
            d.set_strict(b, a)
    if seed_strict is not None:
        for i, a in enumerate(Apos):
            for j, (x, y) in enumerate(H):
                if seed_strict(i, j):
                    d.set_strict(x, a)
    d.info = {"Apos": Apos, "H": H, "Vs": Vs, "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    return d


def base_B(rng):
    return zipper(rng.randint(10, 20), rng.randint(12, 24))


def base_A(rng):
    p, q = rng.randint(10, 20), rng.randint(8, 24)
    k = rng.randint(1, 9)
    nonstrict = set(rng.sample(range(q), min(k, q)))
    cut = rng.randint(8, p)
    return zipper(p, q, seed_strict=lambda i, j: i < cut and j not in nonstrict,
                  contact_a=(None if rng.random() < 0.5 else (lambda i, j: not (i < cut and j not in nonstrict))))


def base_stair(rng):
    p, q = rng.randint(10, 20), rng.randint(12, 24)
    sigma = [rng.randint(0, p // 2) if rng.random() < 0.8 else rng.randint(0, p - 1) for _ in range(q)]
    d = zipper(p, q, seed_strict=lambda i, j: i < sigma[j])
    Apos = d.info["Apos"]
    for j, (x, y) in enumerate(d.info["H"]):
        for z in (x, y):
            d.T[z].add(Apos[sigma[j]])
    return d


def base_ties(rng):
    d = base_stair(rng) if rng.random() < 0.5 else base_B(rng)
    Apos = d.info["Apos"]
    H = d.info["H"]
    for _ in range(rng.randint(1, max(1, len(Apos) // 3))):
        x, y = rng.sample(Apos, 2)
        d.tie(x, y)
    for _ in range(rng.randint(1, max(1, len(H) // 4))):
        (x, _a), (y, _b) = rng.sample(H, 2)
        d.tie(x, y)
    return d


def base_small(rng):
    return zipper(rng.randint(7, 10), rng.randint(9, 20))


def base_mix(rng):
    """R_0 and C_0 positions interleaved: each a has a member left of f_0 and a member in a zone M; each h has members x', x'' around its member of
    M, then x, v, y further right."""
    p, q = rng.randint(10, 14), rng.randint(12, 18)
    naux, buf = 6, 3
    d = Design()
    d.fill("F", 1)
    aux = d.add("E")
    Astar = [aux] + [d.add("E", cls=d.cls[aux - 1]) for _ in range(naux - 1)]
    auxc = d.cls[aux - 1]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", buf)
    Apos = [d.add("E") for _ in range(p)]
    d.fill("F", buf)
    f0 = d.add("F")
    d.fill("E", buf)
    x1s = {}
    M_a = {}
    n_mid = min(p, q)
    perm = list(range(p))
    rng.shuffle(perm)
    for k in range(n_mid):
        x1 = d.add("F")
        am = d.add("E", cls=d.cls[Apos[perm[k]] - 1])
        x2 = d.add("F", cls=d.cls[x1 - 1])
        x1s[k] = (x1, x2)
        M_a[k] = am
    d.fill("E", buf)
    H, Vs = [], []
    for j in range(q):
        if j < n_mid:
            x = d.add("F", cls=d.cls[x1s[j][0] - 1])
        else:
            x = d.add("F")
        vj = d.add("E", cls=auxc)
        y = d.add("F", cls=d.cls[x - 1])
        H.append((x, y))
        Vs.append(vj)
    d.fill("E", buf)
    f1 = d.add("F")
    b0 = d.add("F")
    Bstar = [b0] + [d.add("F", cls=d.cls[b0 - 1]) for _ in range(naux - 1)]
    d.fill("F", 2)
    allh = [z for pr in H for z in pr] + [z for pr in x1s.values() for z in pr]
    Aall = Apos + list(M_a.values())
    for a in Astar + Vs + [e0]:
        d.S[a] = set(allh)
    for a in Aall:
        d.S[a] = {f0, f1} | set(allh)
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Aall)
    for j, (x, y) in enumerate(H):
        d.T[x] = {e0, Vs[j]}
        d.T[y] = {e0, Vs[j]}
        if j in x1s:
            d.T[x1s[j][0]] = {e0, Vs[j], M_a[j]}
            d.T[x1s[j][1]] = {e0, Vs[j], M_a[j]}
            d.T[x] |= {M_a[j]}
            d.T[y] |= {M_a[j]}
    allb = [f0, f1] + allh + Bstar
    for b in allb:
        for a in Astar + [e0]:
            d.set_strict(b, a)
    for a in Apos:
        for b in [f0, f1] + Bstar:
            d.set_strict(b, a)
    d.info = {"Apos": Aall, "H": H + list(x1s.values()), "Vs": Vs, "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    return d


def base_cross(rng):
    """Classes a_k = {a^L_k, a^Z_k} touched completely by h_k: a^L_k early in the left zone, a^Z_k sandwiched between two members of h_k in a zone M;
    singletons c_i right of all a^L_k form kappa.  One pair (h_i, h_j) keeps a_i, a_j; only the second pair of Shape B removes them."""
    n, mc, q0 = rng.randint(10, 14), rng.randint(10, 14), rng.randint(4, 8)
    naux, buf = 6, 3
    d = Design()
    d.fill("F", 1)
    aux = d.add("E")
    Astar = [aux] + [d.add("E", cls=d.cls[aux - 1]) for _ in range(naux - 1)]
    auxc = d.cls[aux - 1]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", buf)
    aL = [d.add("E") for _ in range(n)]
    cs = [d.add("E") for _ in range(mc)]
    d.fill("F", buf)
    f0 = d.add("F")
    d.fill("E", buf)
    aZ, xs = [], []
    for k in range(n):
        x1 = d.add("F")
        am = d.add("E", cls=d.cls[aL[k] - 1])
        x2 = d.add("F", cls=d.cls[x1 - 1])
        aZ.append(am)
        xs.append((x1, x2))
    d.fill("E", buf)
    H, Vs = [], []
    for j in range(n + q0):
        x = d.add("F") if j >= n else d.add("F", cls=d.cls[xs[j][0] - 1])
        vj = d.add("E", cls=auxc)
        y = d.add("F", cls=d.cls[x - 1])
        H.append((x, y))
        Vs.append(vj)
    d.fill("E", buf)
    f1 = d.add("F")
    b0 = d.add("F")
    Bstar = [b0] + [d.add("F", cls=d.cls[b0 - 1]) for _ in range(naux - 1)]
    d.fill("F", 2)
    allh = [z for pr in H for z in pr] + [z for pr in xs for z in pr]
    Aall = aL + cs + aZ
    for a in Astar + Vs + [e0]:
        d.S[a] = set(allh)
    for a in Aall:
        d.S[a] = {f0, f1} | set(allh)
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Aall)
    for j, (x, y) in enumerate(H):
        d.T[x] = {e0, Vs[j]}
        d.T[y] = {e0, Vs[j]}
        if j < n:
            for z in (x, y, xs[j][0], xs[j][1]):
                d.T[z] = {e0, Vs[j], aL[j], aZ[j]}
            for i in range(j):
                d.set_strict(x, aL[i])
    allb = [f0, f1] + allh + Bstar
    for b in allb:
        for a in Astar + [e0]:
            d.set_strict(b, a)
    for a in aL + cs:
        for b in [f0, f1] + Bstar:
            d.set_strict(b, a)
    d.info = {"Apos": Aall, "H": H + xs, "Vs": Vs, "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    return d


def base_allstrict(rng):
    """Tie-free walk: core a left, core h right, every pair strict."""
    p, q, naux = rng.randint(12, 20), rng.randint(12, 20), 6
    d = Design()
    d.fill("F", 1)
    Astar = [d.add("E") for _ in range(naux)]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", 3)
    Apos = [d.add("E") for _ in range(p)]
    d.fill("F", 3)
    f0 = d.add("F")
    d.fill("E", 3)
    es = d.add("E")
    d.fill("E", 3)
    Hs = [d.add("F") for _ in range(q)]
    d.fill("E", 3)
    f1 = d.add("F")
    Bstar = [d.add("F") for _ in range(naux)]
    d.fill("F", 2)
    for a in Astar + [e0, es]:
        d.S[a] = set(Hs)
    for a in Apos:
        d.S[a] = {f0, f1} | set(Hs)
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Apos)
    for b in Hs:
        d.T[b] = {e0, es}
    allb = [f0, f1] + Hs + Bstar
    for b in allb:
        for a in Astar + [e0, es] + Apos:
            d.set_strict(b, a)
    d.info = {"Apos": Apos, "H": [(b, b) for b in Hs], "Vs": [], "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    return d


def base_local(rng):
    """Alternating core highs and lows, all pairs strict; hill climbing with contacts between near positions makes the detour lemmas tight."""
    n = rng.randint(24, 60)
    d = Design()
    E, F = [], []
    for i in range(n):
        if i % 2 == 0:
            E.append(d.add("E"))
        else:
            F.append(d.add("F"))
    for a in E:
        for b in F:
            d.set_strict(b, a)
    d.info = {"Apos": E, "H": [(b, b) for b in F], "Vs": [], "local": True}
    return d


def near_move(d, rng):
    """Contacts between positions at word distance at most W, with or without removing the strict pair."""
    Apos = d.info["Apos"]
    Bpos = [z for pr in d.info["H"] for z in pr]
    W = rng.choice([2, 3, 4, 5, 6, 7, 9, 11])
    a = rng.choice(Apos)
    near = [b for b in Bpos if 0 < abs(a - b) <= W]
    if not near:
        return "none"
    b = rng.choice(near)
    kind = rng.choice(["contS", "contT", "un", "un", "tieA", "tieB"])
    if kind == "contS":
        d.S[a].add(b)
    elif kind == "contT":
        d.T[b].add(a)
    elif kind == "un":
        if not d.is_strict(b, a):
            return "none"
        d.unset_strict(b, a)
        bs = [p for p in Bpos if d.cls[p - 1] == d.cls[b - 1]]
        aa = [p for p in Apos if d.cls[p - 1] == d.cls[a - 1]]
        for x in bs:
            for y in aa:
                if rng.random() < 0.5:
                    d.S[y].add(x)
                else:
                    d.T[x].add(y)
    elif kind == "tieA":
        o = [p for p in Apos if 0 < abs(p - a) <= W]
        if not o:
            return "none"
        d.tie(a, rng.choice(o))
    else:
        o = [p for p in Bpos if 0 < abs(p - b) <= W]
        if not o:
            return "none"
        d.tie(b, rng.choice(o))
    return "near " + kind


def base_kappa(rng):
    """All classes of the zipper touch the first class of R_0 from below; only the term up A_kappa of Shape B removes it."""
    p, q = rng.randint(10, 18), rng.randint(10, 20)
    s = 3
    d = zipper(p, q, seed_strict=lambda i, j: i < s)
    Apos = d.info["Apos"]
    for (x, y) in d.info["H"]:
        d.T[x].add(Apos[s])
        d.T[y].add(Apos[s])
    return d


def base_margin2(rng):
    """Mutation test of the margin: a_1, f, a_2, h, a_3, g in consecutive positions.  With margin 2, R_0 = {a_2} and h lies in C_0 although no position of h
    exceeds tau*; with the margin of the text this instance leaves Stage 0 at an exit."""
    naux = 6
    d = Design()
    d.fill("F", 1)
    aux = d.add("E")
    Astar = [aux] + [d.add("E", cls=d.cls[aux - 1]) for _ in range(naux - 1)]
    d.fill("F", 1)
    a1 = d.add("E")
    f = d.add("F")
    a2 = d.add("E")
    h = d.add("F")
    a3 = d.add("E")
    g = d.add("F")
    b0 = d.add("F")
    Bstar = [b0] + [d.add("F", cls=d.cls[b0 - 1]) for _ in range(naux - 1)]
    d.fill("F", 1)
    highs = Astar + [a1, a2, a3]
    lows = [f, h, g] + Bstar
    for a in highs:
        for b in lows:
            d.set_strict(b, a)
        d.S[a] = {f, h, g}
    for b in Bstar:
        d.T[b] = {a1, a2, a3}
    d.T[h] = {a1, a3}
    d.info = {"Apos": [a1, a2, a3], "H": [(h, h), (f, f), (g, g)], "Vs": [], "Astar": Astar, "Bstar": Bstar}
    return d


def base_far2(rng):
    """Mutation test of the far pairs: two adjacent highs g_1, g_2 with empty contacts come first in the sorts by l and by r."""
    d0 = base_allstrict(rng)
    d = Design()
    d.fill("F", 1)
    g1 = d.add("E")
    g2 = d.add("E")
    shift = len(d.word)
    d.word += d0.word
    d.role += d0.role
    base = d.ncls
    d.cls += [c + base if c >= 0 else c for c in d0.cls]
    d.ncls = base + d0.ncls
    for k, st in d0.S.items():
        d.S[k + shift] = {x + shift for x in st}
    for k, st in d0.T.items():
        d.T[k + shift] = {x + shift for x in st}
    d.strict = {(x + base, y + base) for x, y in d0.strict}
    for p in range(1, len(d.word) + 1):
        if d.word[p - 1] == "F" and d.role[p - 1] == "core":
            d.set_strict(p, g1)
            d.set_strict(p, g2)
    info = d0.info
    d.info = {"Apos": [x + shift for x in info["Apos"]], "H": [(x + shift, y + shift) for x, y in info["H"]], "Vs": [], "g": (g1, g2)}
    return d


BASES = {"B": base_B, "A": base_A, "stair": base_stair, "ties": base_ties, "small": base_small, "mix": base_mix, "cross": base_cross, "allstrict": base_allstrict,
         "local": base_local, "kappa": base_kappa, "margin2": base_margin2, "far2": base_far2}
