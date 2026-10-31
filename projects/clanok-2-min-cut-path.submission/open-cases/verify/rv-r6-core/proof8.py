"""The proof of Lemma 8.1 and Theorem 8.2 of r5-core.md as a program, with every claim checked (own code).

levels(I, Sk, mode) runs the levels of Theorem 8.2 on the fixed valid path of Sk and returns a record; every claim
that fails is counted in the Counter `st` under a key in capitals ending in 'FAIL'.

Modes:
  'proof'  : theta = |A'|/(2k), covers of at most k tools found by exhaustive branching, the cover used for the next
             level chosen ADVERSARIALLY (largest residue A''), and every enumerated cover (up to `ccap`) checked;
  'stress' : theta = |A'|/2 (more rows light, more damage, more levels); covers of at most k tools; only the logical
             claims are checked (the halving |A''| <= |A'|/2 is not claimed there; |A''| <= sum of the damages of the
             light tools is).
The game value is computed by LP (scipy, HiGHS); the case split v >= 1/2 versus v < 1/2 is the one of the proof; the
probabilistic step is checked numerically (expected number of uncovered items < 1 for the optimal strategy) and the
existence of the cover it promises is checked by exhaustive search.
"""
import math
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from zzl import bits, popcount, term_D, kparam

TOL = 1e-9
import random as _random
proof8_rng = _random.Random(12345)


def game_value(rows, cols, Mrow):
    """Mrow[x] = mask of columns covered by row x (payoff 1).  Returns (v, p dict, q dict)."""
    nr, nc = len(rows), len(cols)
    M = np.zeros((nr, nc))
    for i, x in enumerate(rows):
        for j, y in enumerate(cols):
            if (Mrow[x] >> y) & 1:
                M[i, j] = 1.0
    # shortcuts
    if M.min(axis=1).max() >= 1.0:          # a row covering every column
        i = int(np.argmax(M.min(axis=1)))
        p = {x: (1.0 if a == i else 0.0) for a, x in enumerate(rows)}
        q = {y: 1.0 / nc for y in cols}
        return 1.0, p, q
    if M.max(axis=0).min() <= 0.0:          # a column covered by no row
        j = int(np.argmin(M.max(axis=0)))
        q = {y: (1.0 if b == j else 0.0) for b, y in enumerate(cols)}
        p = {x: 1.0 / nr for x in rows}
        return 0.0, p, q
    # row player: max v s.t. M^T p >= v, sum p = 1
    c = np.zeros(nr + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-M.T, np.ones((nc, 1))])
    b_ub = np.zeros(nc)
    A_eq = np.hstack([np.ones((1, nr)), np.zeros((1, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * nr + [(None, None)], method="highs")
    v = -res.fun
    p = {x: max(0.0, float(res.x[i])) for i, x in enumerate(rows)}
    # column player: min w s.t. M q <= w, sum q = 1
    c2 = np.zeros(nc + 1)
    c2[-1] = 1.0
    A_ub2 = np.hstack([M, -np.ones((nr, 1))])
    res2 = linprog(c2, A_ub=A_ub2, b_ub=np.zeros(nr), A_eq=np.hstack([np.ones((1, nc)), np.zeros((1, 1))]),
                   b_eq=[1.0], bounds=[(0, None)] * nc + [(None, None)], method="highs")
    q = {y: max(0.0, float(res2.x[j])) for j, y in enumerate(cols)}
    return v, p, q


def covers(universe, cand, covmask, depth, cap):
    """All (up to cap) sets of at most `depth` candidates whose covmask union contains `universe`
    (branching on an uncovered element with fewest covering candidates).  Returns a list of frozensets."""
    out = set()
    by_elem = {}
    for e in bits(universe):
        by_elem[e] = [c for c in cand if (covmask[c] >> e) & 1]

    def rec(chosen, covered):
        if len(out) >= cap:
            return
        rest = universe & ~covered
        if rest == 0:
            out.add(frozenset(chosen))
            return
        if len(chosen) >= depth:
            return
        e = min(bits(rest), key=lambda e: len(by_elem[e]))
        for c in by_elem[e]:
            if c in chosen:
                continue
            chosen.append(c)
            rec(chosen, covered | covmask[c])
            chosen.pop()
    rec([], 0)
    # keep inclusion-minimal ones first, then the rest
    res = sorted(out, key=len)
    return res


def min_hitting(sets, ground, limit):
    """Minimum hitting set (size <= limit) of the list of masks `sets` with elements from mask `ground`;
    returns a set or None."""
    sets = [s & ground for s in sets]
    if any(s == 0 for s in sets):
        return None
    best = [None]

    def rec(chosen, rest):
        if best[0] is not None and len(chosen) >= len(best[0]):
            return
        if not rest:
            best[0] = list(chosen)
            return
        if len(chosen) >= limit:
            return
        s = min(rest, key=popcount)
        for a in bits(s):
            chosen.append(a)
            rec(chosen, [t for t in rest if not (t >> a) & 1])
            chosen.pop()
    rec([], sets)
    return best[0]


def one_level(I, Sk, Ap, k, N, mode, st, ccap=40, pick="adversarial"):
    """Lemma 8.1 for the residue Ap (mask, non-empty).  Returns (kind, term, D, App) with kind in
    'final', 'continue', 'stuck' (stress mode only, no progress) and term a tuple describing the term."""
    m = I.m
    nA = popcount(Ap)
    R = I.upc(Ap) & I.fnon
    C = Sk.NE_
    # sanity of the setting
    if R & Sk.L:
        st["ROW IN L FAIL"] += 1
    if C & Sk.Up:
        st["COLUMN IN Up FAIL"] += 1
    if (R & ~Sk.NF_):
        st["ROW NOT IN N_F FAIL"] += 1
    if mode == "proof":
        thr = Fraction(nA, 2 * k)
    else:
        thr = Fraction(nA, 2)
    dam = {x: Ap & I.sdn[x] for x in bits(R)}
    light = {x for x in bits(R) if popcount(dam[x]) <= thr}
    for a in bits(Ap & R):
        if dam[a]:
            st["DAMAGE OF A' ELEMENT FAIL"] += 1
    covE = {x: (I.NEs[x] | (I.sdn[x] if x in light else 0)) & C for x in bits(R)}
    covF = {y: (I.NFs[y] | (I.sup[y] if (Sk.B >> y) & 1 else 0)) & R for y in bits(C)}
    # duality claim for every light row and every column
    for x in light:
        for y in bits(C):
            st["duality pairs"] += 1
            if not ((covE[x] >> y) & 1 or (covF[y] >> x) & 1):
                st["DUALITY FAIL"] += 1
            if I.le[y][x] and not I.le[x][y]:
                st["duality pairs y<x"] += 1
            if I.le[x][y]:
                st["ROW <= COLUMN FAIL"] += 1
    heavy = set(bits(R)) - light
    st["rows"] += popcount(R)
    st["heavy rows"] += len(heavy)
    # trivial cases
    if C == 0:
        st["case C0"] += 1
        D, U, S, G = term_D(I, "E", [], [], 0, 0)
        check_term_common(I, Sk, D, st)
        if D & I.upc(Ap):
            st["TRIVIAL C=0 FINAL FAIL"] += 1
        return "final", ("E", (), (), 0, 0), D, 0
    if R == 0:
        st["case R0"] += 1
        D, U, S, G = term_D(I, "F", [], [], 0, 0)
        check_term_common(I, Sk, D, st)
        if D & I.upc(Ap):
            st["TRIVIAL R=0 FINAL FAIL"] += 1
        return "final", ("F", (), (), 0, 0), D, 0
    rows = list(bits(R))
    cols = list(bits(C))
    v, p, q = game_value(rows, cols, covE)
    st["games"] += 1
    if abs(v - 0.5) < 1e-7:
        st["games with v = 1/2 (float)"] += 1
    if v >= 0.5 - 1e-7:
        st["case E (v>=1/2)"] += 1
        # numeric check of the probabilistic step
        cy = {y: sum(p[x] for x in rows if (covE[x] >> y) & 1) for y in cols}
        if min(cy.values()) < 0.5 - 1e-6:
            st["E STRATEGY BELOW 1/2 FAIL"] += 1
        expo = sum((1 - cy[y]) ** k for y in cols)
        if expo >= 1 - 1e-12:
            st["E EXPECTED UNCOVERED >= 1 FAIL"] += 1
        st["max E expected uncovered x1000"] = max(st["max E expected uncovered x1000"], int(1000 * expo))
        cvs = covers(C, rows, covE, k, ccap)
        if not cvs:
            st["E COVER BY k TOOLS MISSING FAIL"] += 1
            return "error", None, None, None
        cand = list(cvs)
        if pick == "adversarial":
            # pad covers with light tools of largest new damage, up to k tools (still covers, so the claims of the
            # proof must hold for them as well)
            padded = []
            for T in cvs[:10]:
                T = set(T)
                cur = 0
                for x in T:
                    if x in light:
                        cur |= dam[x]
                while len(T) < k:
                    cands = [x for x in light if x not in T]
                    if not cands:
                        break
                    x = max(cands, key=lambda x: (popcount(dam[x] & ~cur), popcount(dam[x])))
                    if not dam[x] & ~cur:
                        break
                    T.add(x)
                    cur |= dam[x]
                padded.append(frozenset(T))
            cand = padded + cand
        elif pick == "sample":
            rs = proof8_rng
            got = None
            for _ in range(200):
                T = set(rs.choices(rows, weights=[p[x] + 1e-15 for x in rows], k=k))
                cov = 0
                for x in T:
                    cov |= covE[x]
                if cov & C == C:
                    got = frozenset(T)
                    break
            if got is None:
                st["sample: no E cover in 200 draws"] += 1
            else:
                st["sample: E cover drawn"] += 1
                cand = [got] + cand
        best = None
        for T in cand:
            T = sorted(T)
            Tp = [x for x in T if x in light]
            # Phi = A' & U
            U = 0
            for x in T:
                U |= I.NEs[x]
            Phi = Ap & U
            D, U2, S, G = term_D(I, "E", T, Tp, 0, Phi)
            st["E terms checked"] += 1
            check_term_common(I, Sk, D, st)
            if popcount(Phi) > 9 * len(T):
                st["E FLIPS > 9|T| FAIL"] += 1
            st["max |Phi|/|T| x100"] = max(st["max |Phi|/|T| x100"], (100 * popcount(Phi)) // max(1, len(T)))
            if popcount(Phi) > 5 * len(T):
                st["E flips > 5|T| (Lemma 6.3 with 5)"] += 1
            if G & Sk.L:
                st["E G MEETS L FAIL"] += 1
            App = Ap & ~G
            damU = 0
            for x in Tp:
                damU |= dam[x]
            if App & ~(damU & ~U):
                st["E A'' NOT IN (A' & S) - U FAIL"] += 1
            sdam = sum(popcount(dam[x]) for x in Tp)
            if popcount(App) > sdam:
                st["E |A''| > SUM OF LIGHT DAMAGES FAIL"] += 1
            if mode == "proof" and 2 * popcount(App) > nA:
                st["E |A''| > |A'|/2 FAIL"] += 1
            if mode == "proof" and App and 2 * popcount(App) == nA:
                st["boundary: |A''| = |A'|/2 exactly"] += 1
            if mode == "proof" and any(popcount(dam[x]) == thr for x in Tp):
                st["boundary: tool with |dam| = theta exactly"] += 1
            if D & I.upc(Ap) & ~I.upc(App):
                st["E D & up(A') NOT IN up(A'') FAIL"] += 1
            key = (popcount(App), len(T))
            if best is None or (pick == "adversarial" and key > best[0]):
                best = (key, T, Tp, Phi, D, App)
        _, T, Tp, Phi, D, App = best
        if App == 0:
            st["E final"] += 1
            return "final", ("E", tuple(T), tuple(Tp), 0, Phi), D, 0
        if App == Ap:
            st["stuck (no progress)"] += 1
            return "stuck", ("E", tuple(T), tuple(Tp), 0, Phi), D, App
        st["E continue"] += 1
        return "continue", ("E", tuple(T), tuple(Tp), 0, Phi), D, App
    # case v < 1/2
    st["case F (v<1/2)"] += 1
    Lrows = sum(1 << x for x in light)
    dx = {x: sum(q[y] for y in cols if (covF[y] >> x) & 1) for x in rows}
    for x in light:
        if dx[x] <= 0.5 + 1e-12:
            st["F LIGHT ROW NOT COVERED > 1/2 FAIL"] += 1
    expo = sum((1 - dx[x]) ** k for x in light)
    expo += sum((1 - Fraction(popcount(dam[x]), nA)) ** N for x in heavy) if heavy else 0
    expo = float(expo)
    if expo >= 1 - 1e-12:
        st["F EXPECTED FAILURES >= 1 FAIL"] += 1
    st["max F expected failures x1000"] = max(st["max F expected failures x1000"], int(1000 * expo))
    cvs = covers(Lrows, cols, covF, k, ccap)
    if not cvs:
        st["F COVER OF LIGHT ROWS BY k TOOLS MISSING FAIL"] += 1
        return "error", None, None, None
    anc = []
    if heavy:
        anc = min_hitting([dam[x] for x in heavy], Ap, N)
        if anc is None:
            st["F ANCHORS > N FAIL"] += 1
            return "error", None, None, None
        st["max anchors"] = max(st["max anchors"], len(anc))
    if pick == "sample":
        rs = proof8_rng
        got = None
        for _ in range(200):
            T = set(rs.choices(cols, weights=[q[y] + 1e-15 for y in cols], k=k))
            cov = 0
            for y in T:
                cov |= covF[y]
            if cov & Lrows == Lrows:
                got = frozenset(T)
                break
        if got is None:
            st["sample: no F cover in 200 draws"] += 1
        else:
            st["sample: F cover drawn"] += 1
            cvs = [got] + list(cvs)
        if heavy:
            Al = list(bits(Ap))
            ok = None
            for _ in range(200):
                an = set(rs.choice(Al) for _ in range(N))
                if all(dam[x] & sum(1 << a for a in an) for x in heavy):
                    ok = an
                    break
            if ok is None:
                st["sample: no anchor draw in 200"] += 1
            else:
                st["sample: anchors drawn"] += 1
                st["max sampled anchors (distinct)"] = max(st["max sampled anchors (distinct)"], len(ok))
                anc = sorted(ok)
    X0 = sum(1 << a for a in anc)
    if X0 & ~Ap:
        st["F ANCHOR OUTSIDE A' FAIL"] += 1
    best = None
    for T in cvs:
        T = sorted(T)
        Tp = [y for y in T if (Sk.B >> y) & 1]
        U = 0
        for y in T:
            U |= I.NFs[y]
        Phi = Sk.B & U
        D, U2, S, G = term_D(I, "F", T, Tp, X0, Phi)
        st["F terms checked"] += 1
        check_term_common(I, Sk, D, st)
        if popcount(Phi) > 9 * len(T):
            st["F FLIPS > 9|T| FAIL"] += 1
        st["max |Phi|/|T| x100"] = max(st["max |Phi|/|T| x100"], (100 * popcount(Phi)) // max(1, len(T)))
        if G & I.upc(Ap):
            st["F G' MEETS up(A') FAIL"] += 1
        if D & I.upc(Ap):
            st["F D MEETS up(A') FAIL"] += 1
        if Sk.B & ~G:
            st["F B NOT IN G' FAIL"] += 1
        if best is None:
            best = (T, Tp, Phi, D)
    T, Tp, Phi, D = best
    st["F final"] += 1
    if heavy:
        st["F final with anchors"] += 1
    return "final", ("F", tuple(T), tuple(Tp), X0, Phi), D, 0


def check_term_common(I, Sk, D, st):
    if not I.is_down(D):
        st["TERM D NOT A DOWN-SET FAIL"] += 1
    if Sk.L & ~D:
        st["TERM D MISSES PART OF L FAIL"] += 1


def levels(I, Sk, mode, st, ccap=40, pick="adversarial"):
    """Theorem 8.2 on the path of Sk.  Returns (D, terms, nlevels, status)."""
    m = I.m
    k, N = kparam(m)
    if Sk.A == 0:
        D, U, S, G = term_D(I, "F", [], [], 0, 0)
        st["A empty"] += 1
        check_term_common(I, Sk, D, st)
        if D & Sk.Up:
            st["A EMPTY FINAL FAIL"] += 1
        return D, [("F", (), (), 0, 0)], 1, "final"
    if I.upc(Sk.A) != Sk.Up:
        st["Up != up(A) FAIL"] += 1
    Ap = Sk.A
    Dall = I.full
    terms = []
    nlev = 0
    status = None
    anchors_total = 0
    while True:
        nlev += 1
        kind, term, D, App = one_level(I, Sk, Ap, k, N, mode, st, ccap, pick)
        if kind == "error":
            return None, terms, nlev, "error"
        terms.append(term)
        if term[3]:
            anchors_total += popcount(term[3])
            if kind != "final" or term[0] != "F":
                st["ANCHORS IN A NON-FINAL OR E TERM FAIL"] += 1
        if len(term[1]) > k:
            st["MORE THAN k TOOLS FAIL"] += 1
        Dall &= D
        if kind == "final":
            status = "final"
            break
        if kind == "stuck":
            status = "stuck"
            break
        Ap = App
    st["levels=%d (%s)" % (nlev, mode)] += 1
    if mode == "proof" and nlev > k:
        st["MORE THAN k LEVELS FAIL"] += 1
    if anchors_total > N:
        st["MORE THAN N ANCHORS FAIL"] += 1
    if status == "final":
        if Sk.L & ~Dall:
            st["FINAL D MISSES L FAIL"] += 1
        if Dall & Sk.Up:
            st["FINAL D MEETS Up FAIL"] += 1
        if not I.is_down(Dall):
            st["FINAL D NOT DOWN-SET FAIL"] += 1
        if not I.connects(Dall):
            st["FINAL D DOES NOT CONNECT FAIL"] += 1
    return Dall, terms, nlev, status


def lemma63_check(I, Sk, st):
    """|A & NE(E#_x)| for x not in L, dual for y not in Up; records the maximum and counts > 9."""
    for x in range(I.m):
        if not (Sk.L >> x) & 1:
            c = popcount(Sk.A & I.NEs[x])
            st["max |A & NE(E#x)|"] = max(st["max |A & NE(E#x)|"], c)
            if c > 9:
                st["LEMMA 6.3 FAIL"] += 1
        if not (Sk.Up >> x) & 1:
            c = popcount(Sk.B & I.NFs[x])
            st["max |B & NF(F#y)|"] = max(st["max |B & NF(F#y)|"], c)
            if c > 9:
                st["LEMMA 6.3 DUAL FAIL"] += 1
