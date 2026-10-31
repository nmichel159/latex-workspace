"""Referee rv-r7-desc: the construction of r7-desc.md Sections 2-3, step by step, every intermediate claim asserted.

construct(ob, rng, st): given a shortest valid path, builds the formula of Theorem B following the proof; final(D) asserts
that D is a down-set with L <= D <= M - Up and that D connects s and t.  Counters in st say which stage was reached.
check_lemmas(ob, ...): Lemmas 4.2, 4.4, 4.5 (used, reviewed elsewhere), R, EP, FP, J, G, X on the path.
theorem_A(ob, ...): the construction of Theorem A on tie-free paths.
"""
import bisect
from swf import bits, chk, ClaimFail

INF = float("inf")


class Obj:
    """Objects of Def. 4.1 for a valid path P (list of sides)."""

    def __init__(self, I, P):
        self.I, self.P = I, list(P)
        self.r = len(P)
        self.pos = {}
        WE = WF = 0
        for i, sd in enumerate(P):
            w = sd >> 1
            self.pos[w] = i + 1
            if sd & 1:
                WF |= 1 << w
            else:
                WE |= 1 << w
        self.WE, self.WF = WE, WF
        self.Up = I.up(WE)
        self.Lm = I.down(WF)
        self.A = [w for w in bits(WE) if I.DSTR[w] & WE == 0]
        self.B = [w for w in bits(WF) if I.USTR[w] & WF == 0]
        self.Am = sum(1 << a for a in self.A)
        self.Bm = sum(1 << b for b in self.B)

    def Pos(self, w):
        """Pos[w]: positions of the members of the same type tied with w."""
        mask = self.WE if self.WE >> w & 1 else self.WF
        return sorted(self.pos[x] for x in bits(self.I.CL[w] & mask))

    def C(self, a):
        return self.I.NFs[a] & self.Bm

    def Cp(self, b):
        return self.I.NEs[b] & self.Am

    def S(self, a):
        return sorted(self.pos[x] for x in bits(self.C(a)))

    def T(self, b):
        return sorted(self.pos[x] for x in bits(self.Cp(b)))


def final(ob, D, label):
    I = ob.I
    chk(I.is_downset(D), label + ": not a down-set")
    chk(ob.Lm & ~D == 0, label + ": L not inside D")
    chk(D & ob.Up == 0, label + ": D meets Up")
    chk(I.connects(D), label + ": D does not connect s, t")


def check_lemmas(ob, st, rng, far_cap=150, pair_cap=4000):
    I, A, B, r, pos = ob.I, ob.A, ob.B, ob.r, ob.pos
    m = I.m
    P = ob.P
    # Lemma 4.2
    chk(ob.Up & ob.Lm == 0, "4.2a Up meets L")
    chk(I.up(ob.Am) == ob.Up, "4.2a Up = up A")
    chk(I.down(ob.Bm) == ob.Lm, "4.2a L = down B")
    for c in range(r):
        for d in range(c + 2, r):
            chk(not (I.side(P[c]) & I.side(P[d])), "4.2e non-consecutive members meet (P not shortest?)")
    # Lemma 4.4
    for x in range(m):
        if not ob.Lm >> x & 1:
            ps = [pos[a] for a in bits(I.NEs[x] & ob.Am)]
            if ps:
                sp = max(ps) - min(ps)
                chk(sp <= 8, "4.4 span of A in star")
                st["max_span_44"] = max(st["max_span_44"], sp)
        if not ob.Up >> x & 1:
            ps = [pos[b] for b in bits(I.NFs[x] & ob.Bm)]
            if ps:
                sp = max(ps) - min(ps)
                chk(sp <= 8, "4.4 dual span of B in star")
                st["max_span_44"] = max(st["max_span_44"], sp)
    # Lemma 4.5
    for x in range(m):
        if not I.F[x]:
            continue
        for y in range(m):
            if x != y and I.E[y] and not I.comparable(x, y):
                chk(I.NEs[x] >> y & 1 or I.NFs[y] >> x & 1, "4.5 duality")
    # R(c), R(d), EP, FP
    for h in B:
        Dp = I.FP(h)
        win = I.NFs[h] & ob.Bm
        chk(win >> h & 1, "R(c) h in C_h")
        chk(popcnt_(win) <= 9, "win(h) <= 9")
        chk(ob.Bm & ~win & ~Dp == 0, "R(c) FP contains B - C_h")
        for a in A:
            if I.lt(h, a):
                chk(not Dp >> a & 1, "R(c) FP misses a > h")
        chk(I.DN[h] & ob.Up == 0, "R(d)")
    for a in A:
        De = I.EP(a)
        win = I.NEs[a] & ob.Am
        chk(popcnt_(win) <= 9, "win(a) <= 9")
        chk(ob.Am & ~win & De == 0, "EP misses A - win(a)")
        for b in B:
            if I.lt(b, a):
                chk(De >> b & 1, "EP contains b < a")
        chk(ob.Lm & I.UP[a] == 0, "R(d)")
    # R(a), R(b) on far pairs
    fa = [(x, y) for x in A for y in A if x < y and abs(pos[x] - pos[y]) >= 9]
    if len(fa) > far_cap:
        fa = rng.sample(fa, far_cap)
    for a1, a2 in fa:
        D = I.FR(a1, a2)
        chk(D & ob.Up == 0, "R(a) FR misses Up")
        chk(ob.Bm & ~ob.C(a1) & ~ob.C(a2) & ~D == 0, "R(a) FR contains B - C - C")
        st["R(a) far pairs"] += 1
    fb = [(x, y) for x in B for y in B if x < y and abs(pos[x] - pos[y]) >= 9]
    if len(fb) > far_cap:
        fb = rng.sample(fb, far_cap)
    for b1, b2 in fb:
        D = I.ER(b1, b2)
        chk(ob.Lm & ~D == 0, "R(b) ER contains L")
        chk(ob.Am & ~ob.Cp(b1) & ~ob.Cp(b2) & D == 0, "R(b) ER misses A - C' - C'")
        st["R(b) far pairs"] += 1
    # Lemma J, Lemma G
    Sd = {a: ob.S(a) for a in A}
    Td = {h: ob.T(h) for h in B}
    Pa = {a: ob.Pos(a) for a in A}
    Ph = {h: ob.Pos(h) for h in B}
    for a in A:
        S = Sd[a]
        if S and S[0] < Pa[a][0] and Pa[a][-1] < S[-1]:
            chk(S[-1] - S[0] <= 4, "Lemma J(a)")
            st["J hypothesis met"] += 1
    for h in B:
        Tt = Td[h]
        if Tt and Tt[0] < Ph[h][0] and Ph[h][-1] < Tt[-1]:
            chk(Tt[-1] - Tt[0] <= 4, "Lemma J(b)")
            st["J hypothesis met"] += 1
    prs = [(a, h) for a in A for h in B if not I.leq(h, a) and Sd[a] and Td[h]]
    if len(prs) > pair_cap:
        prs = rng.sample(prs, pair_cap)
    for a, h in prs:
        S, Tt = Sd[a], Td[h]
        Z = sorted(Pa[a] + Ph[h])
        p1, p4 = Tt[0], S[-1]
        for rho in Tt:
            if rho <= p1:
                continue
            j = bisect.bisect_left(S, rho)
            for gam in ([S[j]] if j < len(S) else []) + ([S[j - 1]] if j > 0 else []):
                lo, hi = min(rho, gam), max(rho, gam)
                if not (p1 < lo and hi < p4):
                    continue
                k = bisect.bisect_left(Z, lo)
                if k < len(Z) and Z[k] <= hi:
                    continue        # Z meets [lo, hi]
                if Z[0] > p1 and Z[-1] < p4:
                    st["G hypothesis met"] += 1
                    chk((lo - p1) + (p4 - hi) <= 8, "Lemma G")
    # Lemma X on tie-free paths
    if tie_free(ob):
        for a, h in prs:
            if I.comparable(a, h):
                continue
            S, Tt = Sd[a], Td[h]
            chk(not (S[0] <= pos[h] - 4 and S[-1] >= pos[h] + 4 and Tt[0] <= pos[a] - 4 and Tt[-1] >= pos[a] + 4),
                "Lemma X")


def popcnt_(x):
    return bin(x).count("1")


def tie_free(ob):
    I = ob.I
    for w in bits(ob.WE):
        if popcnt_(I.CL[w] & ob.WE) > 1:
            return False
    for w in bits(ob.WF):
        if popcnt_(I.CL[w] & ob.WF) > 1:
            return False
    return True


def sort_data(ob, rng):
    """l, r, u, v and the four sorts with random tie-breaks."""
    A, B = list(ob.A), list(ob.B)
    rng.shuffle(A)
    rng.shuffle(B)
    S = {a: ob.S(a) for a in A}
    Tt = {b: ob.T(b) for b in B}
    ll = {a: (S[a][0] if S[a] else INF) for a in A}
    rr = {a: (S[a][-1] if S[a] else -INF) for a in A}
    uu = {b: (Tt[b][0] if Tt[b] else INF) for b in B}
    vv = {b: (Tt[b][-1] if Tt[b] else -INF) for b in B}
    ol = sorted(A, key=lambda a: -ll[a])
    or_ = sorted(A, key=lambda a: rr[a])
    ou = sorted(B, key=lambda b: -uu[b])
    ov = sorted(B, key=lambda b: vv[b])
    return ll, rr, uu, vv, ol, or_, ou, ov


def extremes(ob, lst):
    p = sorted(lst, key=lambda x: ob.pos[x])
    return p[0], p[-1]


def theorem_A(ob, rng, st):
    """Theorem A, tie-free P."""
    I, A, B, pos = ob.I, ob.A, ob.B, ob.pos
    if len(A) < 10 or len(B) < 10:
        st["ThA trivial"] += 1
        return
    ll, rr, uu, vv, ol, or_, ou, ov = sort_data(ob, rng)
    L, R, U, V = ll[ol[9]], rr[or_[9]], uu[ou[9]], vv[ov[9]]
    FR_L = I.FR(*extremes(ob, ol[:10]))
    FR_R = I.FR(*extremes(ob, or_[:10]))
    ER_U = I.ER(*extremes(ob, ou[:10]))
    ER_V = I.ER(*extremes(ob, ov[:10]))
    E0 = set(ol[:9]) | set(or_[:9]) | {a for a in A if U <= pos[a] < U + 4 or V - 4 < pos[a] <= V}
    H0 = set(ou[:9]) | set(ov[:9]) | {b for b in B if L <= pos[b] < L + 4 or R - 4 < pos[b] <= R}
    Ao = [a for a in A if a not in E0 and U + 4 <= pos[a] <= V - 4]
    Bo = [b for b in B if b not in H0 and L + 4 <= pos[b] <= R - 4]
    for a in Ao:
        for b in Bo:
            chk(I.lt(b, a), "ThA: b < a in the middle")
    Fs = FR_L | FR_R
    for b in H0:
        Fs |= I.DN[b]
    Es = ER_U & ER_V
    for a in E0:
        Es &= ~I.UP[a]
    if len(Bo) < 18:
        D = Fs
        for b in Bo:
            D |= I.DN[b]
        final(ob, D, "ThA F*")
        st["ThA F* branch"] += 1
    elif not Ao:
        final(ob, Es, "ThA E*")
        st["ThA E* branch"] += 1
    else:
        h1, h2 = extremes(ob, Bo)
        X = I.FP(h1) | I.FP(h2)
        chk(all(not X >> a & 1 for a in Ao) and ob.Bm & ~X == 0, "ThA X")
        final(ob, Fs | (Es & X), "ThA X")
        st["ThA X branch"] += 1


class View:
    """Positions after Orientation (p or r + 1 - p)."""

    def __init__(self, ob, rev):
        self.ob, self.rev = ob, rev
        self.r = ob.r

    def p(self, x):
        return self.r + 1 - self.ob.pos[x] if self.rev else self.ob.pos[x]

    def conv(self, q):
        return sorted((self.r + 1 - y) if self.rev else y for y in q)

    def Pos(self, w):
        return self.conv(self.ob.Pos(w))

    def S(self, a):
        return self.conv(self.ob.S(a))

    def T(self, h):
        return self.conv(self.ob.T(h))


def classes(ob, V, members):
    """Tie classes of a set of members, each as (rep list, positions)."""
    I = ob.I
    seen = {}
    for w in members:
        key = min(bits(I.CL[w] & (ob.WE | ob.WF)))
        seen.setdefault(key, []).append(w)
    out = []
    for key, mem in seen.items():
        out.append({"mem": mem, "pos": sorted(V.p(x) for x in mem)})
    return out


def construct(ob, rng, st, extended=True):
    I, A, B, pos, r = ob.I, ob.A, ob.B, ob.pos, ob.r
    ALL = I.ALL
    Up, Lm = ob.Up, ob.Lm
    st["paths"] += 1
    # ------------------------------------------------------------------ Stage 0
    if len(A) < 10 or len(B) < 10:
        if len(A) < 10:
            D = ALL
            for a in A:
                D &= ~I.UP[a]
            final(ob, D, "S0 |A|<10")
            st["S0: |A|<10"] += 1
        if len(B) < 10:
            D = 0
            for b in B:
                D |= I.DN[b]
            final(ob, D, "S0 |B|<10")
            st["S0: |B|<10"] += 1
        return
    st["S0: |A|,|B|>=10"] += 1
    ll, rr, uu, vv, ol, or_, ou, ov = sort_data(ob, rng)
    L, R, U, V_ = ll[ol[9]], rr[or_[9]], uu[ou[9]], vv[ov[9]]
    for lst in (ol[:10], or_[:10], ou[:10], ov[:10]):
        x, y = extremes(ob, lst)
        chk(pos[y] - pos[x] >= 9, "S0 far pair")
    FR_L = I.FR(*extremes(ob, ol[:10]))
    FR_R = I.FR(*extremes(ob, or_[:10]))
    ER_U = I.ER(*extremes(ob, ou[:10]))
    ER_V = I.ER(*extremes(ob, ov[:10]))
    chk((FR_L | FR_R) & Up == 0, "S0 FR_L, FR_R miss Up")
    chk(Lm & ~(ER_U & ER_V) == 0, "S0 ER_U, ER_V contain L")
    for b in B:
        if pos[b] < L:
            chk(FR_L >> b & 1, "S0 FR_L contains pos(b) < L")
        if pos[b] > R:
            chk(FR_R >> b & 1, "S0 FR_R contains pos(b) > R")
    for a in A:
        if pos[a] < U:
            chk(not ER_U >> a & 1, "S0 ER_U misses pos(a) < U")
        if pos[a] > V_:
            chk(not ER_V >> a & 1, "S0 ER_V misses pos(a) > V")
    E0 = set(ol[:9]) | set(or_[:9]) | {a for a in A if U <= pos[a] < U + 5 or V_ - 5 < pos[a] <= V_}
    H0 = set(ou[:9]) | set(ov[:9]) | {b for b in B if L <= pos[b] < L + 5 or R - 5 < pos[b] <= R}
    chk(len(E0) <= 28 and len(H0) <= 28, "S0 |E_0|, |H_0| <= 28")
    Fs = FR_L | FR_R
    for b in H0:
        Fs |= I.DN[b]
    Es = ER_U & ER_V
    for a in E0:
        Es &= ~I.UP[a]
    chk(Fs & Up == 0, "S0 F* misses Up")
    chk(Lm & ~Es == 0, "S0 E* contains L")
    R0 = [a for a in A if Es >> a & 1]
    C0 = [b for b in B if not Fs >> b & 1]
    R0m = sum(1 << a for a in R0)
    C0m = sum(1 << b for b in C0)
    for a in R0:
        chk(I.CL[a] & ob.WE & ~R0m == 0, "S0 R_0 closed under ties")
    for b in C0:
        chk(I.CL[b] & ob.WF & ~C0m == 0, "S0 C_0 closed under ties")
    if not C0 or not R0:
        if not C0:
            final(ob, Fs, "S0 F*")
            st["S0 exit: C_0 empty, F*"] += 1
        if not R0:
            final(ob, Es, "S0 E*")
            st["S0 exit: R_0 empty, E*"] += 1
        return
    st["S0 pass: R_0, C_0 nonempty"] += 1
    chk(all(x not in (INF, -INF) for x in (L, R, U, V_)), "S0 L, R, U, V finite")
    for a in R0:
        chk(a not in E0, "S0 R_0 misses E_0")
        for q in ob.Pos(a):
            chk(U + 5 <= q <= V_ - 5, "S0 Pos[a] in [U+5, V-5]")
        chk(ll[a] <= L and rr[a] >= R, "S0 l(a) <= L, r(a) >= R")
    for h in C0:
        chk(h not in H0, "S0 C_0 misses H_0")
        for q in ob.Pos(h):
            chk(L + 5 <= q <= R - 5, "S0 Pos[h] in [L+5, R-5]")
        chk(uu[h] <= U and vv[h] >= V_, "S0 u(h) <= U, v(h) >= V")
    # ------------------------------------------------------------------ Orientation
    chk(U != L and U != R and V_ != L and V_ != R, "Or: positions differ")
    chk(not (U < L and R < V_), "Or: U < L, R < V is impossible by J(b)")
    chk(not (L < U and V_ < R), "Or: L < U, V < R is impossible by J(a)")
    rev = L < U and R < V_
    if rev:
        st["Or: reversed"] += 1
        L, R, U, V_ = r + 1 - R, r + 1 - L, r + 1 - V_, r + 1 - U
    else:
        st["Or: direct"] += 1
    chk(U < L and V_ < R, "Or: U < L, V < R after reversal")
    W = View(ob, rev)
    S = {a: W.S(a) for a in A}
    Tt = {b: W.T(b) for b in B}
    PosA = {a: W.Pos(a) for a in R0}
    PosH = {h: W.Pos(h) for h in C0}
    for a in R0:
        chk(U + 5 <= PosA[a][0] and PosA[a][-1] <= V_ - 5, "Or: inclusions a")
        chk(S[a][0] <= L and S[a][-1] >= R, "Or: l, r")
    for h in C0:
        chk(L + 5 <= PosH[h][0] and PosH[h][-1] <= R - 5, "Or: inclusions h")
        chk(Tt[h][0] <= U and Tt[h][-1] >= V_, "Or: u, v")
    # Proposition C (a), (b)
    for h in C0:
        chk(PosH[h][-1] > V_, "PropC(a) class of C_0 has a position > V")
    for a in R0:
        chk(PosA[a][0] < L, "PropC(a) class of R_0 has a position < L")
    # (star)
    R0pos = sorted(W.p(a) for a in R0)
    C0pos = sorted(W.p(h) for h in C0)
    R0posS, C0posS = set(R0pos), set(C0pos)
    n_pairs = 0
    for a in R0:
        Sc = [q for q in S[a] if q in C0posS]
        if not Sc:
            continue
        for h in C0:
            if I.leq(h, a):
                continue
            n_pairs += 1
            Z = sorted(PosA[a] + PosH[h])
            for rho in Tt[h]:
                if rho not in R0posS:
                    continue
                j = bisect.bisect_left(Sc, rho)
                for gam in ([Sc[j]] if j < len(Sc) else []) + ([Sc[j - 1]] if j > 0 else []):
                    lo, hi = min(rho, gam), max(rho, gam)
                    k = bisect.bisect_left(Z, lo)
                    chk(k < len(Z) and Z[k] <= hi, "(star) fails")
                    st["(star) tested"] += 1
    if n_pairs:
        st["paths with non-strict R_0 x C_0 pair"] += 1
    if extended:
        generalized(ob, W, I, R0, C0, S, Tt, Fs, Es, rng, st)
    # ------------------------------------------------------------------ Stage 1
    K = [dict(c, typ="R") for c in classes(ob, W, R0)] + [dict(c, typ="C") for c in classes(ob, W, C0)]
    if len(K) < 20:
        D = Fs
        for c in K:
            if c["typ"] == "C":
                D |= I.DN[c["mem"][0]]
        final(ob, D, "S1 |K| < 20")
        st["S1: |K|<20"] += 1
        return
    st["S1: |K|>=20"] += 1
    K.sort(key=lambda c: c["pos"][-1])
    # Proposition C (b): every class of R_0 before every class of C_0 in the sort by last position
    seen_c = False
    for c in K:
        if c["typ"] == "C":
            seen_c = True
        else:
            chk(not seen_c, "PropC(b) class of R_0 after a class of C_0")
    kap = K[:20]
    pst = kap[-1]["pos"][-1]
    for c in K[20:]:
        chk(c["pos"][-1] > pst, "S1 other classes have a tail position")
    Rk = [c for c in kap if c["typ"] == "R"]
    Ck = [c for c in kap if c["typ"] == "C"]
    Ek = ALL
    for c in Rk:
        Ek &= ~I.UP[rng.choice(c["mem"])]
    Fk = 0
    for c in Ck:
        Fk |= I.DN[rng.choice(c["mem"])]
    if len(Rk) >= 10:
        case_I(ob, W, K, Rk, Ek, Fk, Fs, Es, R0, C0, rng, st)
    if len(Ck) >= 10:
        case_II_written(ob, W, K, Ck, Rk, Ek, Fk, Fs, Es, R0, C0, rng, st)
    if extended:
        mirror(ob, W, K, Fs, Es, rng, st)


def far_pair_from(ob, W, cl, rng):
    """A pair of elements from different classes of cl at distance >= 9, or None."""
    els = [(W.p(x), i, x) for i, c in enumerate(cl) for x in c["mem"]]
    if len(els) < 2:
        return None
    for _ in range(40):
        x, y = rng.sample(els, 2)
        if x[1] != y[1] and abs(x[0] - y[0]) >= 9:
            return (x[2], y[2], x[1], y[1])
    els.sort()
    for x, y in ((els[0], els[-1]),):
        if x[1] != y[1] and abs(x[0] - y[0]) >= 9:
            return (x[2], y[2], x[1], y[1])
    return None


def f1_of(ob, W, a1, a2, Fs, Fk):
    I = ob.I
    win = (I.NEs[a1] | I.NEs[a2]) & ob.Am
    chk(bin(win).count("1") <= 18, "|win(a1) + win(a2)| <= 18")
    Wc = I.ALL
    for a in bits(win):
        Wc &= ~I.UP[a]
    chk(ob.Lm & ~Wc == 0, "W contains L")
    part = Wc & (I.EP(a1) | I.EP(a2))
    chk(part & ob.Am == 0, "W & (EP + EP) misses A")
    F1 = Fs | Fk | I.FR(a1, a2) | part
    chk(F1 & ob.Up == 0, "F^1 misses Up")
    chk(I.is_downset(F1), "F^1 down-set")
    return F1


def e1_of(ob, W, h1, h2, Es, Ek):
    I = ob.I
    win = (I.NFs[h1] | I.NFs[h2]) & ob.Bm
    chk(bin(win).count("1") <= 18, "|win(h1) + win(h2)| <= 18")
    V0 = 0
    for b in bits(win):
        V0 |= I.DN[b]
    part = V0 | (I.FP(h1) & I.FP(h2))
    chk(ob.Bm & ~part == 0, "V_0 + FP & FP contains B")
    E1 = Es & Ek & I.ER(h1, h2) & part
    chk(ob.Lm & ~E1 == 0, "E^1 contains L")
    chk(I.is_downset(E1), "E^1 down-set")
    return E1


def check_C1(ob, W, F1, a1, a2, C_classes, in_kappa_ids):
    """Classes of C_0 outside F^1 and the facts claimed for them."""
    I = ob.I
    S1, S2 = set(W.S(a1)), set(W.S(a2))
    out = []
    for c in C_classes:
        inn = [F1 >> x & 1 for x in c["mem"]]
        chk(all(inn) or not any(inn), "F^1 cuts a class")
        if any(inn):
            continue
        for x in c["mem"]:
            chk(W.p(x) in S1 or W.p(x) in S2, "Case I: Pos[h] inside S(a1) + S(a2)")
            chk(not I.leq(x, a1) and not I.leq(x, a2), "Case I: h not <= a_i")
        out.append(c)
    return out


def check_R1(ob, W, E1, h1, h2, R_classes):
    I = ob.I
    T1, T2 = set(W.T(h1)), set(W.T(h2))
    out = []
    for c in R_classes:
        inn = [E1 >> x & 1 for x in c["mem"]]
        chk(all(inn) or not any(inn), "E^1 cuts a class")
        if not any(inn):
            continue
        for x in c["mem"]:
            chk(W.p(x) in T1 or W.p(x) in T2, "Case II: Pos[a] inside T(h1) + T(h2)")
            chk(not I.leq(h1, x) and not I.leq(h2, x), "Case II: h_i not <= a")
        out.append(c)
    return out


def twenty_pick(ob, W, classes_, rng):
    """20 classes, one element of each, two pairs at distance >= 9 among the first and the other 10 by position."""
    pick = rng.sample(classes_, 20)
    els = sorted((rng.choice(c["mem"]) for c in pick), key=W.p)
    x1, x2, x3, x4 = els[0], els[9], els[10], els[19]
    chk(W.p(x2) - W.p(x1) >= 9 and W.p(x4) - W.p(x3) >= 9, "far pairs in the 20 classes")
    return x1, x2, x3, x4


def case_I(ob, W, K, Rk, Ek, Fk, Fs, Es, R0, C0, rng, st):
    I = ob.I
    st["Case I"] += 1
    ten = rng.sample(Rk, 10)
    lasts = sorted(c["pos"][-1] for c in ten)
    byp = {W.p(a): a for a in R0}
    a1, a2 = byp[lasts[0]], byp[lasts[-1]]
    chk(lasts[-1] - lasts[0] >= 9, "Case I: a1, a2 far")
    pst = max(c["pos"][-1] for c in K[:20])
    chk(W.Pos(a1)[-1] <= pst and W.Pos(a2)[-1] <= pst, "Case I: Pos[a_i] misses the tail")
    F1 = f1_of(ob, W, a1, a2, Fs, Fk)
    Cc = [c for c in K if c["typ"] == "C"]
    C1 = check_C1(ob, W, F1, a1, a2, Cc, None)
    kap_ids = {id(c) for c in K[:20]}
    for c in C1:
        chk(id(c) not in kap_ids, "Case I: class of C_1 inside kappa")
        chk(c["pos"][-1] > pst, "Case I: class of C_1 has a tail position")
    st["C_1 max"] = max(st["C_1 max"], len(C1))
    if len(C1) == 0:
        final(ob, F1, "Case I F^1")
        st["Case I: F^1 alone"] += 1
    elif len(C1) < 20:
        D = F1
        for c in C1:
            D |= I.DN[rng.choice(c["mem"])]
        final(ob, D, "Shape A")
        st["Shape A (C_1 nonempty)"] += 1
    else:
        x1, x2, x3, x4 = twenty_pick(ob, W, C1, rng)
        D = Es & Ek & I.ER(x1, x2) & I.ER(x3, x4)
        final(ob, D, "Shape B")
        st["Shape B"] += 1
        one = [a for a in R0 if (Es & Ek & I.ER(x1, x2)) >> a & 1 or (Es & Ek & I.ER(x3, x4)) >> a & 1]
        if one:
            st["Shape B: one pair alone leaves a class of R_0"] += 1
        Rin = [a for a in R0 if D >> a & 1]
        chk(not Rin, "Shape B: D meets R_0")


def case_II_written(ob, W, K, Ck, Rk, Ek, Fk, Fs, Es, R0, C0, rng, st):
    """Case II as written in r7-desc.md (tail on the right).  Proposition C says R_1 is empty."""
    I = ob.I
    st["Case II (as written)"] += 1
    ten = rng.sample(Ck, 10)
    lasts = sorted(c["pos"][-1] for c in ten)
    byp = {W.p(h): h for h in C0}
    h1, h2 = byp[lasts[0]], byp[lasts[-1]]
    chk(lasts[-1] - lasts[0] >= 9, "Case II: h1, h2 far")
    E1 = e1_of(ob, W, h1, h2, Es, Ek)
    Rc = [c for c in K if c["typ"] == "R"]
    R1 = check_R1(ob, W, E1, h1, h2, Rc)
    chk(not R1, "PropC(c): R_1 not empty in Case II")
    chk(all(not (Es & Ek) >> a & 1 for a in ob.A), "PropC(c): E* & E_kappa misses A")
    final(ob, E1, "Case II E^1")
    final(ob, Es & Ek, "Case II E* & E_kappa")
    st["Case II: R_1 empty (Prop. C)"] += 1


def mirror(ob, W, K, Fs, Es, rng, st):
    """The true dual of Case I: tail on the left, kappa' = the 20 classes with the largest first positions."""
    I = ob.I
    Km = sorted(K, key=lambda c: -c["pos"][0])
    kap = Km[:20]
    pst = kap[-1]["pos"][0]
    for c in Km[20:]:
        chk(c["pos"][0] < pst, "mirror: other classes have a tail position")
    Rk = [c for c in kap if c["typ"] == "R"]
    Ck = [c for c in kap if c["typ"] == "C"]
    Ek = I.ALL
    for c in Rk:
        Ek &= ~I.UP[rng.choice(c["mem"])]
    Fk = 0
    for c in Ck:
        Fk |= I.DN[rng.choice(c["mem"])]
    if len(Ck) >= 10:
        st["Mirror II°"] += 1
        ten = rng.sample(Ck, 10)
        firsts = sorted(c["pos"][0] for c in ten)
        allC = [x for c in K if c["typ"] == "C" for x in c["mem"]]
        byp = {W.p(h): h for h in allC}
        h1, h2 = byp[firsts[0]], byp[firsts[-1]]
        chk(firsts[-1] - firsts[0] >= 9, "mirror: h1, h2 far")
        E1 = e1_of(ob, W, h1, h2, Es, Ek)
        Rc = [c for c in K if c["typ"] == "R"]
        R1 = check_R1(ob, W, E1, h1, h2, Rc)
        kap_ids = {id(c) for c in kap}
        for c in R1:
            chk(id(c) not in kap_ids, "mirror: class of R_1 inside kappa'")
        st["R_1 max"] = max(st["R_1 max"], len(R1))
        if not R1:
            final(ob, E1, "mirror E^1")
            st["Mirror II°: E^1 alone"] += 1
        elif len(R1) < 20:
            D = E1
            for c in R1:
                D &= ~I.UP[rng.choice(c["mem"])]
            final(ob, D, "Shape A'")
            st["Shape A' (mirror, R_1 nonempty)"] += 1
        else:
            x1, x2, x3, x4 = twenty_pick(ob, W, R1, rng)
            D = Fs | Fk | I.FR(x1, x2) | I.FR(x3, x4)
            final(ob, D, "Shape B'")
            st["Shape B' (mirror)"] += 1
    if len(Rk) >= 10:
        st["Mirror I°"] += 1
        chk(all(ob.Bm >> h & 1 for c in K if c["typ"] == "C" for h in c["mem"]), "sanity")
        # Prop. C in the mirror: all classes of C_0 lie in kappa', so F* + F_kappa' contains B
        if len(Rk) >= 10 and len(Km) >= 20:
            final(ob, Fs | Fk, "mirror I° F* + F_kappa'") if all(c in kap for c in K if c["typ"] == "C") else None
            chk(all(c in kap for c in K if c["typ"] == "C"), "Prop C mirror: C_0 inside kappa'")


def generalized(ob, W, I, R0, C0, S, Tt, Fs, Es, rng, st, trials=6):
    """The proof of the claim of Shape B (and of Shape B') uses no count 20: a_1, a_2 far with no tail position, E_kappa, F_kappa
    over all classes without a tail position, far pairs from disjoint classes.  Stress test of the argument with any p*."""
    K = [dict(c, typ="R") for c in classes(ob, W, R0)] + [dict(c, typ="C") for c in classes(ob, W, C0)]
    allpos = sorted(q for c in K for q in c["pos"])
    for _ in range(trials):
        pst = rng.choice(allpos)
        # tail on the right
        kap = [c for c in K if c["pos"][-1] <= pst]
        out = [c for c in K if c["pos"][-1] > pst]
        Rk = [c for c in kap if c["typ"] == "R"]
        Ck = [c for c in kap if c["typ"] == "C"]
        Ek = I.ALL
        for c in Rk:
            Ek &= ~I.UP[c["mem"][0]]
        Fk = 0
        for c in Ck:
            Fk |= I.DN[c["mem"][0]]
        fp = far_pair_from(ob, W, Rk, rng)
        if fp:
            a1, a2 = fp[0], fp[1]
            F1 = f1_of(ob, W, a1, a2, Fs, Fk)
            C1 = check_C1(ob, W, F1, a1, a2, [c for c in out if c["typ"] == "C"], None)
            st["gen right: a-pair"] += 1
            if len(C1) >= 4:
                p1 = far_pair_from(ob, W, C1, rng)
                if p1:
                    rest = [c for i, c in enumerate(C1) if i not in (p1[2], p1[3])]
                    p2 = far_pair_from(ob, W, rest, rng)
                    if p2:
                        D = Es & Ek & I.ER(p1[0], p1[1]) & I.ER(p2[0], p2[1])
                        final(ob, D, "generalized claim of Shape B")
                        st["gen right: claim B tested"] += 1
        # tail on the left
        kap = [c for c in K if c["pos"][0] >= pst]
        out = [c for c in K if c["pos"][0] < pst]
        Rk = [c for c in kap if c["typ"] == "R"]
        Ck = [c for c in kap if c["typ"] == "C"]
        Ek = I.ALL
        for c in Rk:
            Ek &= ~I.UP[c["mem"][0]]
        Fk = 0
        for c in Ck:
            Fk |= I.DN[c["mem"][0]]
        fp = far_pair_from(ob, W, Ck, rng)
        if fp:
            h1, h2 = fp[0], fp[1]
            E1 = e1_of(ob, W, h1, h2, Es, Ek)
            R1 = check_R1(ob, W, E1, h1, h2, [c for c in out if c["typ"] == "R"])
            st["gen left: h-pair"] += 1
            if len(R1) >= 4:
                p1 = far_pair_from(ob, W, R1, rng)
                if p1:
                    rest = [c for i, c in enumerate(R1) if i not in (p1[2], p1[3])]
                    p2 = far_pair_from(ob, W, rest, rng)
                    if p2:
                        D = Fs | Fk | I.FR(p1[0], p1[1]) | I.FR(p2[0], p2[1])
                        final(ob, D, "generalized claim of Shape B'")
                        st["gen left: claim B' tested"] += 1


def run_all(I, P, rng, st, trials=1, lemmas=True, extended=True):
    """All checks for one instance and one shortest valid path."""
    chk(I.is_valid_path(P), "P is not a valid path")
    ob = Obj(I, P)
    if lemmas:
        check_lemmas(ob, st, rng)
    if tie_free(ob):
        st["tie-free paths"] += 1
        theorem_A(ob, rng, st)
    for _ in range(trials):
        construct(ob, rng, st, extended=extended)
