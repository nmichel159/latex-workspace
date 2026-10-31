"""Claim checks of the review rv-classes-q on one shortest valid path P (r5-classes.md §2, §2a, §2b, §2c).

Every claim is an assertion (ClaimFailure with the name of the claim).  Positions are 0-based in the code; the
text's positions are 1-based (only differences matter).
"""
from fractions import Fraction

from qcore import bits, popcount, solve_game, min_cover, kq


class ClaimFailure(Exception):
    pass


def need(cond, name, **info):
    if not cond:
        raise ClaimFailure(name + " " + repr(info))


def bump(st, key, by=1):
    st[key] = st.get(key, 0) + by


def bmax(st, key, val):
    if val is not None and val > st.get(key, -1):
        st[key] = val


def contacts(I, Y, P):
    """positions c (0-based) with Y meeting X_c"""
    my = I.mask[Y]
    return [a for a, x in enumerate(P) if my & I.mask[x]]


def p_consistent(I, Y, pt):
    """Y is P-consistent: its class is not used on P with the type opposite to the type of Y"""
    C = I.cl[Y >> 1]
    return pt.get(C, Y & 1) == (Y & 1)


# ---------------------------------------------------------------- §2: A1-A5, Lemma W
def check_basic(I, P, st):
    r = len(P)
    need(I.is_valid_path(P), "P valid")
    pt = I.path_types(P)
    onP = set(P)
    sw_on = {x >> 1: a for a, x in enumerate(P)}
    # A1
    for a in range(r):
        for b in range(a + 2, r):
            need(not (I.mask[P[a]] & I.mask[P[b]]), "A1", a=a, b=b)
    # A2
    for a in range(r):
        for b in range(a + 2, r):
            xa, xb = P[a], P[b]
            if I.cl[xa >> 1] == I.cl[xb >> 1]:
                continue
            pa, pb = I.mask[xa ^ 1], I.mask[xb ^ 1]
            if (xa & 1) == (xb & 1):
                need(pa & pb, "A2 same type: partners meet", a=a, b=b)
            else:
                need((pa & I.mask[xb]) or (I.mask[xa] & pb), "A2 opposite types", a=a, b=b)
            bump(st, "A2")
    # Lemma W (all P-consistent sides not on P) and the member version via A1
    for Y in I.sides:
        cs = contacts(I, Y, P)
        if Y in onP:
            a = P.index(Y)
            need(all(abs(c - a) <= 1 for c in cs), "W member", a=a, cs=cs)
            continue
        if p_consistent(I, Y, pt):
            if cs:
                need(max(cs) - min(cs) <= 2, "Lemma W", Y=Y, cs=cs)
                bump(st, "W_sides")
                bmax(st, "W_maxwidth", max(cs) - min(cs))
        else:
            if cs:
                bmax(st, "nonconsistent_maxwidth", max(cs) - min(cs))
    # A3 (span lemma): O-sides of switches of a class C of P
    for C, TC in pt.items():
        posC = [a for a, x in enumerate(P) if I.cl[x >> 1] == C]
        a1, ak = posC[0], posC[-1]
        for w in I.classes[C]:
            Z = 2 * w + (1 - TC)
            if not I.mask[Z]:
                continue
            cs = contacts(I, Z, P)
            left = [d for d in cs if d < a1]
            right = [c for c in cs if c > ak]
            if left and right:
                d, c = min(left), max(right)
                need(c - d <= 2, "A3 span", C=C, d=d, c=c)
                need(len(posC) == 1 and d == a1 - 1 and c == a1 + 1, "A3 k>=2 impossible / k=1 Lemma 1",
                     C=C, posC=posC, d=d, c=c)
                bump(st, "A3_both_sides_k1")
            bump(st, "A3_sides")
            if len(posC) >= 2:
                bump(st, "A3_multi")
    # A4: T-side Z of a switch of a class used with T, Z not on P: window (Lemma W) and the P2 consequence
    for Y in I.sides:
        if Y in onP:
            continue
        C = I.cl[Y >> 1]
        if pt.get(C) != (Y & 1):
            continue
        cs = contacts(I, Y, P)
        if cs:
            need(max(cs) - min(cs) <= 2, "A4 window", Y=Y, cs=cs)
        need((Y >> 1) not in sw_on, "A4 switch of Z not on P", Y=Y)
        Zp = I.mask[Y ^ 1]
        for b, xb in enumerate(P):
            if (xb & 1) == (Y & 1) and I.cl[xb >> 1] != C and not (I.mask[Y] & I.mask[xb]):
                need(Zp & I.mask[xb ^ 1], "A4 P2 consequence", Y=Y, b=b)
                bump(st, "A4_dom")
    bump(st, "paths")
    bmax(st, "r_max", r)


# ---------------------------------------------------------------- §2a: Lemma 2a.1
def check_2a1(I, P, rng, st, trials=4):
    pt = I.path_types(P)
    for _ in range(trials):
        T = rng.randrange(2)
        O = 1 - T
        U = 0
        for x in I.sides:
            if (x & 1) == O and rng.random() < 0.5:
                U |= 1 << x
        calT = [C for C, ty in pt.items() if ty == T]
        calO = [C for C, ty in pt.items() if ty == O]
        Phi = [C for C in calT if I.Omega[C][O] & ~U] + [D for D in calO if not (I.Omega[D][O] & ~U)]
        modes = I.sigma(U, O)
        need(sorted(Phi) == I.misclassified(P, modes), "2a.1 Phi = classes of P on which sigma_U is wrong")
        m2 = modes
        for C in Phi:
            m2 ^= 1 << C
        need(I.picks_path(P, m2), "2a.1 sigma_U^Phi picks P")
        need(I.connects(m2), "2a.1 connects")
        bump(st, "2a1")


# ---------------------------------------------------------------- §2b: Lemma D, Theorem Q
def check_theorem_q(I, P, T, st, rec=None):
    """Runs the proof of Theorem Q for the path P and the type T with an assertion for each step.
    Returns a dict with lam, the case, the number of centres, |Phi|, tau, U, Phi."""
    O = 1 - T
    sw = I.sw
    pt = I.path_types(P)
    calT = {C for C, ty in pt.items() if ty == T}
    calO = {C for C, ty in pt.items() if ty == O}
    need(not (calT & calO), "classes of P have one type")
    Wall = [w for w in range(I.n) if I.cl[w] in calT]
    Wstar = [w for w in Wall if sw[w][O]]
    V = [v for v in range(I.n) if I.cl[v] in calO]
    Vstar = [v for v in V if sw[v][T]]
    k = kq(I.n)
    # Lemma D for every pair (all switches of the two families, mates included)
    for w in Wall:
        for v in V:
            need((sw[w][O] & sw[v][O]) or (sw[w][T] & sw[v][T]), "Lemma D", w=w, v=v)
    bump(st, "D_pairs", len(Wall) * len(V))
    # Omega(C, O) = {w^O : w in C and W*} for C in calT, Omega(D, T) = {v^T : v in D and V*}
    for C in calT:
        need(I.Omega[C][O] == sum(1 << (2 * w + O) for w in Wstar if I.cl[w] == C), "Omega(C,O)")
    for D in calO:
        need(I.Omega[D][T] == sum(1 << (2 * v + T) for v in Vstar if I.cl[v] == D), "Omega(D,T)")
    out = {"T": T, "nW": len(Wstar), "nV": len(V), "nVstar": len(Vstar), "k": k}
    if not Wstar or not Vstar:
        tau = O if not Wstar else T
        modes = I.sigma(0, tau)
        need(I.picks_path(P, modes), "Q empty case: sigma_0 picks P", tau=tau)
        need(I.connects(modes), "Q empty case connects")
        bump(st, "Q_empty_W" if not Wstar else "Q_empty_V")
        out.update(case="empty", tau=tau, h=0, phi=0, U=0, Phi=[])
        return out
    A = [[1 if (sw[v][O] & sw[w][O]) else 0 for w in Wstar] for v in V]
    lam, p, q = solve_game(A)
    half = Fraction(1, 2)
    out["lam"] = lam
    if lam >= half:
        for j in range(len(Wstar)):
            need(sum(p[i] * A[i][j] for i in range(len(V))) >= half, "case 1: column payoff >= 1/2")
        supp = [i for i in range(len(V)) if p[i] > 0]
        univ = (1 << len(Wstar)) - 1
        sets = [sum(A[i][j] << j for j in range(len(Wstar))) for i in supp]
        h, idx = min_cover(univ, sets)
        need(h is not None and h <= kq(len(Wstar)) <= k, "case 1: sampling bound", h=h, nW=len(Wstar))
        centres = [2 * V[supp[i]] + O for i in idx]
        tau = O
        covered = calT
        flipside = calO
        bump(st, "Q_case1")
    else:
        for i in range(len(V)):
            need(sum(A[i][j] * q[j] for j in range(len(Wstar))) < half, "case 2: row payoff < 1/2")
        for v in V:
            pr = sum(q[j] for j, w in enumerate(Wstar) if sw[w][T] & sw[v][T])
            need(pr > half, "case 2: Lemma D gives Pr[w^T meets v^T] > 1/2", v=v, pr=pr)
        supp = [j for j in range(len(Wstar)) if q[j] > 0]
        univ = (1 << len(Vstar)) - 1
        sets = [sum(1 << i for i, v in enumerate(Vstar) if sw[Wstar[j]][T] & sw[v][T]) for j in supp]
        h, idx = min_cover(univ, sets)
        need(h is not None and h <= kq(len(Vstar)) <= k, "case 2: sampling bound", h=h, nV=len(Vstar))
        centres = [2 * Wstar[supp[j]] + T for j in idx]
        tau = T
        covered = calO
        flipside = calT
        bump(st, "Q_case2")
    U = 0
    for Y in centres:
        need(I.mask[Y] != 0, "centre non-empty")
        U |= I.Nset(tau, Y)
    for C in covered:
        need(not (I.Omega[C][tau] & ~U), "needed sides covered", C=C, tau=tau)
    memb_in_U = [a for a, x in enumerate(P) if (U >> x) & 1]
    for Y in centres:
        need(p_consistent(I, Y, pt), "centre P-consistent", Y=Y)
        pos = [a for a, x in enumerate(P) if (I.Nset(tau, Y) >> x) & 1]
        need(len(pos) <= 3 and (not pos or max(pos) - min(pos) <= 2), "N_tau[Y] has <= 3 members (Lemma W)",
             Y=Y, pos=pos)
    need(len(memb_in_U) <= 3 * len(centres), "members in U <= 3 per centre")
    modes = I.sigma(U, tau)
    Phi = I.misclassified(P, modes)
    need(set(Phi) <= flipside, "only classes of the other family misclassified", Phi=Phi)
    for C in Phi:
        need(any(I.cl[P[a] >> 1] == C for a in memb_in_U), "misclassified class has a member in U", C=C)
    need(len(Phi) <= 3 * len(centres) <= 3 * k, "|Phi| <= 3 * centres", phi=len(Phi), h=len(centres))
    m2 = modes
    for C in Phi:
        m2 ^= 1 << C
    need(I.picks_path(P, m2), "sigma_U^Phi picks P")
    need(I.connects(m2), "sigma_U^Phi connects s, t")
    bmax(st, "Q_h_max", len(centres))
    bmax(st, "Q_phi_max", len(Phi))
    bmax(st, "Q_members_in_U_max", len(memb_in_U))
    out.update(case=1 if tau == O else 2, tau=tau, h=len(centres), phi=len(Phi), U=U, Phi=Phi)
    return out


def full_covers(I, P, T):
    """least numbers of centres with centres from ALL switches of the family (not only the support):
    hO = O-sides of switches of O-classes covering every needed O-side of T-classes,
    hT = T-sides of switches of T-classes covering every needed T-side of O-classes."""
    O = 1 - T
    sw = I.sw
    pt = I.path_types(P)
    Wall = [w for w in range(I.n) if pt.get(I.cl[w]) == T]
    V = [v for v in range(I.n) if pt.get(I.cl[v]) == O]
    Wstar = [w for w in Wall if sw[w][O]]
    Vstar = [v for v in V if sw[v][T]]
    setsO = [sum(1 << j for j, w in enumerate(Wstar) if sw[v][O] & sw[w][O]) for v in V]
    hO, _ = min_cover((1 << len(Wstar)) - 1, setsO)
    setsT = [sum(1 << i for i, v in enumerate(Vstar) if sw[w][T] & sw[v][T]) for w in Wall]
    hT, _ = min_cover((1 << len(Vstar)) - 1, setsT)
    return hO, hT


# ---------------------------------------------------------------- §2c: Lemma PP
def check_pp(I, P, T, st, maxpairs=None):
    O = 1 - T
    r = len(P)
    pt = I.path_types(P)
    calT = [C for C, ty in pt.items() if ty == T]
    calO = [C for C, ty in pt.items() if ty == O]
    Tm = [a for a, x in enumerate(P) if (x & 1) == T]
    pairs = [(u, b) for u in Tm for b in Tm if u < b and b - u >= 3 and I.cl[P[u] >> 1] != I.cl[P[b] >> 1]]
    errs = []
    for (u, b) in pairs[:maxpairs] if maxpairs else pairs:
        Xu, Xb = P[u] ^ 1, P[b] ^ 1
        U = I.Nset(O, Xu) | I.Nset(O, Xb) | I.Omega[I.cl[P[u] >> 1]][O] | I.Omega[I.cl[P[b] >> 1]][O]
        for a in (u - 1, u + 1, b - 1, b + 1):
            if 0 <= a < r and (P[a] & 1) == T and I.mask[P[a] ^ 1]:
                U |= 1 << (P[a] ^ 1)
        for C in calT:
            need(not (I.Omega[C][O] & ~U), "PP: Omega(C,O) in U", C=C, u=u, b=b)
        modes = I.sigma(U, O)
        mis = I.misclassified(P, modes)
        mu, mb = I.mask[Xu], I.mask[Xb]
        Err = sorted(D for D in calO if all((I.mask[Y] & mu) or (I.mask[Y] & mb) for Y in bits(I.Omega[D][O])))
        need(mis == Err, "PP: misclassified = Err(u,b)", mis=mis, Err=Err)
        m2 = modes
        for C in mis:
            m2 ^= 1 << C
        need(I.picks_path(P, m2) and I.connects(m2), "PP: sigma_U^Err picks P")
        errs.append(len(Err))
        bump(st, "PP_pairs")
    if not pairs:
        need(len(calT) <= 3, "PP fallback: at most 3 T-classes", calT=calT)
        U = 0
        for C in calT:
            U |= I.Omega[C][O]
        modes = I.sigma(U, O)
        need(I.misclassified(P, modes) == [], "PP fallback: misclassification 0")
        bump(st, "PP_fallback")
    if errs:
        bmax(st, "PP_minErr_max", min(errs))
    return min(errs) if errs else None


# ---------------------------------------------------------------- A5: class search
def class_search(I, K, B, count_classes=True):
    """Search of r4-switch Theorem 5 with Pi(Y) = all opposite-type sides of the class of Y and stored
    (class, type) pairs.  Conditions at step j: (i) Pi(Y_j) is contained in K; (ii) (class of Y_j, opposite type)
    is not stored; storage = number of stored pairs (or of distinct members in K) <= B.  BFS over states.
    Returns a walk (list of sides) or None."""
    from collections import deque
    start = [x for x in I.sides if (I.hasS >> x) & 1]

    def ok(y, stored):
        # stored: frozenset of (class, type, side) for the walk's sides in K so far
        C = I.cl[y >> 1]
        ty = y & 1
        if I.Omega[C][1 - ty] & ~K:
            return None
        if any(c == C and t_ == 1 - ty for (c, t_, _) in stored):
            return None
        if (K >> y) & 1:
            ns = stored | {(C, ty, y)}
            size = len({(c, t_) for (c, t_, _) in ns}) if count_classes else len(ns)
            if size > B:
                return None
            return ns
        return stored

    seen = {}
    dq = deque()
    for x in start:
        ns = ok(x, frozenset())
        if ns is None:
            continue
        stt = (x, frozenset(ns))
        if stt not in seen:
            seen[stt] = None
            dq.append(stt)
    while dq:
        stt = dq.popleft()
        x, stored = stt
        if (I.hasT >> x) & 1:
            walk = []
            cur = stt
            while cur is not None:
                walk.append(cur[0])
                cur = seen[cur]
            return walk[::-1]
        for y in bits(I.meet[x]):
            ns = ok(y, stored)
            if ns is None:
                continue
            s2 = (y, frozenset(ns))
            if s2 not in seen:
                seen[s2] = stt
                dq.append(s2)
    return None


def walk_ok(I, W):
    """a valid walk with classes: s in first, t in last, consecutive equal or meeting, no two sides of one class
    with different types; then the mode vector it defines connects s, t"""
    if not W:
        return False
    if not ((I.mask[W[0]] >> I.s) & 1) or not ((I.mask[W[-1]] >> I.t) & 1):
        return False
    for a in range(len(W) - 1):
        if W[a] != W[a + 1] and not (I.mask[W[a]] & I.mask[W[a + 1]]):
            return False
    ty = {}
    for x in W:
        C = I.cl[x >> 1]
        if ty.setdefault(C, x & 1) != (x & 1):
            return False
    modes = 0
    for C, t_ in ty.items():
        modes |= t_ << C
    return I.connects(modes)
