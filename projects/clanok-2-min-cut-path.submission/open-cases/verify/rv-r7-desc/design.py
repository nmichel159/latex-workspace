"""Referee rv-r7-desc: planted designs.

A design is a path word with classes; the flip side of an E-member a is F_a = {z_g : g in S(a)} + hubF, with z_g a node of the
member at position g; the flip side of an F-member b is E_b = {n_q : q in T(b)} + hubE.  hubF, hubE lie in flip sides only and
give P2 between members of the same type.  Fillers: E-fillers lie in one class TOP above everything, with empty F-side;
F-fillers in one class BOT below everything, with empty E-side.  A contact can also be realized by a middle witness: an
off-path switch w in TOP with E_w = {rho(a,w), rho(b,w)}, or z in BOT with F_z = {rho(z,b), rho(z,a)}.
strict: pairs (class of an F-member, class of an E-member), F-class below E-class.
"""
from swf import Inst


class Design:
    def __init__(self):
        self.word = []          # 'E' / 'F', index = position - 1
        self.role = []          # 'core' or 'fill'
        self.cls = []           # class id
        self.ncls = 0
        self.S = {}             # position of an E-member -> set of positions of F-members
        self.T = {}             # position of an F-member -> set of positions of E-members
        self.strict = set()     # (F class, E class)
        self.wS = set()         # (a pos, b pos): contact a -> b realized by an upper middle witness
        self.wT = set()         # (b pos, a pos): contact b -> a realized by a lower middle witness

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
        return d

    def build(self):
        r = len(self.word)
        names = {}

        def node(x):
            if x not in names:
                names[x] = len(names)
            return 1 << names[x]

        s, t = node("s"), node("t")
        ns, nt = 0, 1
        wits = [("U",) + x for x in sorted(self.wS)] + [("L",) + x for x in sorted(self.wT)]
        m = r + len(wits)
        E = [0] * m
        F = [0] * m
        side = lambda i: E if self.word[i] == "E" else F
        side(0)[0] |= s
        side(r - 1)[r - 1] |= t
        for i in range(r - 1):
            y = node(("y", i))
            side(i)[i] |= y
            side(i + 1)[i + 1] |= y
        hubE, hubF = node("hubE"), node("hubF")
        me = []
        for p, st in self.S.items():
            if self.role[p - 1] == "fill":
                continue
            F[p - 1] |= hubF
            for g in st:
                if (p, g) in self.wS:
                    continue
                z = node(("z", g))
                F[p - 1] |= z
                F[g - 1] |= z
        for p, st in self.T.items():
            if self.role[p - 1] == "fill":
                continue
            E[p - 1] |= hubE
            for q in st:
                if (p, q) in self.wT:
                    continue
                n = node(("n", q))
                E[p - 1] |= n
                E[q - 1] |= n
        wi = r
        top = [i for i in range(r) if self.role[i] == "fill" and self.word[i] == "E"]
        bot = [i for i in range(r) if self.role[i] == "fill" and self.word[i] == "F"]
        for w in wits:
            if w[0] == "U":
                a, b = w[1] - 1, w[2] - 1
                pa, pb = node(("r", a, wi)), node(("r", b, wi))
                F[a] |= pa
                F[b] |= pb
                E[wi] |= pa | pb
                me.append((a, wi, pa.bit_length() - 1))
                me.append((b, wi, pb.bit_length() - 1))
                top.append(wi)
            else:
                b, a = w[1] - 1, w[2] - 1
                pa, pb = node(("r", a, wi)), node(("r", b, wi))
                E[a] |= pa
                E[b] |= pb
                F[wi] |= pa | pb
                me.append((wi, a, pa.bit_length() - 1))
                me.append((wi, b, pb.bit_length() - 1))
                bot.append(wi)
            wi += 1
        topS, botS = set(top), set(bot)
        le = [[False] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if i == j:
                    le[i][j] = True
                elif i in botS or j in topS:
                    # bottom class below everything, top class above everything
                    le[i][j] = not (i in topS and j in topS and False)
                    if i in topS and j not in topS:
                        le[i][j] = False
                    if j in botS and i not in botS:
                        le[i][j] = False
                elif i < r and j < r:
                    ci, cj = self.cls[i], self.cls[j]
                    if ci == cj:
                        le[i][j] = True
                    elif (ci, cj) in self.strict:
                        le[i][j] = True
        I = Inst(m, le, E, F, ns, nt, len(names), me)
        P = [2 * i + (1 if self.word[i] == "F" else 0) for i in range(r)]
        return I, P

    def is_a(self, p):
        return self.word[p - 1] == "E" and self.role[p - 1] == "core"

    def is_b(self, p):
        return self.word[p - 1] == "F" and self.role[p - 1] == "core"

    def members(self):
        A = [p for p in range(1, len(self.word) + 1) if self.is_a(p)]
        B = [p for p in range(1, len(self.word) + 1) if self.is_b(p)]
        return A, B


def zipper(p, q, seed_strict=None, naux=12, buf=6, end=3, contact_a=None):
    """Design reaching Stage 1, Case I.  Layout (left to right):
    A* (naux elements of one auxiliary E-class, never skippable), e_0, buffer, core a_1..a_p (singleton classes), buffer, f_0, buffer,
    zipper x_j v_j y_j (j = 1..q; {x_j, y_j} a class of F-members; v_j in the auxiliary E-class), buffer, f_1, B* (naux F-members, one
    class, never skippable), filler.
    F-contacts: A*, e_0, v_j touch every x_j, y_j; core a_i touch f_0, f_1, every x_j, y_j.
    E-contacts: h_j touch e_0, v_j; f_0, f_1 touch e_0; B* touch every a_i.
    Auxiliary E-members lie above all F-members; f_0, f_1, B* lie below all E-members.
    After E_{h_j} the member v_j is a dead end (both neighbours x_j, y_j conflict), and no other flip is usable, so P is the only
    valid path.  seed_strict(i, j): pair a_i > h_j strict.  contact_a(i, j): a_i touches h_j (default all)."""
    d = Design()
    d.fill("F", 2)
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
        v = d.add("E", cls=auxc)
        y = d.add("F", cls=d.cls[x - 1])
        H.append((x, y))
        Vs.append(v)
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
    for (x, y), v in zip(H, Vs):
        d.T[x] = {e0, v}
        d.T[y] = {e0, v}
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
