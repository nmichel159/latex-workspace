"""r7-desc: checks of Lemma X and Theorem A (r7-desc.md Section 2).

  python check_a.py x SEED COUNT NMIN NMAX      falsification of Lemma X on planted cells (exact shortest path search)
  python check_a.py rigid SEED COUNT NMIN NMAX PTIE   Theorem A on rigid designs of verify/rv-r6-core/gen8 (planted path)
  python check_a.py random SEED COUNT MMIN MMAX       Lemma X and Theorem A on random instances, all shortest paths
  python check_a.py files FILE...                     the same on stored instances (JSON of r5-core or rv-r6-core)

Library: verify/rv-r6-core/zzl.py (reviewed), imported read-only.  A failure is a counter ending in FAIL.
"""
import json
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
sys.path.append(os.path.join(OC, "verify", "rv-r6-core"))

from zzl import Budget, SW, Skel, all_shortest_valid_paths, bits, popcount, term_D  # noqa: E402
import gen8  # noqa: E402

K = 4
INF = 10 ** 9


def tie_free(I, S):
    for mask in (S.WE, S.WF):
        for w in bits(mask):
            if I.tie[w] & mask & ~(1 << w):
                return False
    return True


def contacts(I, S):
    C = {a: sorted(S.pos[b] for b in bits(S.B & I.NFs[a])) for a in bits(S.A)}
    Cp = {b: sorted(S.pos[a] for a in bits(S.A & I.NEs[b])) for b in bits(S.B)}
    return C, Cp


def cross_cells(I, S, C, Cp):
    """Cells (a, h), a || h, with far contacts on all four sides (Lemma X says: none on a tie-free path)."""
    out = []
    for a in bits(S.A):
        for h in bits(S.B):
            if I.le[a][h] or I.le[h][a]:
                continue
            pa, ph = S.pos[a], S.pos[h]
            if C[a] and Cp[h] and C[a][0] <= ph - K and C[a][-1] >= ph + K and Cp[h][0] <= pa - K and Cp[h][-1] >= pa + K:
                out.append((a, h))
    return out


def atom_FR(I, a1, a2):
    return term_D(I, "F", [a1, a2], [], (1 << a1) | (1 << a2), 0)[0]


def atom_ER(I, b1, b2):
    return term_D(I, "E", [b1, b2], [], (1 << b1) | (1 << b2), 0)[0]


def atom_FP(I, h):
    return term_D(I, "F", [h], [h], 0, 0)[0]


def far_pair(S, ten):
    ten = sorted(ten, key=lambda w: S.pos[w])
    return ten[0], ten[-1]


def theorem_a(I, S, cnt):
    """The construction of Theorem A.  Returns the formula value D*; checks each claim on the way."""
    A = list(bits(S.A))
    B = list(bits(S.B))
    if len(A) < 10:
        D = I.full
        for a in A:
            D &= I.full & ~I.up[a]
        cnt["small A"] += 1
        return D
    if len(B) < 10:
        D = 0
        for b in B:
            D |= I.dn[b]
        cnt["small B"] += 1
        return D
    C, Cp = contacts(I, S)
    l = {a: (C[a][0] if C[a] else INF) for a in A}
    r = {a: (C[a][-1] if C[a] else -INF) for a in A}
    u = {b: (Cp[b][0] if Cp[b] else INF) for b in B}
    v = {b: (Cp[b][-1] if Cp[b] else -INF) for b in B}
    byl = sorted(A, key=lambda a: -l[a])
    byr = sorted(A, key=lambda a: r[a])
    byu = sorted(B, key=lambda b: -u[b])
    byv = sorted(B, key=lambda b: v[b])
    L, R, U, V = l[byl[9]], r[byr[9]], u[byu[9]], v[byv[9]]
    FR_L = atom_FR(I, *far_pair(S, byl[:10]))
    FR_R = atom_FR(I, *far_pair(S, byr[:10]))
    ER_U = atom_ER(I, *far_pair(S, byu[:10]))
    ER_V = atom_ER(I, *far_pair(S, byv[:10]))
    for D in (FR_L, FR_R):
        if D & S.Up:
            cnt["FR meets Up FAIL"] += 1
    for D in (ER_U, ER_V):
        if S.L & ~D:
            cnt["ER misses L FAIL"] += 1
    for b in B:
        if S.pos[b] < L and not (FR_L >> b) & 1:
            cnt["FR_L keep FAIL"] += 1
        if S.pos[b] > R and not (FR_R >> b) & 1:
            cnt["FR_R keep FAIL"] += 1
    for a in A:
        if S.pos[a] < U and (ER_U >> a) & 1:
            cnt["ER_U kill FAIL"] += 1
        if S.pos[a] > V and (ER_V >> a) & 1:
            cnt["ER_V kill FAIL"] += 1
    E0 = set(byl[:9]) | set(byr[:9]) | {a for a in A if U <= S.pos[a] < U + K or V - K < S.pos[a] <= V}
    H0 = set(byu[:9]) | set(byv[:9]) | {b for b in B if L <= S.pos[b] < L + K or R - K < S.pos[b] <= R}
    A0 = [a for a in A if a not in E0 and U + K <= S.pos[a] <= V - K]
    B0 = [b for b in B if b not in H0 and L + K <= S.pos[b] <= R - K]
    cnt["paths with big A, B"] += 1
    if A0:
        cnt["A0 non-empty"] += 1
    if B0:
        cnt["B0 non-empty"] += 1
    Bad = [(a, b) for a in A0 for b in B0 if not I.le[b][a] or I.le[a][b]]
    if Bad:
        cnt["cells of A0 x B0 not strict"] += 1
        cnt["(%s) strict claim %s" % ("tie-free" if tie_free(I, S) else "ties", "FAIL" if tie_free(I, S) else "fails")] += 1
    if A0 and B0:
        cnt["A0, B0 both non-empty"] += 1
    if len(B0) < 18:
        H0 |= set(B0)
        B0 = []
    Fs = FR_L | FR_R
    for b in H0:
        Fs |= I.dn[b]
    Es = ER_U & ER_V
    for a in E0:
        Es &= I.full & ~I.up[a]
    if not B0:
        return Fs
    if not A0:
        return Es
    far = sorted(B0, key=lambda b: S.pos[b])
    X = atom_FP(I, far[0]) | atom_FP(I, far[-1])
    if S.B & ~X:
        cnt["X misses B FAIL"] += 1
    cnt["formula with X"] += 1
    return Fs | (Es & X)


def run_path(I, P, cnt, bad=None):
    S = Skel(I, P)
    tf = tie_free(I, S)
    cnt["paths"] += 1
    cnt["tie-free paths" if tf else "paths with same-type ties"] += 1
    C, Cp = contacts(I, S)
    cc = cross_cells(I, S, C, Cp)
    if cc:
        cnt["cross cells on tie-free path FAIL" if tf else "cross cells on paths with ties"] += len(cc)
    D = theorem_a(I, S, cnt)
    ok = I.is_down(D) and not (S.L & ~D) and not (D & S.Up) and I.connects(D)
    if not ok:
        cnt["Theorem A formula wrong on tie-free path FAIL" if tf else "formula wrong on path with ties"] += 1
        if bad is not None:
            bad.append((P, tf))
    else:
        cnt["formula picks P"] += 1


# -------------------------------------------------------------------------- direct falsification of Lemma X

def planted_cell(rng, n, chains):
    """A planted path with a word, no order except optional relations outside the cell; one cell (a, h), a || h,
    with four far contacts through fresh nodes (or through middle edges when chains is True)."""
    word = [rng.choice("EF") for _ in range(n)]
    # one extra E-member a, one extra F-member h are chosen among the positions
    Es = [i for i in range(n) if word[i] == "E"]
    Fs = [i for i in range(n) if word[i] == "F"]
    if len(Es) < 3 or len(Fs) < 3:
        return None
    a, h = rng.choice(Es), rng.choice(Fs)
    a1s = [i for i in Es if i <= a - K]
    a2s = [i for i in Es if i >= a + K]
    h1s = [i for i in Fs if i <= h - K]
    h2s = [i for i in Fs if i >= h + K]
    if not (a1s and a2s and h1s and h2s):
        return None
    a1, a2, h1, h2 = rng.choice(a1s), rng.choice(a2s), rng.choice(h1s), rng.choice(h2s)
    m = n
    extras = []
    if chains:
        extras = ["w1", "w2", "z1", "z2"]
    idx = {name: m + i for i, name in enumerate(extras)}
    m += len(extras)
    nn = 0

    def new():
        nonlocal nn
        nn += 1
        return nn - 1
    s = new()
    t = new()
    E = [0] * m
    F = [0] * m
    side = [E if word[i] == "E" else F for i in range(n)]
    side[0][0] |= 1 << s
    side[n - 1][n - 1] |= 1 << t
    for i in range(n - 1):
        c = new()
        side[i][i] |= 1 << c
        side[i + 1][i + 1] |= 1 << c
    le = [[i == j for j in range(m)] for i in range(m)]
    me = []
    if not chains:
        for hi in (h1, h2):
            c = new()
            F[a] |= 1 << c
            F[hi] |= 1 << c
        for ai in (a1, a2):
            c = new()
            E[h] |= 1 << c
            E[ai] |= 1 << c
    else:
        # F_a -- E_w -- X_hi through private nodes; E_h -- F_z -- X_ai through private nodes
        for name, hi in (("w1", h1), ("w2", h2)):
            w = idx[name]
            le[a][w] = True
            le[hi][w] = True
            for z0 in (a, hi):
                p = new()
                me.append((z0, w, p))
                F[z0] |= 1 << p
                E[w] |= 1 << p
        for name, ai in (("z1", a1), ("z2", a2)):
            z = idx[name]
            le[z][h] = True
            le[z][ai] = True
            for v0 in (h, ai):
                p = new()
                me.append((z, v0, p))
                F[z] |= 1 << p
                E[v0] |= 1 << p
    # random strict relations among members that keep the planted path valid and keep a || h, minimality, maximality
    for _ in range(rng.randint(0, n)):
        x, y = rng.randrange(n), rng.randrange(n)
        if x == y or word[x] != "F" or word[y] != "E":
            continue          # only F-member below E-member is compatible with validity
        if {x, y} == {h, a} or y == a and x == h:
            continue
        if word[x] == "F" and word[y] == "E":
            le[x][y] = True
    # transitive closure
    for k_ in range(m):
        for i in range(m):
            if le[i][k_]:
                for j in range(m):
                    if le[k_][j]:
                        le[i][j] = True
    if le[h][a] or le[a][h]:
        return None
    I = SW(m, le, E, F, s, t, nn, me)
    P = [(i, 0 if word[i] == "E" else 1) for i in range(n)]
    return I, P, a, h


def falsify(seed, count, nmin, nmax):
    rng = random.Random(seed)
    cnt = Counter()
    for it in range(count):
        n = rng.randint(nmin, nmax)
        g = planted_cell(rng, n, rng.random() < 0.5)
        if g is None:
            cnt["no cell"] += 1
            continue
        I, P, a, h = g
        S = Skel(I, P)
        if not ((S.A >> a) & 1 and (S.B >> h) & 1):
            cnt["a or h not extremal"] += 1
            continue
        if I.tie[a] & S.WE & ~(1 << a) or I.tie[h] & S.WF & ~(1 << h):
            cnt["tied"] += 1
            continue
        r0, ps = all_shortest_valid_paths(I, cap=1, maxlen=n, budget=2000000)
        cnt["cells tested"] += 1
        if r0 is None or r0 >= n:
            cnt["planted path stays shortest: Lemma X FAIL"] += 1
            print("FAIL", it, n, a, h)
        else:
            cnt["shorter path found, as Lemma X says"] += 1
    return cnt


# --------------------------------------------------------------------------- design with all cells strict

def xdesign(n):
    """Word E^n F^n.  Every F_{a_i} meets X_{b_1}, X_{b_n}; every E_{b_j} meets X_{a_1}, X_{a_n}; b_j < a_i for
    1 < i < n, 1 < j < n.  Exercises the branch with X of Theorem A: the middle of A x B is strict."""
    m = 2 * n
    nn = 0

    def new():
        nonlocal nn
        nn += 1
        return nn - 1
    s, t = new(), new()
    E = [0] * m
    F = [0] * m
    side = lambda i: E if i < n else F
    side(0)[0] |= 1 << s
    side(m - 1)[m - 1] |= 1 << t
    for i in range(m - 1):
        c = new()
        side(i)[i] |= 1 << c
        side(i + 1)[i + 1] |= 1 << c
    # contact nodes, one per end member: they also give P2 inside A and inside B
    for bj in (n, m - 1):
        c = new()
        F[bj] |= 1 << c
        for i in range(n):
            F[i] |= 1 << c
    for ai in (0, n - 1):
        c = new()
        E[ai] |= 1 << c
        for j in range(n, m):
            E[j] |= 1 << c
    le = [[i == j for j in range(m)] for i in range(m)]
    for i in range(1, n - 1):
        for j in range(n + 1, m - 1):
            le[j][i] = True
    I = SW(m, le, E, F, s, t, nn, [])
    P = [(i, 0 if i < n else 1) for i in range(m)]
    return I, P


# --------------------------------------------------------------------------- main

def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    conv = lambda x: int(x, 16) if isinstance(x, str) else int(x)
    if "medge" in d:
        E = [conv(x) for x in d["E"]]
        F = [conv(x) for x in d["F"]]
        me = [(int(v[0]), int(v[1]), int(p)) for p, v in d["medge"].items()]
        return SW(len(E), [[bool(b) for b in row] for row in d["le"]], E, F, d["s"], d["t"], d["N"], me)
    return SW(d["m"], [[bool(b) for b in row] for row in d["le"]], [conv(x) for x in d["E"]],
              [conv(x) for x in d["F"]], d["s"], d["t"], d["nn"], [tuple(e) for e in d["me"]])


def main():
    mode = sys.argv[1]
    cnt = Counter()
    if mode == "x":
        seed, count, nmin, nmax = map(int, sys.argv[2:6])
        cnt = falsify(seed, count, nmin, nmax)
    elif mode == "rigid":
        seed, count, nmin, nmax = map(int, sys.argv[2:6])
        ptie = float(sys.argv[6])
        rng = random.Random(seed)
        for it in range(count):
            n = rng.randint(nmin, nmax)
            style = rng.choice(["alt", "runs", "rand"])
            if style == "alt":
                word = "EF" * (n // 2)
            elif style == "runs":
                word = "E" * (n // 2) + "F" * (n // 2)
            else:
                word = "".join(rng.choice("EF") for _ in range(n))
            if "E" not in word or "F" not in word:
                continue
            nx = rng.randint(2, 10)
            ny = rng.randint(2, 10)
            I, P, info = gen8.rigid_design(rng, word, nx, ny, rng.randint(1, 6), rng.randint(1, 3),
                                           pbad=rng.choice([0.3, 0.6, 1.0]), ptie_ex=rng.choice([0.0, 0.2]),
                                           ptie_mem=ptie, pme=rng.choice([0.0, 0.3]))
            run_path(I, P, cnt)
    elif mode == "random":
        seed, count, mmin, mmax = map(int, sys.argv[2:6])
        rng = random.Random(seed)
        for it in range(count):
            m = rng.randint(mmin, mmax)
            I = gen8.random_sw(rng, m, rng.randint(2, 2 * m), rng.choice([0.08, 0.15, 0.25]),
                               rng.choice([0.05, 0.15, 0.3]), rng.choice([0.0, 0.2]), rng.choice([0.0, 0.2]))
            try:
                r0, ps = all_shortest_valid_paths(I, cap=20, budget=300000)
            except Budget:
                cnt["skipped (search budget)"] += 1
                continue
            if r0 is None:
                cnt["no-instances"] += 1
                continue
            for P in ps:
                run_path(I, P, cnt)
    elif mode == "xdesign":
        for n in map(int, sys.argv[2:]):
            I, P = xdesign(n)
            if not I.p2_switch():
                cnt["xdesign without P2 FAIL"] += 1
            if n <= 30:
                try:
                    r0, ps = all_shortest_valid_paths(I, cap=3, maxlen=2 * n - 1, budget=3000000)
                    cnt["xdesign: no shorter path" if r0 is None else "xdesign: shorter path exists"] += 1
                except Budget:
                    cnt["xdesign: search budget"] += 1
            run_path(I, P, cnt)
    elif mode == "files":
        for path in sys.argv[2:]:
            I = load(path)
            r0, ps = all_shortest_valid_paths(I, cap=20, budget=2000000)
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
