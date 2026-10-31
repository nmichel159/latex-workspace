"""r7-desc: checks of Lemma G and Theorem B (r7-desc.md Section 3).

  python check_b.py g SEED COUNT NMIN NMAX             falsification of Lemma G on planted configurations with ties
  python check_b.py sat SEED COUNT NMIN NMAX EXT K KAP  saturated planted paths with crossing classes: Theorem B with
                                                        thresholds EXT (10), K (5), KAP (20); all lemmas pointwise
  python check_b.py rigid SEED COUNT NMIN NMAX PTIE     Theorem B with the true thresholds on rigid designs
  python check_b.py files FILE...                       the same on stored instances, all shortest paths (cap 20)

A failure is a counter ending in FAIL.  With thresholds below the true ones a wrong formula is not a failure of the
proof (the distance hypotheses of Lemma R are missing); such events are counted under "small thresholds".
"""
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
from check_a import load, atom_FR, atom_ER, atom_FP, INF  # noqa: E402
from zzl import Budget, SW, Skel, all_shortest_valid_paths, bits, popcount, term_D  # noqa: E402
import gen8  # noqa: E402


def atom_EP(I, a):
    return term_D(I, "E", [a], [a], 0, 0)[0]


class Con:
    """Contacts of a valid path: S[a] = positions of C(a), T[h] = positions of C'(h), Pos[w] = positions of the
    same-type members tied with w."""

    def __init__(self, I, Sk):
        self.I = I
        self.Sk = Sk
        self.A = list(bits(Sk.A))
        self.B = list(bits(Sk.B))
        pos = Sk.pos
        self.pos = pos
        self.S = {a: sorted(pos[b] for b in bits(Sk.B & I.NFs[a])) for a in self.A}
        self.T = {b: sorted(pos[a] for a in bits(Sk.A & I.NEs[b])) for b in self.B}
        self.Pos = {}
        for a in self.A:
            self.Pos[a] = sorted(pos[w] for w in bits(I.tie[a] & Sk.WE))
        for b in self.B:
            self.Pos[b] = sorted(pos[w] for w in bits(I.tie[b] & Sk.WF))


def lemma_g_pointwise(I, Sk, c, cnt):
    """Lemmas J and G for every a, h and every quadruple of contacts on a shortest valid path."""
    for a in c.A:
        Pa = c.Pos[a]
        Sa = c.S[a]
        if Sa and Sa[0] < Pa[0] and Sa[-1] > Pa[-1]:
            cnt["J(a) instances"] += 1
            if Sa[-1] - Sa[0] > 4:
                # contacts c < d around Pos[a]: the largest span
                cnt["Lemma J(a) FAIL"] += 1
    for h in c.B:
        Ph = c.Pos[h]
        Th = c.T[h]
        if Th and Th[0] < Ph[0] and Th[-1] > Ph[-1]:
            cnt["J(b) instances"] += 1
            if Th[-1] - Th[0] > 4:
                cnt["Lemma J(b) FAIL"] += 1
    for a in c.A:
        for h in c.B:
            if I.le[h][a]:
                continue
            Z = sorted(set(c.Pos[a]) | set(c.Pos[h]))
            Sa, Th = c.S[a], c.T[h]
            if not Sa or not Th:
                continue
            for p1 in Th:
                for p4 in Sa:
                    if not (p1 < Z[0] and Z[-1] < p4):
                        continue
                    for x in Th:
                        for y in Sa:
                            p2, p3 = min(x, y), max(x, y)
                            if p2 <= p1 or p3 >= p4 or x == y:
                                continue
                            if any(p2 <= z <= p3 for z in Z):
                                continue
                            cnt["G quadruples"] += 1
                            if (p2 - p1) + (p4 - p3) > 8:
                                cnt["Lemma G FAIL"] += 1


def far(c, elems):
    e = sorted(elems, key=lambda w: c.pos[w])
    return e[0], e[-1]


def theorem_b(I, Sk, c, cnt, EXT=10, K=5, KAP=20):
    """The construction of Theorem B; returns the down-set D."""
    A, B = c.A, c.B
    full = I.full
    if len(A) < EXT:
        cnt["shape: small A"] += 1
        D = full
        for a in A:
            D &= full & ~I.up[a]
        return D
    if len(B) < EXT:
        cnt["shape: small B"] += 1
        D = 0
        for b in B:
            D |= I.dn[b]
        return D
    l = {a: (c.S[a][0] if c.S[a] else INF) for a in A}
    r = {a: (c.S[a][-1] if c.S[a] else -INF) for a in A}
    u = {b: (c.T[b][0] if c.T[b] else INF) for b in B}
    v = {b: (c.T[b][-1] if c.T[b] else -INF) for b in B}
    byl = sorted(A, key=lambda a: -l[a])
    byr = sorted(A, key=lambda a: r[a])
    byu = sorted(B, key=lambda b: -u[b])
    byv = sorted(B, key=lambda b: v[b])
    L, R, U, V = l[byl[EXT - 1]], r[byr[EXT - 1]], u[byu[EXT - 1]], v[byv[EXT - 1]]
    pos = c.pos
    E0 = set(byl[:EXT - 1]) | set(byr[:EXT - 1]) | {a for a in A if U <= pos[a] < U + K or V - K < pos[a] <= V}
    H0 = set(byu[:EXT - 1]) | set(byv[:EXT - 1]) | {b for b in B if L <= pos[b] < L + K or R - K < pos[b] <= R}
    Fs = atom_FR(I, *far(c, byl[:EXT])) | atom_FR(I, *far(c, byr[:EXT]))
    for b in H0:
        Fs |= I.dn[b]
    Es = atom_ER(I, *far(c, byu[:EXT])) & atom_ER(I, *far(c, byv[:EXT]))
    for a in E0:
        Es &= full & ~I.up[a]
    R0 = [a for a in A if (Es >> a) & 1]
    C0 = [b for b in B if not (Fs >> b) & 1]
    cnt["paths reaching Stage 0"] += 1
    if not C0:
        cnt["shape: F* (C_0 empty)"] += 1
        return Fs
    if not R0:
        cnt["shape: E* (R_0 empty)"] += 1
        return Es
    cnt["R_0, C_0 both non-empty"] += 1
    # orientation; the reversed path is treated by mirroring positions in (star) only, which Stage 1 does not read
    # directly: Stage 1 below needs "tail" on the side away from the walks, and works for both orientations by symmetry
    mirror = (L < U and R < V)
    if (U < L and R < V) or (L < U and V < R):
        cnt["nested zones with alive classes"] += 1
        return None
    def key_last(cl_pos):
        return -cl_pos[0] if mirror else cl_pos[-1]

    classes = {}
    for w in R0:
        classes[("R", min(bits(I.tie[w] & Sk.A)))] = c.Pos[w]
    for w in C0:
        classes[("C", min(bits(I.tie[w] & Sk.B)))] = c.Pos[w]
    keys = sorted(classes, key=lambda k_: key_last(classes[k_]))
    if len(keys) < KAP:
        cnt["shape: few classes"] += 1
        D = Fs
        for k_ in keys:
            if k_[0] == "C":
                D |= I.dn[k_[1]]
        return D
    kap = keys[:KAP]
    last = lambda k_: (classes[k_][0] if mirror else classes[k_][-1])
    pstar = key_last(classes[kap[-1]])
    in_tail = lambda p: (-p if mirror else p) > pstar
    # representatives: the element at the last position of a class
    at = {pos[w]: w for w in A + B}
    rowk = [k_ for k_ in kap if k_[0] == "R"]
    colk = [k_ for k_ in kap if k_[0] == "C"]
    Fk = 0
    Ek = full
    for k_ in kap:
        if k_[0] == "C":
            Fk |= I.dn[k_[1]]
        else:
            Ek &= full & ~I.up[k_[1]]
    half = KAP // 2
    if len(rowk) >= half:
        cnt["case I"] += 1
        a1, a2 = far(c, [at[last(k_)] for k_ in rowk[:half]])
        win = (Sk.A & I.NEs[a1]) | (Sk.A & I.NEs[a2])
        W = full
        for a in bits(win):
            W &= full & ~I.up[a]
        F1 = Fs | Fk | atom_FR(I, a1, a2) | (W & (atom_EP(I, a1) | atom_EP(I, a2)))
        if F1 & Sk.Up:
            cnt["F^1 meets Up (small thresholds or FAIL)"] += 1
        C1 = {}
        for b in C0:
            if not (F1 >> b) & 1:
                C1[min(bits(I.tie[b] & Sk.B))] = b
        if not C1:
            cnt["shape: F^1 alone"] += 1
            return F1
        if len(C1) < KAP:
            cnt["shape A"] += 1
            D = F1
            for b in C1:
                D |= I.dn[b]
            return D
        reps = list(C1)[:KAP]
        h1, h2 = far(c, reps[:half])
        h3, h4 = far(c, reps[half:])
        cnt["shape B"] += 1
        D = Es & Ek & atom_ER(I, h1, h2) & atom_ER(I, h3, h4)
        if D & Sk.A:
            cnt["shape B: claim wrong (small thresholds or FAIL)"] += 1
        return D
    cnt["case II"] += 1
    h1, h2 = far(c, [at[last(k_)] for k_ in colk[:half]])
    win = (Sk.B & I.NFs[h1]) | (Sk.B & I.NFs[h2])
    V0 = 0
    for b in bits(win):
        V0 |= I.dn[b]
    E1 = Es & Ek & atom_ER(I, h1, h2) & (V0 | (atom_FP(I, h1) & atom_FP(I, h2)))
    if Sk.L & ~E1:
        cnt["E^1 misses L (small thresholds or FAIL)"] += 1
    R1 = {}
    for a in R0:
        if (E1 >> a) & 1:
            R1[min(bits(I.tie[a] & Sk.A))] = a
    if not R1:
        cnt["shape: E^1 alone"] += 1
        return E1
    if len(R1) < KAP:
        cnt["shape A'"] += 1
        D = E1
        for a in R1:
            D &= full & ~I.up[a]
        return D
    reps = list(R1)[:KAP]
    a1, a2 = far(c, reps[:half])
    a3, a4 = far(c, reps[half:])
    cnt["shape B'"] += 1
    D = Fs | Fk | atom_FR(I, a1, a2) | atom_FR(I, a3, a4)
    if Sk.B & ~D:
        cnt["shape B': claim wrong (small thresholds or FAIL)"] += 1
    return D


def run_path(I, P, cnt, EXT=10, K=5, KAP=20, pointwise=True, verified=True):
    Sk = Skel(I, P)
    c = Con(I, Sk)
    cnt["paths"] += 1
    cnt["paths with same-type ties" if (any(len(c.Pos[w]) > 1 for w in c.A + c.B)) else "tie-free paths"] += 1
    if pointwise and verified:
        lemma_g_pointwise(I, Sk, c, cnt)
    D = theorem_b(I, Sk, c, cnt, EXT, K, KAP)
    true_thr = (EXT, K, KAP) == (10, 5, 20)
    if D is None:
        cnt["nested with alive classes FAIL" if true_thr else "nested (small thresholds)"] += 1
        return
    ok = I.is_down(D) and not (Sk.L & ~D) and not (D & Sk.Up) and I.connects(D)
    if ok:
        cnt["formula picks P"] += 1
    else:
        cnt["formula wrong FAIL" if true_thr else "formula wrong (small thresholds)"] += 1


# ------------------------------------------------------------------- planted instances with classes

def closure(le):
    m = len(le)
    for k_ in range(m):
        for i in range(m):
            if le[i][k_]:
                for j in range(m):
                    if le[k_][j]:
                        le[i][j] = True


class Planted:
    """Word over E, F; tie classes among same-type members; hubs for P2 inside A and inside B."""

    def __init__(self, word, ties):
        self.word = word
        n = self.n = len(word)
        self.nn = 2
        self.s, self.t = 0, 1
        self.E = [0] * n
        self.F = [0] * n
        self.side(0, self.s)
        self.side(n - 1, self.t)
        for i in range(n - 1):
            c = self.new()
            self.side(i, c)
            self.side(i + 1, c)
        self.le = [[i == j for j in range(n)] for i in range(n)]
        for cl in ties:
            for x in cl:
                for y in cl:
                    self.le[x][y] = True
        ef = self.new()
        fh = self.new()
        for i in range(n):
            if word[i] == "F":
                self.E[i] |= 1 << ef
            else:
                self.F[i] |= 1 << fh

    def new(self):
        self.nn += 1
        return self.nn - 1

    def side(self, i, c):
        if self.word[i] == "E":
            self.E[i] |= 1 << c
        else:
            self.F[i] |= 1 << c

    def inst(self):
        le = [row[:] for row in self.le]
        closure(le)
        return SW(self.n, le, self.E, self.F, self.s, self.t, self.nn, [])

    def path(self):
        return [(i, 0 if self.word[i] == "E" else 1) for i in range(self.n)]


def shortest_len(I, limit, cap=400000):
    """Least number of sides of a conflict-free walk from s to t, if at most limit; else None.  BFS by levels over
    (side, Up, Dn) with dominance per side; a shortest such walk is a shortest valid path (Lemma 3.4).  Raises
    Budget beyond cap states."""
    sides = [(w, ty) for w in range(I.m) for ty in (0, 1) if (I.F[w] if ty else I.E[w])]
    sn = {sd: (I.F[sd[0]] if sd[1] else I.E[sd[0]]) for sd in sides}
    nbr = {sd: [o for o in sides if o != sd and sn[sd] & sn[o]] for sd in sides}
    seen = {sd: [] for sd in sides}
    front = []
    total = 0

    def add(sd, U, Dn, out):
        nonlocal total
        lst = seen[sd]
        for (u0, d0) in lst:
            if not (u0 & ~U) and not (d0 & ~Dn):
                return
        lst[:] = [(u0, d0) for (u0, d0) in lst if (U & ~u0) or (Dn & ~d0)]
        lst.append((U, Dn))
        out.append((sd, U, Dn))
        total += 1
        if total > cap:
            raise Budget()
    for sd in sides:
        if (sn[sd] >> I.s) & 1:
            w, ty = sd
            add(sd, 0 if ty else I.up[w], I.dn[w] if ty else 0, front)
    lev = 1
    while front and lev <= limit:
        nxt = []
        for (sd, U, Dn) in front:
            if (sn[sd] >> I.t) & 1:
                return lev
        for (sd, U, Dn) in front:
            for o in nbr[sd]:
                w, ty = o
                if ty == 0:
                    if (Dn >> w) & 1:
                        continue
                    add(o, U | I.up[w], Dn, nxt)
                else:
                    if (U >> w) & 1:
                        continue
                    add(o, U, Dn | I.dn[w], nxt)
        front = nxt
        lev += 1
    return None


def still_shortest(pl, budget):
    I = pl.inst()
    try:
        return shortest_len(I, pl.n - 1) is None
    except Budget:
        return None


def crossing2(rng, g, nr, nc):
    """Word G0 A1 C0 B1 A2 G3 B2 C3 with crossing classes A1_i ~ A2_i, B1_j ~ B2_j; pre-contacts: every column of
    B1, B2 touches G0 and G3 by its E-side, every row of A1, A2 catches C0 and C3 by its F-side.  Stage 1 exercise."""
    word = ""
    idx = {}

    def run(name, ch, k_):
        nonlocal word
        idx[name] = list(range(len(word), len(word) + k_))
        word += ch * k_
    run("G0", "E", g)
    run("A1", "E", nr)
    run("C0", "F", g)
    run("B1", "F", nc)
    run("A2", "E", nr)
    run("G3", "E", g)
    run("B2", "F", nc)
    run("C3", "F", g)
    p1, p2 = list(range(nr)), list(range(nr))
    rng.shuffle(p1)
    rng.shuffle(p2)
    ties = [[idx["A1"][p1[i]], idx["A2"][p2[i]]] for i in range(nr)]
    q1, q2 = list(range(nc)), list(range(nc))
    rng.shuffle(q1)
    rng.shuffle(q2)
    ties += [[idx["B1"][q1[j]], idx["B2"][q2[j]]] for j in range(nc)]
    pre = []
    for h in idx["B1"] + idx["B2"]:
        for e in idx["G0"] + idx["G3"]:
            pre.append(("E", e, h))
    for a in idx["A1"] + idx["A2"]:
        for f in idx["C0"] + idx["C3"]:
            pre.append(("F", a, f))
    # the extreme runs are crossing classes too, with the same hull contacts
    r0, r3 = list(idx["G0"]), list(idx["G3"])
    rng.shuffle(r3)
    c0, c3 = list(idx["C0"]), list(idx["C3"])
    rng.shuffle(c3)
    ties += [[x, y] for x, y in zip(r0, r3)] + [[x, y] for x, y in zip(c0, c3)]
    for c_ in c0 + c3:
        for e in r0 + r3:
            pre.append(("E", e, c_))
    for e in r0 + r3:
        for f in c0 + c3:
            pre.append(("F", e, f))
    return word, ties, pre


def saturate(rng, word, ties, budget=60000, prob=1.0, pre=()):
    """Adds contacts F_a - X_b and E_b - X_a in random order, keeping the planted path shortest (exact search);
    for a row/column pair (classes of A, B) without any contact: strict relation b < a.  Gives P2."""
    pl = Planted(word, ties)
    n = pl.n
    Es = [i for i in range(n) if word[i] == "E"]
    Fs = [i for i in range(n) if word[i] == "F"]
    for (kd, a0, b0) in pre:
        c = pl.new()
        if kd == "F":
            pl.F[a0] |= 1 << c
            pl.F[b0] |= 1 << c
        else:
            pl.E[a0] |= 1 << c
            pl.E[b0] |= 1 << c
    if not still_shortest(pl, budget):
        return None
    pairs = [(a, b) for a in Es for b in Fs]
    rng.shuffle(pairs)
    stats = Counter()
    for (a, b) in pairs:
        if abs(a - b) <= 1 and rng.random() < 0.5:
            pass
        kinds = ["F", "E"]
        rng.shuffle(kinds)
        done = False
        if rng.random() < prob:
            for kd in kinds:
                saveE, saveF, savenn = pl.E[:], pl.F[:], pl.nn
                c = pl.new()
                if kd == "F":
                    pl.F[a] |= 1 << c
                    pl.F[b] |= 1 << c
                else:
                    pl.E[a] |= 1 << c
                    pl.E[b] |= 1 << c
                ok = still_shortest(pl, budget)
                if ok:
                    done = True
                    stats["contact " + kd] += 1
                    break
                pl.E, pl.F, pl.nn = saveE, saveF, savenn
                stats["rejected"] += 1
        if not done:
            pl.le[b][a] = True
            stats["strict"] += 1
    I = pl.inst()
    return I, pl.path(), stats


def crossing_word(rng, nr, nc, blocks):
    """(a-run b-run)^blocks with the classes of rows and of columns tied across the blocks, in random orders."""
    word = ""
    rows = [[] for _ in range(nr)]
    cols = [[] for _ in range(nc)]
    for bl in range(blocks):
        order = list(range(nr))
        rng.shuffle(order)
        for i in order:
            rows[i].append(len(word))
            word += "E"
        order = list(range(nc))
        rng.shuffle(order)
        for j in order:
            cols[j].append(len(word))
            word += "F"
    return word, rows + cols


def xtie(rng, g, nr, nc, flips, budget=400000):
    """Skeleton crossing2, every middle row strictly above every middle column, extreme cells by contacts or strict.
    Then up to flips attempts to make a class pair (row, column) incomparable with contacts on its 4 element pairs,
    keeping the planted path shortest (exact).  Exercises Stage 1 with the true thresholds."""
    word, ties, pre = crossing2(rng, g, nr, nc)
    pl = Planted(word, ties)
    n = pl.n
    for (kd, a0, b0) in pre:
        c = pl.new()
        if kd == "F":
            pl.F[a0] |= 1 << c
            pl.F[b0] |= 1 << c
        else:
            pl.E[a0] |= 1 << c
            pl.E[b0] |= 1 << c
    rows = [t_ for t_ in ties if word[t_[0]] == "E"]
    cols = [t_ for t_ in ties if word[t_[0]] == "F"]
    midE = {x for t_ in rows for x in t_}
    midF = {x for t_ in cols for x in t_}
    Es = [i for i in range(n) if word[i] == "E"]
    Fs = [i for i in range(n) if word[i] == "F"]
    strict = set()
    for a in Es:
        for b in Fs:
            pl.le[b][a] = True
            c = pl.new()                     # dense: every row catches every column, every column touches every row
            pl.F[a] |= 1 << c
            pl.F[b] |= 1 << c
            c = pl.new()
            pl.E[a] |= 1 << c
            pl.E[b] |= 1 << c
            if a not in midE and b not in midF and not (a > b):
                # extreme row before an extreme column: both contacts, so that hulls are finite; never around a member
                if a > 2 * g + nr:          # a row of G3 stays without contacts to C0 (a > b already excludes C0)
                    pass
                c = pl.new()
                pl.F[a] |= 1 << c
                pl.F[b] |= 1 << c
                c = pl.new()
                pl.E[a] |= 1 << c
                pl.E[b] |= 1 << c
    I = pl.inst()
    st = Counter()
    try:
        r0 = shortest_len(I, n - 1, cap=budget)
    except Budget:
        st["skeleton: budget"] += 1
        return None
    if r0 is not None:
        st["skeleton shorter"] += 1
        return None
    for _ in range(flips):
        ra = rng.choice(rows)
        co = rng.choice(cols)
        saveE, saveF, savenn = pl.E[:], pl.F[:], pl.nn
        savele = [row[:] for row in pl.le]
        for a in ra:
            for b in co:
                pl.le[b][a] = False
        for a in ra:
            for b in co:
                c = pl.new()
                if rng.random() < 0.5:
                    pl.F[a] |= 1 << c
                    pl.F[b] |= 1 << c
                else:
                    pl.E[a] |= 1 << c
                    pl.E[b] |= 1 << c
        I2 = pl.inst()
        comparable = I2.le[ra[0]][co[0]] or I2.le[co[0]][ra[0]]
        ok = False
        if not comparable:
            try:
                ok = shortest_len(I2, n - 1, cap=budget) is None
            except Budget:
                st["flip: budget"] += 1
        if ok:
            st["flips accepted"] += 1
        else:
            st["flips rejected"] += 1
            pl.E, pl.F, pl.nn, pl.le = saveE, saveF, savenn, savele
    return pl.inst(), pl.path(), st


def planted_g(rng, nmin, nmax):
    """A configuration of Lemma G with sum >= 9, on a word with tie classes; returns (I, n) or None."""
    n = rng.randint(nmin, nmax)
    word = "".join(rng.choice("EF") for _ in range(n))
    Es = [i for i in range(n) if word[i] == "E"]
    Fs = [i for i in range(n) if word[i] == "F"]
    if len(Es) < 4 or len(Fs) < 4:
        return None
    a, h = rng.choice(Es), rng.choice(Fs)
    # tied mates of a and h
    tiesA = [a] + rng.sample([x for x in Es if x != a], rng.randint(0, min(2, len(Es) - 1)))
    tiesH = [h] + rng.sample([x for x in Fs if x != h], rng.randint(0, min(2, len(Fs) - 1)))
    Z = sorted(tiesA + tiesH)
    for _ in range(40):
        # p1 in T(h) (an E-member), p4 in S(a) (an F-member), the middle pair
        p1 = rng.choice(Es)
        p4 = rng.choice(Fs)
        x = rng.choice(Es)    # in T(h)
        y = rng.choice(Fs)    # in S(a)
        p2, p3 = min(x, y), max(x, y)
        if not (p1 < Z[0] and Z[-1] < p4 and p1 < p2 and p3 < p4):
            continue
        if any(p2 <= z <= p3 for z in Z):
            continue
        if (p2 - p1) + (p4 - p3) < 9:
            continue
        if {p1, x} & set(tiesA) or {p4, y} & set(tiesH):
            continue
        break
    else:
        return None
    pl = Planted(word, [tiesA, tiesH])
    for t_ in (p1, x):
        c = pl.new()
        pl.E[h] |= 1 << c
        pl.E[t_] |= 1 << c
    for t_ in (p4, y):
        c = pl.new()
        pl.F[a] |= 1 << c
        pl.F[t_] |= 1 << c
    # random strict pairs that keep h not below a and keep a, h, contacts extremal
    for _ in range(rng.randint(0, n)):
        f, e = rng.choice(Fs), rng.choice(Es)
        if f in tiesH or e in tiesA:
            continue
        pl.le[f][e] = True
    I = pl.inst()
    if I.le[h][a] or I.le[a][h]:
        return None
    Sk = Skel(I, pl.path())
    if not ((Sk.A >> a) & 1 and (Sk.B >> h) & 1 and (Sk.A >> p1) & 1 and (Sk.A >> x) & 1 and (Sk.B >> p4) & 1 and (Sk.B >> y) & 1):
        return None
    return I, n


def main():
    mode = sys.argv[1]
    cnt = Counter()
    if mode == "g":
        seed, count, nmin, nmax = map(int, sys.argv[2:6])
        rng = random.Random(seed)
        for it in range(count):
            g = planted_g(rng, nmin, nmax)
            if g is None:
                cnt["no configuration"] += 1
                continue
            I, n = g
            try:
                r0, _ = all_shortest_valid_paths(I, cap=1, maxlen=n, budget=2000000)
            except Budget:
                cnt["search budget"] += 1
                continue
            cnt["configurations"] += 1
            if r0 is None or r0 >= n:
                cnt["planted path stays shortest: Lemma G FAIL"] += 1
            else:
                cnt["shorter path, as Lemma G says"] += 1
    elif mode == "sat":
        seed, count, nmin, nmax, EXT, K_, KAP = map(int, sys.argv[2:9])
        rng = random.Random(seed)
        for it in range(count):
            n = rng.randint(nmin, nmax)
            blocks = rng.choice([1, 2, 3])
            nr = max(2, n // (2 * blocks))
            word, ties = crossing_word(rng, nr, nr, blocks)
            g = saturate(rng, word, ties)
            if g is None:
                cnt["word already has a shorter path"] += 1
                continue
            I, P, st = g
            for k_, v_ in st.items():
                cnt["sat " + k_] += v_
            if not I.p2_switch():
                cnt["saturated instance without P2 FAIL"] += 1
            run_path(I, P, cnt, EXT, K_, KAP)
    elif mode == "sat2":
        seed, count, g0, nr, nc, EXT, K_, KAP = map(int, sys.argv[2:10])
        rng = random.Random(seed)
        for it in range(count):
            word, ties, pre = crossing2(rng, g0, nr, nc)
            g = saturate(rng, word, ties, pre=pre, prob=rng.choice([1.0, 0.6]))
            if g is None:
                wI = Planted(word, ties)
                cnt["skeleton rejected"] += 1
                continue
            I, P, st = g
            for k_, v_ in st.items():
                cnt["sat " + k_] += v_
            if not I.p2_switch():
                cnt["saturated instance without P2 FAIL"] += 1
            run_path(I, P, cnt, EXT, K_, KAP)
    elif mode == "xtie":
        seed, count, g0, nr, nc, flips, EXT, K_, KAP = map(int, sys.argv[2:11])
        rng = random.Random(seed)
        for it in range(count):
            g = xtie(rng, g0, nr, nc, flips)
            if g is None:
                cnt["skeleton rejected"] += 1
                continue
            I, P, st = g
            for k_, v_ in st.items():
                cnt[k_] += v_
            cnt["P2" if I.p2_switch() else "no P2 FAIL"] += 1
            run_path(I, P, cnt, EXT, K_, KAP, pointwise=False)
    elif mode == "rigid":
        seed, count, nmin, nmax = map(int, sys.argv[2:6])
        ptie = float(sys.argv[6])
        rng = random.Random(seed)
        for it in range(count):
            n = rng.randint(nmin, nmax)
            style = rng.choice(["alt", "runs", "rand"])
            word = "EF" * (n // 2) if style == "alt" else ("E" * (n // 2) + "F" * (n // 2) if style == "runs"
                                                           else "".join(rng.choice("EF") for _ in range(n)))
            if "E" not in word or "F" not in word:
                continue
            I, P, info = gen8.rigid_design(rng, word, rng.randint(2, 10), rng.randint(2, 10), rng.randint(1, 6),
                                           rng.randint(1, 3), pbad=rng.choice([0.3, 0.6, 1.0]),
                                           ptie_ex=rng.choice([0.0, 0.2]), ptie_mem=ptie, pme=rng.choice([0.0, 0.3]))
            run_path(I, P, cnt, pointwise=True)
    elif mode == "files":
        for path in sys.argv[2:]:
            I = load(path)
            try:
                r0, ps = all_shortest_valid_paths(I, cap=20, budget=2000000)
            except Budget:
                cnt["search budget"] += 1
                continue
            if r0 is None:
                cnt["no-instances"] += 1
                continue
            for P in ps:
                run_path(I, P, cnt)
    for k_ in sorted(cnt):
        print("%-60s %d" % (k_, cnt[k_]))
    fails = [k_ for k_ in cnt if k_.endswith("FAIL")]
    print("FAILURES:", fails if fails else "none")


if __name__ == "__main__":
    main()
