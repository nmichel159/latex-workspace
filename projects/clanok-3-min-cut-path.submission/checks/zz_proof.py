"""The construction of thm:pa-formulas, step by step as the proof states it, with every claim asserted.

check_lemmas(): lem:pa-basic, lem:pa-one, lem:pa-two (with the detour walks of the proofs built and tested under def:zz-valid),
lem:pa-atoms.  construct(): small sets, Stage 0, ranges, Orientation, property (star), Positions of C_0, Stage 1, Shapes A and B,
and the final condition L_P subset D subset Q minus U_P for the value of the formula of def:pa-atoms.
Cfg holds the constants of the text; run_mut.py lowers them to confirm that the harness detects errors.
"""
from bisect import bisect_left

from zz_core import INF, ClaimFail, bits, chk, popcnt


class Cfg:
    def __init__(self, **kw):
        self.margin = 6          # margin of eq:pa-ranges-r, eq:pa-ranges-c
        self.first = 4           # the far pair is taken among the first `first` elements of a sort (distance >= 2(first - 1))
        self.use_Akappa = True   # the term up A_kappa of Shape B
        self.use_EP = True       # the term with EP of F^1
        self.use_second_pair = True  # the pair h_3, h_4 of Shape B
        self.shape_a_max = 7     # Shape A if |C_1| <= shape_a_max
        self.far_a = 6           # distance of a_1 and a_2: 6 means kappa_1 and kappa_4
        self.atom_far = 6        # distance of the far pairs in the test of lem:pa-atoms
        self.one_bound = 4       # the bound of lem:pa-one
        self.two_bound = 8       # the bound of lem:pa-two
        self.lemma_caps = dict(one_walks=60, two_pairs=250, two_walks=25, atom_pairs=120)
        self.star_cap = 600
        self.check_lemmas = True
        self.__dict__.update(kw)


class Walk:
    """A valid walk, with the objects of Section sec:pa-detours."""

    def __init__(self, I, W):
        self.I, self.W = I, list(W)
        self.q = len(W) - 1
        self.labels = I.label_of(W)
        chk(I.is_valid_walk(self.W, self.labels), "P is not a valid walk")
        self.pos = {}
        self.highs = 0
        self.lows = 0
        for i, x in enumerate(self.W):
            chk(x not in self.pos, "lem:zz-valid(d): repeated element on a shortest walk")
            self.pos[x] = i
            if self.labels[i] == "H":
                self.highs |= 1 << x
            else:
                self.lows |= 1 << x
        chk(self.highs & self.lows == 0, "element both high and low")
        self.U = I.up(self.highs)
        self.L = I.dn(self.lows)
        chk(self.U & self.L == 0, "lem:zz-valid(a): U_P and L_P disjoint")
        self.A = [h for h in bits(self.highs) if I.DSTR[h] & self.highs == 0]
        self.B = [l for l in bits(self.lows) if I.USTR[l] & self.lows == 0]
        self.Am = sum(1 << a for a in self.A)
        self.Bm = sum(1 << b for b in self.B)
        parity_h = {self.pos[h] % 2 for h in bits(self.highs)}
        parity_l = {self.pos[l] % 2 for l in bits(self.lows)}
        chk(len(parity_h) == 1 and len(parity_l) == 1 and parity_h != parity_l, "parity of the positions")

    def Pos(self, w):
        mask = self.highs if self.highs >> w & 1 else self.lows
        return sorted(self.pos[x] for x in bits(self.I.CL[w] & mask))

    def C(self, a):
        return self.Bm & self.I.MA[a]

    def Cp(self, b):
        return self.Am & self.I.MB[b]

    def Ptn(self, mask):
        return sorted(self.pos[x] for x in bits(mask))


def lowest_witness(I, x, y):
    """z with zx, zy in R."""
    w = I.LO[x] & I.LO[y]
    chk(w, "no lower witness")
    return (w & -w).bit_length() - 1


def highest_witness(I, x, y):
    w = I.HI[x] & I.HI[y]
    chk(w, "no upper witness")
    return (w & -w).bit_length() - 1


def rand_witness(rng, mask):
    return rng.choice(list(bits(mask)))


def detour_one_a(w, p, pp, x, rng):
    """The walk of the proof of lem:pa-one(a)."""
    I = w.I
    a, ap = w.W[p], w.W[pp]
    z = rand_witness(rng, I.LO[a] & I.LO[x])
    zp = rand_witness(rng, I.LO[ap] & I.LO[x])
    W = w.W[:p + 1] + [z, x, zp] + w.W[pp:]
    labels = w.labels[:p + 1] + ["L", "H", "L"] + w.labels[pp:]
    return W, labels


def detour_one_b(w, p, pp, y, rng):
    """The walk of the dual lem:pa-one(b)."""
    I = w.I
    b, bp = w.W[p], w.W[pp]
    z = rand_witness(rng, I.HI[b] & I.HI[y])
    zp = rand_witness(rng, I.HI[bp] & I.HI[y])
    W = w.W[:p + 1] + [z, y, zp] + w.W[pp:]
    labels = w.labels[:p + 1] + ["H", "L", "H"] + w.labels[pp:]
    return W, labels


def detour_two(w, a, h, p1, p2, p3, p4, rng):
    """The walk of the proof of lem:pa-two."""
    I = w.I
    x2, x3 = w.W[p2], w.W[p3]
    a2_at_p2 = bool(w.Am >> x2 & 1 and I.MB[h] >> x2 & 1 and w.Bm >> x3 & 1 and I.MA[a] >> x3 & 1)
    a1 = w.W[p1]
    b2 = w.W[p4]
    if a2_at_p2:
        a2, b1 = x2, x3
        Wm = w.W[p2:p3 + 1]
        Lm = w.labels[p2:p3 + 1]
    else:
        a2, b1 = x3, x2
        Wm = w.W[p2:p3 + 1][::-1]
        Lm = w.labels[p2:p3 + 1][::-1]
    z1 = rand_witness(rng, I.LO[a1] & I.LO[h])
    z2 = rand_witness(rng, I.LO[a2] & I.LO[h])
    w1 = rand_witness(rng, I.HI[b1] & I.HI[a])
    w2 = rand_witness(rng, I.HI[b2] & I.HI[a])
    W = w.W[:p1 + 1] + [z1, h, z2] + Wm + [w1, a, w2] + w.W[p4:]
    labels = w.labels[:p1 + 1] + ["L", "H", "L"] + Lm + ["H", "L", "H"] + w.labels[p4:]
    return W, labels


def check_lemmas(w, cfg, rng, st):
    I = w.I
    caps = cfg.lemma_caps
    # lem:pa-basic
    chk(w.U == I.up(w.Am), "lem:pa-basic(a) U_P")
    chk(w.L == I.dn(w.Bm), "lem:pa-basic(a) L_P")
    for a in w.A:
        for e in bits(I.DN[a] & w.highs):
            chk(I.tied(e, a) and w.Am >> e & 1, "lem:pa-basic(b) highs")
    for b in w.B:
        for f in bits(I.UP[b] & w.lows):
            chk(I.tied(f, b) and w.Bm >> f & 1, "lem:pa-basic(b) lows")

    # lem:pa-one
    budget = caps["one_walks"]
    Q = list(range(I.m))
    rng.shuffle(Q)
    for x in Q:
        Ax = sorted(w.pos[a] for a in bits(w.Am & I.MB[x]))
        lows_above = sorted(w.pos[f] for f in bits(w.lows & I.UP[x]))
        if not w.L >> x & 1:
            if Ax:
                chk(Ax[-1] - Ax[0] <= 4, "lem:pa-one(c) distance, A")
                chk(len(Ax) <= 3, "lem:pa-one(c) count, A")
                st["one(c) A tested"] += 1
                st["one(c) A max size %d" % len(Ax)] += 1
        for i in range(len(Ax)):
            for j in range(i + 1, len(Ax)):
                p, pp = Ax[i], Ax[j]
                # the hypothesis: no low at a position outside (p, pp) is >= x
                ok = all(p < t < pp for t in lows_above)
                if ok:
                    chk(pp - p <= cfg.one_bound, "lem:pa-one(a): distance")
                    st["one(a) tested"] += 1
                    st["one(a) max span"] = max(st["one(a) max span"], pp - p)
                    if budget > 0:
                        budget -= 1
                        W, lb = detour_one_a(w, p, pp, x, rng)
                        chk(I.is_valid_walk(W, lb), "lem:pa-one(a): the walk of the proof is not valid")
                        chk(len(W) - 1 >= w.q, "lem:pa-one(a): shorter valid walk")
                        st["one(a) walks built"] += 1
        By = sorted(w.pos[b] for b in bits(w.Bm & I.MA[x]))
        highs_below = sorted(w.pos[e] for e in bits(w.highs & I.DN[x]))
        if not w.U >> x & 1:
            if By:
                chk(By[-1] - By[0] <= 4, "lem:pa-one(c) distance, B")
                chk(len(By) <= 3, "lem:pa-one(c) count, B")
                st["one(c) B tested"] += 1
        for i in range(len(By)):
            for j in range(i + 1, len(By)):
                p, pp = By[i], By[j]
                ok = all(p < t < pp for t in highs_below)
                if ok:
                    chk(pp - p <= cfg.one_bound, "lem:pa-one(b): distance")
                    st["one(b) tested"] += 1
                    st["one(b) max span"] = max(st["one(b) max span"], pp - p)
                    if budget > 0:
                        budget -= 1
                        W, lb = detour_one_b(w, p, pp, x, rng)
                        chk(I.is_valid_walk(W, lb), "lem:pa-one(b): the walk of the proof is not valid")
                        chk(len(W) - 1 >= w.q, "lem:pa-one(b): shorter valid walk")
                        st["one(b) walks built"] += 1

    # lem:pa-two: p_1 = min, p_4 = max are the worst case; all pairs (alpha, beta) are tested.
    pairs = [(a, h) for a in w.A for h in w.B if not I.leq(h, a)]
    rng.shuffle(pairs)
    walks = caps["two_walks"]
    for a, h in pairs[:caps["two_pairs"]]:
        XA = w.Ptn(w.Am & I.MB[h])
        XB = w.Ptn(w.Bm & I.MA[a])
        if not XA or not XB:
            continue
        Z = sorted(set(w.Pos(a)) | set(w.Pos(h)))
        p1, p4 = XA[0], XB[-1]
        if not (p1 < Z[0] and Z[-1] < p4):
            continue
        for al in XA:
            for be in XB:
                p2, p3 = min(al, be), max(al, be)
                if not (p1 < p2 and p3 < p4):
                    continue
                i = bisect_left(Z, p2)
                if i < len(Z) and Z[i] <= p3:
                    continue
                s = (p2 - p1) + (p4 - p3)
                chk(s <= cfg.two_bound, "lem:pa-two: bound")
                st["two tested"] += 1
                st["two max sum"] = max(st["two max sum"], s)
                if s == 8:
                    st["two tight"] += 1
                if walks > 0:
                    walks -= 1
                    W, lb = detour_two(w, a, h, p1, p2, p3, p4, rng)
                    chk(I.is_valid_walk(W, lb), "lem:pa-two: the walk of the proof is not valid")
                    chk(len(W) - 1 == p1 + 4 + (p3 - p2) + 4 + (w.q - p4), "lem:pa-two: length formula")
                    chk(len(W) - 1 >= w.q, "lem:pa-two: shorter valid walk")
                    st["two walks built"] += 1

    # lem:pa-atoms
    A = sorted(w.A, key=lambda x: w.pos[x])
    B = sorted(w.B, key=lambda x: w.pos[x])
    for _ in range(caps["atom_pairs"]):
        if len(A) >= 2:
            a1, a2 = rng.sample(A, 2)
            if abs(w.pos[a1] - w.pos[a2]) >= cfg.atom_far:
                D = I.FR(a1, a2)
                chk(D & w.U == 0, "lem:pa-atoms(a): FR meets U_P")
                chk(w.Bm & ~(w.C(a1) | w.C(a2)) & ~D == 0, "lem:pa-atoms(a): FR misses an element of B_P")
                st["atoms(a) tested"] += 1
        if len(B) >= 2:
            b1, b2 = rng.sample(B, 2)
            if abs(w.pos[b1] - w.pos[b2]) >= cfg.atom_far:
                D = I.ER(b1, b2)
                chk(w.L & ~D == 0, "lem:pa-atoms(b): ER misses L_P")
                chk(D & w.Am & ~(w.Cp(b1) | w.Cp(b2)) == 0, "lem:pa-atoms(b): ER meets A_P")
                st["atoms(b) tested"] += 1
    for a in A[:60]:
        D = I.EP(a)
        for b in w.B:
            if I.lt(b, a):
                chk(D >> b & 1, "lem:pa-atoms(c): EP misses b < a")
        win = w.Am & I.MB[a]
        chk(D & w.Am & ~win == 0, "lem:pa-atoms(c): EP meets A_P outside win")
        chk(popcnt(win) <= 3, "lem:pa-atoms(c): |win| <= 3")
        st["atoms(c) tested"] += 1


def mask_of(it):
    r = 0
    for x in it:
        r |= 1 << x
    return r


class Stage0:
    """Stage 0 for a walk w with the position map of w.  Orders may be given (corresponding tie-breaks after a reversal)."""

    def __init__(self, w, cfg, rng, orders=None):
        self.w = w
        I = w.I
        p = w.pos
        k = cfg.first
        S = {a: w.Ptn(w.C(a)) for a in w.A}
        T = {b: w.Ptn(w.Cp(b)) for b in w.B}
        self.l = {a: (S[a][0] if S[a] else INF) for a in w.A}
        self.r = {a: (S[a][-1] if S[a] else -INF) for a in w.A}
        self.s = {b: (T[b][0] if T[b] else INF) for b in w.B}
        self.t = {b: (T[b][-1] if T[b] else -INF) for b in w.B}
        if orders is None:
            A, B = list(w.A), list(w.B)
            rng.shuffle(A)
            rng.shuffle(B)
            ol = sorted(A, key=lambda a: -self.l[a])
            or_ = sorted(A, key=lambda a: self.r[a])
            os_ = sorted(B, key=lambda b: -self.s[b])
            ot = sorted(B, key=lambda b: self.t[b])
        else:
            ol, or_, os_, ot = orders
            # the given orders must be legal for the current values
            for o, f in ((ol, lambda a: -self.l[a]), (or_, lambda a: self.r[a]), (os_, lambda b: -self.s[b]), (ot, lambda b: self.t[b])):
                vals = [f(x) for x in o]
                chk(vals == sorted(vals), "reversal: the corresponding order is not a legal order")
        self.ol, self.or_, self.os_, self.ot = ol, or_, os_, ot
        self.ls = self.l[ol[k - 1]]
        self.rs = self.r[or_[k - 1]]
        self.ss = self.s[os_[k - 1]]
        self.ts = self.t[ot[k - 1]]

        def ext(lst):
            q = sorted(lst[:k], key=lambda x: p[x])
            return q[0], q[-1]

        self.pl = ext(ol)
        self.pr = ext(or_)
        self.ps = ext(os_)
        self.pt = ext(ot)
        for pr_ in (self.pl, self.pr, self.ps, self.pt):
            chk(abs(p[pr_[0]] - p[pr_[1]]) >= 2 * (k - 1), "Stage 0: first and last of the first elements are far")
        self.FRl = I.FR(*self.pl)
        self.FRr = I.FR(*self.pr)
        self.ERs = I.ER(*self.ps)
        self.ERt = I.ER(*self.pt)
        # the claims made right after each definition
        for a in self.pl:
            for t in S[a]:
                chk(t >= self.ls, "Stage 0: positions of S are >= l*")
        for a in self.pr:
            for t in S[a]:
                chk(t <= self.rs, "Stage 0: positions of S are <= r*")
        for b in self.ps:
            for t in T[b]:
                chk(t >= self.ss, "Stage 0: positions of T are >= sigma*")
        for b in self.pt:
            for t in T[b]:
                chk(t <= self.ts, "Stage 0: positions of T are <= tau*")
        chk(self.FRl & w.U == 0 and self.FRr & w.U == 0, "Stage 0: FR_l, FR_r miss U_P")
        chk(w.L & ~self.ERs == 0 and w.L & ~self.ERt == 0, "Stage 0: ER_s, ER_t contain L_P")
        for b in w.B:
            if p[b] < self.ls:
                chk(self.FRl >> b & 1, "Stage 0: FR_l contains pos(b) < l*")
            if p[b] > self.rs:
                chk(self.FRr >> b & 1, "Stage 0: FR_r contains pos(b) > r*")
        for a in w.A:
            if p[a] < self.ss:
                chk(not self.ERs >> a & 1, "Stage 0: ER_s misses pos(a) < sigma*")
            if p[a] > self.ts:
                chk(not self.ERt >> a & 1, "Stage 0: ER_t misses pos(a) > tau*")
        marg = list(range(0, cfg.margin, 2))
        E0 = set(ol[:k - 1]) | set(or_[:k - 1])
        posE = {self.ss + i for i in marg} | {self.ts - i for i in marg}
        for a in w.A:
            if p[a] in posE:
                E0.add(a)
        H0 = set(os_[:k - 1]) | set(ot[:k - 1])
        posH = {self.ls + i for i in marg} | {self.rs - i for i in marg}
        for b in w.B:
            if p[b] in posH:
                H0.add(b)
        chk(len(E0) <= 12 or cfg.margin > 6 or k > 4, "|E_0| <= 12")
        chk(len(H0) <= 12 or cfg.margin > 6 or k > 4, "|H_0| <= 12")
        self.E0, self.H0 = E0, H0
        self.E0m, self.H0m = mask_of(E0), mask_of(H0)
        self.Fs = self.FRl | self.FRr | I.dn(self.H0m)
        self.Es = (self.ERs & self.ERt) & ~I.up(self.E0m)
        chk(I.is_downset(self.Fs), "F* down-set")
        chk(I.is_downset(self.Es), "E* down-set")
        chk(self.Fs & w.U == 0, "F* misses U_P")
        chk(w.L & ~self.Es == 0, "E* contains L_P")
        self.R0 = w.Am & self.Es
        self.C0 = w.Bm & ~self.Fs


def final(w, D, label, st):
    I = w.I
    chk(I.is_downset(D), label + ": D not a down-set")
    chk(w.L & ~D == 0, label + ": L_P not inside D")
    chk(D & w.U == 0, label + ": D meets U_P")
    chk(D >> I.u & 1 and not D >> I.v & 1, label + ": u, v")
    chk(I.connected_in_GD(D), label + ": u, v not connected in G_D")
    st["final: " + label] += 1


def star_test(w, S0, R0, C0, cfg, rng, st):
    """Property (star) for all or a sample of the pairs (a, h)."""
    I = w.I
    Rl, Cl = list(bits(R0)), list(bits(C0))
    pairs = [(a, h) for a in Rl for h in Cl if not I.leq(h, a)]
    rng.shuffle(pairs)
    n = 0
    for a, h in pairs[:cfg.star_cap]:
        Z = sorted(set(w.Pos(a)) | set(w.Pos(h)))
        Zs = set(Z)
        al = w.Ptn(R0 & w.Cp(h))
        be = w.Ptn(C0 & w.C(a))
        if not al or not be:
            continue
        gaps = {bisect_left(Z, x) for x in al if x not in Zs}
        for y in be:
            if y not in Zs:
                chk(bisect_left(Z, y) not in gaps, "(star): an interval misses Pos[a] and Pos[h]")
        n += len(al) * len(be)
        # quadruples in which the interval between alpha and beta holds exactly one element of Pos[a] and Pos[h]: (star) holds without slack
        for x in al[:30]:
            for y in be[:30]:
                lo, hi = min(x, y), max(x, y)
                if bisect_left(Z, hi + 1) - bisect_left(Z, lo) == 1:
                    st["(star) quadruples without slack (sample)"] += 1
    st["(star) quadruples"] += n
    st["(star) pairs tested"] += min(len(pairs), cfg.star_cap)


def classes_of(w, mask):
    """The classes of a set of elements that is closed under ties within its type; list of masks."""
    I = w.I
    out = []
    rest = mask
    while rest:
        x = (rest & -rest).bit_length() - 1
        c = I.CL[x] & (w.highs if w.highs >> x & 1 else w.lows)
        chk(c & ~mask == 0, "class not closed")
        out.append(c)
        rest &= ~c
    return out


def last_pos(w, c):
    return max(w.pos[x] for x in bits(c))


def construct(w, cfg, rng, st):
    """Runs the proof of thm:pa-formulas on the shortest valid walk of w.  Returns the name of the exit."""
    I = w.I
    if cfg.check_lemmas:
        check_lemmas(w, cfg, rng, st)
    st["walks"] += 1
    st["max m"] = max(st["max m"], I.m)
    st["max q"] = max(st["max q"], w.q)
    # small sets
    exitn = None
    if len(w.A) <= 3:
        D = I.E_formula([], mask_of(w.A))
        chk(D == I.ALL & ~w.U, "small A: value")
        final(w, D, "small A", st)
        exitn = "small A"
    if len(w.B) <= 3:
        D = I.F_formula([], mask_of(w.B), 0)
        chk(D == w.L, "small B: value")
        final(w, D, "small B", st)
        exitn = "small B"
    if exitn:
        return exitn
    st["|A|, |B| >= 4"] += 1

    S0 = Stage0(w, cfg, rng)
    exitn = None
    if S0.C0 == 0:
        D = I.F_formula([S0.pl, S0.pr, None], S0.H0m, 0)
        chk(D == S0.Fs, "F* formula value")
        final(w, D, "C_0 empty, F*", st)
        exitn = "C0 empty"
    if S0.R0 == 0:
        D = I.E_formula([S0.ps, S0.pt], S0.E0m)
        chk(D == S0.Es, "E* formula value")
        final(w, D, "R_0 empty, E*", st)
        exitn = "R0 empty"
    if exitn:
        return exitn
    st["R_0, C_0 nonempty"] += 1
    chk(S0.ls < INF and S0.rs > -INF and S0.ss < INF and S0.ts > -INF, "thresholds are positions")
    for t in (S0.ss, S0.ts):
        chk(0 <= t <= w.q and w.highs >> w.W[t] & 1, "sigma*, tau* are positions of highs")
    for t in (S0.ls, S0.rs):
        chk(0 <= t <= w.q and w.lows >> w.W[t] & 1, "l*, r* are positions of lows")

    def check_ranges(w_, s):
        m = cfg.margin
        for a in bits(s.R0):
            for e in bits(I.CL[a] & w_.highs):
                chk(s.R0 >> e & 1, "class of R_0 is closed")
            for t in w_.Pos(a):
                chk(s.ss + m <= t <= s.ts - m, "eq:pa-ranges-r: position")
            chk(s.l[a] <= s.ls, "eq:pa-ranges-r: l(a) <= l*")
            chk(s.r[a] >= s.rs, "eq:pa-ranges-r: r(a) >= r*")
            chk(-INF < s.l[a] < INF and -INF < s.r[a] < INF, "finite l, r")
        for h in bits(s.C0):
            for f in bits(I.CL[h] & w_.lows):
                chk(s.C0 >> f & 1, "class of C_0 is closed")
            for t in w_.Pos(h):
                chk(s.ls + m <= t <= s.rs - m, "eq:pa-ranges-c: position")
            chk(s.s[h] <= s.ss, "eq:pa-ranges-c: sigma(h) <= sigma*")
            chk(s.t[h] >= s.ts, "eq:pa-ranges-c: tau(h) >= tau*")
            chk(-INF < s.s[h] < INF and -INF < s.t[h] < INF, "finite sigma, tau")
        chk(s.ts - s.ss >= 2 * m and s.rs - s.ls >= 2 * m, "tau* - sigma*, r* - l* large")

    check_ranges(w, S0)

    # Orientation
    chk(S0.ss != S0.ls and S0.ts != S0.rs, "thresholds differ by type")
    if S0.ss < S0.ls and S0.rs < S0.ts:
        raise ClaimFail("Orientation: the case sigma* < l*, r* < tau* occurred")
    if S0.ls < S0.ss and S0.ts < S0.rs:
        raise ClaimFail("Orientation: the case l* < sigma*, tau* < r* occurred")
    if S0.ls < S0.ss and S0.rs < S0.ts:
        st["orientation: reversed"] += 1
        w2 = Walk(I, w.W[::-1])
        chk(w2.U == w.U and w2.L == w.L and w2.Am == w.Am and w2.Bm == w.Bm, "reversal: same sets")
        q = w.q
        S2 = Stage0(w2, cfg, rng, orders=(S0.or_, S0.ol, S0.ot, S0.os_))
        chk(S2.E0 == S0.E0 and S2.H0 == S0.H0, "reversal: E_0, H_0 stay the same")
        chk(S2.Fs == S0.Fs and S2.Es == S0.Es and S2.R0 == S0.R0 and S2.C0 == S0.C0, "reversal: F*, E*, R_0, C_0 stay the same")
        chk((S2.ls, S2.rs, S2.ss, S2.ts) == (q - S0.rs, q - S0.ls, q - S0.ts, q - S0.ss), "reversal: thresholds")
        chk(S2.ss < S2.ls and S2.ts < S2.rs, "reversal: the new values have the fourth orientation")
        check_ranges(w2, S2)
        w, S0 = w2, S2
    else:
        st["orientation: direct"] += 1
    chk(S0.ss < S0.ls and S0.ts < S0.rs, "fourth orientation")
    if cfg.check_lemmas:
        star_test(w, S0, S0.R0, S0.C0, cfg, rng, st)

    # Positions of C_0
    for h in bits(S0.C0):
        chk(any(t > S0.ts for t in w.Pos(h)), "Positions of C_0: no position > tau*")
        chk(all(t > S0.ss for t in w.Pos(h)), "Positions of C_0: positions > sigma*")

    # Stage 1
    Rcl = sorted(classes_of(w, S0.R0), key=lambda c: last_pos(w, c))
    Ccl = classes_of(w, S0.C0)
    lasts = [last_pos(w, c) for c in Rcl]
    chk(len(set(lasts)) == len(lasts), "distinct last positions")
    if len(Rcl) <= 4:
        Ak = [rng.choice(list(bits(c))) for c in Rcl]
        D = I.E_formula([S0.ps, S0.pt], S0.E0m | mask_of(Ak))
        chk(D == S0.Es & ~I.up(mask_of(Ak)), "at most four classes: value")
        final(w, D, "R_0 has at most 4 classes", st)
        return "few classes"
    st["R_0 has at least 5 classes"] += 1
    kap = Rcl[:4]
    ps = last_pos(w, kap[3])
    chk(ps <= S0.ts - cfg.margin, "p* <= tau* - 6")
    for c in Rcl[:4]:
        chk(last_pos(w, c) <= ps, "kappa has no position in the tail")
    for c in Rcl[4:]:
        chk(last_pos(w, c) > ps, "the other classes have their last position in the tail")
    for c in Ccl:
        chk(any(w.pos[x] > ps for x in bits(c)), "every class of C_0 has a position in the tail")
    Ak = [rng.choice(list(bits(c))) for c in kap]
    a1 = w.W[last_pos(w, kap[0])]
    a2 = w.W[last_pos(w, kap[3])]
    chk(abs(w.pos[a1] - w.pos[a2]) >= 6, "a_1, a_2 at distance >= 6")
    Sp = (w.Am & I.MB[a1]) | (w.Am & I.MB[a2])
    chk(popcnt(Sp) <= 6, "|S'| <= 6")
    FRa = I.FR(a1, a2)
    last_term = (I.EP(a1) | I.EP(a2)) & ~I.up(Sp)
    F1 = S0.Fs | FRa | (last_term if cfg.use_EP else 0)
    chk(I.is_downset(F1), "F^1 down-set")
    chk(F1 & w.U == 0, "F^1 misses U_P")
    C1 = [c for c in Ccl if c & ~F1]
    for c in C1:
        chk(c & F1 == 0, "the elements of a class of C_1 lie outside F^1")
        for g in bits(c):
            chk((w.C(a1) | w.C(a2)) >> g & 1, "g in C(a_1) or C(a_2)")
            chk(not I.leq(g, a1) and not I.leq(g, a2), "eq:pa-not-below")
    st["C_1 max"] = max(st["C_1 max"], len(C1))

    if len(C1) <= cfg.shape_a_max:
        H1 = [rng.choice(list(bits(c))) for c in C1]
        S = S0.H0m | mask_of(H1)
        if cfg.use_EP:
            D = I.F_formula([S0.pl, S0.pr, (a1, a2)], S, Sp)
        else:
            D = F1 | I.dn(mask_of(H1))
        chk(D == F1 | I.dn(mask_of(H1)), "Shape A: value of the formula")
        st["max |S| Shape A"] = max(st["max |S| Shape A"], popcnt(S))
        st["max |S'| Shape A"] = max(st["max |S'| Shape A"], popcnt(Sp))
        st["max |C_1| Shape A"] = max(st["max |C_1| Shape A"], len(C1))
        final(w, D, "Shape A (C_1 empty)" if not C1 else "Shape A (C_1 nonempty)", st)
        return "Shape A"

    # Shape B
    if cfg.shape_a_max == 7:
        chosen = rng.sample(C1, 8)
        els = [rng.choice(list(bits(c))) for c in chosen]
        g1, g2 = els[:4], els[4:]
        g1.sort(key=lambda x: w.pos[x])
        g2.sort(key=lambda x: w.pos[x])
        h1, h2, h3, h4 = g1[0], g1[-1], g2[0], g2[-1]
    else:
        # the referee's variant: five classes in the order of position, the pairs c_1, c_4 and c_2, c_5
        chosen = rng.sample(C1, 5)
        els = sorted((rng.choice(list(bits(c))) for c in chosen), key=lambda x: w.pos[x])
        h1, h2, h3, h4 = els[0], els[3], els[1], els[4]
    chk(abs(w.pos[h1] - w.pos[h2]) >= 6 and abs(w.pos[h3] - w.pos[h4]) >= 6, "far pairs of Shape B")
    S = S0.E0m | mask_of(Ak)
    pairs = [S0.ps, S0.pt, (h1, h2)] + ([(h3, h4)] if cfg.use_second_pair else [])
    Dfull = I.E_formula(pairs, S if cfg.use_Akappa else S0.E0m)
    if cfg.use_Akappa:
        chk(w.L & ~Dfull == 0, "Shape B: D contains L_P")
    final(w, Dfull, "Shape B", st)
    st["max |S| Shape B"] = max(st["max |S| Shape B"], popcnt(S))

    # The core of Shape B, also for the term without up A_kappa: an element of A_P in the value lies in a class of kappa
    E2 = S0.Es & I.ER(h1, h2) & I.ER(h3, h4)
    inside = w.Am & E2
    kmask = 0
    for c in kap:
        kmask |= c
    if cfg.use_Akappa:
        chk(inside & ~kmask == 0, "Shape B: a class outside kappa inside D")
    st["Shape B: classes of kappa inside the value without A_kappa"] += 1 if inside else 0
    one = S0.Es & I.ER(h1, h2)
    if w.Am & one & ~kmask:
        st["Shape B: first pair alone leaves a class"] += 1
    return "Shape B"


def general_claim(w, cfg, rng, st, trials=6):
    """Generalized core of Shape B: for any far a_1, a_2 in R_0 (their last positions below p*) and any two far pairs from four classes of
    C_1, no class of R_0 inside the value has a position beyond p*.  The proof of Shape B uses only these properties."""
    I = w.I
    if len(w.A) <= 3 or len(w.B) <= 3:
        return
    S0 = Stage0(w, cfg, rng)
    if S0.C0 == 0 or S0.R0 == 0:
        return
    if not (S0.ss < S0.ls and S0.ts < S0.rs):
        if S0.ls < S0.ss and S0.rs < S0.ts:
            w = Walk(I, w.W[::-1])
            S0 = Stage0(w, cfg, rng, orders=(S0.or_, S0.ol, S0.ot, S0.os_))
        else:
            return
    Rcl = classes_of(w, S0.R0)
    Ccl = classes_of(w, S0.C0)
    if len(Rcl) < 2:
        return
    for _ in range(trials):
        c1, c2 = rng.sample(Rcl, 2)
        a1 = w.W[last_pos(w, c1)]
        a2 = w.W[last_pos(w, c2)]
        if abs(w.pos[a1] - w.pos[a2]) < 6:
            continue
        ps = max(w.pos[a1], w.pos[a2])
        Sp = (w.Am & I.MB[a1]) | (w.Am & I.MB[a2])
        F1 = S0.Fs | I.FR(a1, a2) | ((I.EP(a1) | I.EP(a2)) & ~I.up(Sp))
        C1 = [c for c in Ccl if c & ~F1]
        if len(C1) < 4:
            continue
        ok = None
        for _2 in range(30):
            four = rng.sample(C1, 4)
            hs = [rng.choice(list(bits(c))) for c in four]
            if abs(w.pos[hs[0]] - w.pos[hs[1]]) >= 6 and abs(w.pos[hs[2]] - w.pos[hs[3]]) >= 6:
                ok = hs
                break
        if ok is None:
            continue
        h1, h2, h3, h4 = ok
        D = S0.Es & I.ER(h1, h2) & I.ER(h3, h4)
        st["general: tested"] += 1
        for c in Rcl:
            if c & D == c:
                st["general: class of R_0 inside D"] += 1
                chk(all(w.pos[x] <= ps for x in bits(c)), "general core of Shape B: a class inside D with a position beyond p*")
            if c & D:
                pass
