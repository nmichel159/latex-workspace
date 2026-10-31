"""Every step of r4-switch.md sections 2-4 as an assertion on a given shortest valid path (own implementation).

Positions are 1-based as in the text.  check_path(inst, P) asserts F1-F3, the replacement bound F4 for detours of
1 and 2 sides, Lemma 1 (kinds), Lemma 2, Lemma 3, Theorem 4 (both types), S2, S3, enumerates every straddle of both
types and checks Lemma 7 on each (tightness, the swapped path, its certificate, acceptance by the search), runs the
case distinction of Theorem 8 for every type T without T-straddle with an assertion for each claim, and finally
builds the certificate of Corollary 9 and runs the search of Theorem 5 with it.  Any failed claim raises
ClaimFailure with the name of the claim.
"""
from core import search5, is_valid_path, is_valid_walk

NEG, POS = -10 ** 9, 10 ** 9


class ClaimFailure(Exception):
    pass


def need(cond, name, **info):
    if not cond:
        raise ClaimFailure((name, info))


class Ctx:
    def __init__(self, inst, P):
        self.inst = inst
        self.P = list(P)
        r = self.r = len(P)
        self.X = [None] + [inst.sets[x] for x in P]
        self.typ = [None] + [inst.typ[x] for x in P]
        self.pidx = [None] + [inst.partner[x] for x in P]
        empty = frozenset()
        self.Xp = [None] + [inst.sets[p] if p is not None else empty for p in self.pidx[1:]]
        self.pos = range(1, r + 1)
        self.contacts = [None] + [{c for c in self.pos if c != a and self.Xp[a] & self.X[c]} for a in self.pos]
        kinds = [None]
        for a in self.pos:
            C = self.contacts[a]
            if any(c >= a + 2 for c in C):
                kinds.append('F')
            elif any(c <= a - 2 for c in C):
                kinds.append('B')
            else:
                kinds.append('L')
        self.kind = kinds

    def members(self, T):
        return [a for a in self.pos if self.typ[a] == T]

    def f(self, a):
        O = 1 - self.typ[a]
        return sorted(c for c in self.contacts[a] if self.typ[c] == O)


# ---------------------------------------------------------------- section 2

def check_basic(ctx):
    inst, r, X, Xp, typ = ctx.inst, ctx.r, ctx.X, ctx.Xp, ctx.typ
    need(is_valid_path(inst, ctx.P), "P valid")
    for a in ctx.pos:
        for b in ctx.pos:
            if b <= a:
                continue
            if b - a >= 2:
                need(not (X[a] & X[b]), "F1", a=a, b=b)
                if typ[a] == typ[b]:
                    need(bool(Xp[a]) and bool(Xp[b]) and bool(Xp[a] & Xp[b]), "F2", a=a, b=b)
                else:
                    need(bool(Xp[a] & X[b]) or bool(X[a] & Xp[b]), "F3", a=a, b=b)
    # F4 for detours of one and two sides (all sides of the instance)
    D = inst.D
    swpos = {inst.swof[ctx.P[a - 1]]: a for a in ctx.pos}
    for d in ctx.pos:
        for c in ctx.pos:
            if c <= d + 2:
                continue
            for y in range(D):
                w = inst.swof[y]
                if w in swpos and (swpos[w] <= d or swpos[w] >= c):
                    continue
                if not (inst.sets[y] & X[d]):
                    continue
                need(not (inst.sets[y] & X[c]), "F4 k=1", d=d, c=c, y=y)
                if c <= d + 3:
                    continue
                for y2 in inst.nbrs[y]:
                    w2 = inst.swof[y2]
                    if w2 == w:
                        continue
                    if w2 in swpos and (swpos[w2] <= d or swpos[w2] >= c):
                        continue
                    need(not (inst.sets[y2] & X[c]), "F4 k=2", d=d, c=c, y=y, y2=y2)


def check_lemmas(ctx):
    r, X, Xp, typ, kind, contacts = ctx.r, ctx.X, ctx.Xp, ctx.typ, ctx.kind, ctx.contacts
    for a in ctx.pos:
        C = contacts[a]
        for d in C:
            for c in C:
                if d < a < c:
                    need(d == a - 1 and c == a + 1, "Lemma 1", a=a, d=d, c=c)
        if kind[a] == 'F':
            need(all(c >= a + 1 for c in C), "kind forward", a=a)
        if kind[a] == 'B':
            need(all(c <= a - 1 for c in C), "kind backward", a=a)
        if kind[a] == 'L':
            need(all(c in (a - 1, a + 1) for c in C), "kind local", a=a)
    for a in ctx.pos:
        for b in ctx.pos:
            if a == b or not (Xp[a] & Xp[b]):
                continue
            if kind[a] == 'F' and b < a:
                need(not any(d < b for d in contacts[b]), "Lemma 2(a)", a=a, b=b)
            if kind[a] == 'B' and b > a:
                need(not any(d > b for d in contacts[b]), "Lemma 2(b)", a=a, b=b)
    for a in ctx.pos:
        for q in ctx.pos:
            if typ[a] != typ[q] and abs(a - q) >= 2 and a not in contacts[q]:
                need(bool(Xp[a] & X[q]), "Lemma 3", a=a, q=q)


def theorem4(ctx, T):
    """Return (qf, qb, R) when the hypotheses of Theorem 4 hold for T, else None; asserts (a)-(c)."""
    O = 1 - T
    Om = ctx.members(O)
    if not Om or any(ctx.kind[q] == 'L' for q in Om):
        return None
    fw = [q for q in Om if ctx.kind[q] == 'F']
    bw = [q for q in Om if ctx.kind[q] == 'B']
    qf = max(fw) if fw else NEG
    qb = min(bw) if bw else POS
    if fw and bw:
        need(qb >= qf - 1, "Theorem 4(a)", qf=qf, qb=qb)
    for a in ctx.members(T):
        if fw and a <= qf - 2:
            need(bool(ctx.Xp[a] & ctx.X[qf]), "Theorem 4(b) qf", a=a, qf=qf)
        if bw and a >= qb + 2:
            need(bool(ctx.Xp[a] & ctx.X[qb]), "Theorem 4(b) qb", a=a, qb=qb)
    R = [c for c in ctx.pos if qf < c < qb]
    for c in R:
        need(ctx.typ[c] == T, "Theorem 4(c)", c=c)
    return qf, qb, R


def check_S(ctx):
    inst = ctx.inst
    Pset = set(ctx.P)
    for c in ctx.pos:
        for O in (0, 1):
            Nc = inst.N_of(O, ctx.P[c - 1])
            mem = [a for a in ctx.pos if ctx.P[a - 1] in Nc]
            need(len(mem) <= 3 and all(abs(a - c) <= 1 for a in mem), "S2", c=c)
    for a in ctx.pos:
        p = ctx.pidx[a]
        if p is None:
            continue
        need(p not in Pset, "S1", a=a)
        O = 1 - ctx.typ[a]
        Np = inst.N_of(O, p)
        mem = sorted(c for c in ctx.pos if ctx.P[c - 1] in Np)
        need(mem == ctx.f(a), "S3", a=a)


# ---------------------------------------------------------------- straddles and Lemma 7

def straddles(ctx, T):
    """All T-straddles (x, p, x1, x2, p1, p2)."""
    O = 1 - T
    res = []
    Tm, Om = ctx.members(T), ctx.members(O)
    for x in Tm:
        for p in Om:
            L1 = [y for y in Tm if y < x and ctx.Xp[p] & ctx.X[y]]
            L2 = [y for y in Tm if y > x and ctx.Xp[p] & ctx.X[y]]
            M1 = [c for c in Om if c < p and ctx.Xp[x] & ctx.X[c]]
            M2 = [c for c in Om if c > p and ctx.Xp[x] & ctx.X[c]]
            for x1 in L1:
                for x2 in L2:
                    for p1 in M1:
                        for p2 in M2:
                            if x2 < p1 or p2 < x1:
                                res.append((x, p, x1, x2, p1, p2))
    return res


def cert_check(inst, Pp, KT, KO, T, name):
    """Coverage of the pair (T-certificate KT, O-certificate KO) for the path Pp; returns the total storage."""
    O = 1 - T
    for a, x in enumerate(Pp, 1):
        pt = inst.partner[x]
        if pt is None:
            continue
        if inst.typ[x] == T:
            need(pt in KT, name + " coverage T", a=a)
        else:
            need(pt in KO, name + " coverage O", a=a)
    for y in KT:
        need(inst.typ[y] == O, name + " KT has O-sides only")
    for y in KO:
        need(inst.typ[y] == T, name + " KO has T-sides only")
    return len(set(Pp) & set(KT)), len(set(Pp) & set(KO)), len(set(Pp) & (set(KT) | set(KO)))


def lemma7(ctx, T, st):
    inst = ctx.inst
    O = 1 - T
    x, p, x1, x2, p1, p2 = st
    need(x1 == x - 1 and x2 == x + 1 and p1 == p - 1 and p2 == p + 1, "Lemma 7 tightness", st=st)
    P = ctx.P
    if x2 < p1:
        Q = P[:x1] + [ctx.pidx[p]] + P[x2 - 1:p1] + [ctx.pidx[x]] + P[p2 - 1:]
    else:
        Q = P[:p1] + [ctx.pidx[x]] + P[p2 - 1:x1] + [ctx.pidx[p]] + P[x2 - 1:]
    Pstar = list(P)
    Pstar[x - 1] = ctx.pidx[p]
    Pstar[p - 1] = ctx.pidx[x]
    need(Q == Pstar, "Lemma 7 Q = P*", st=st)
    need(is_valid_path(inst, Pstar) and len(Pstar) == ctx.r, "Lemma 7 P* valid shortest", st=st)
    for a in range(1, ctx.r + 1):
        need(inst.typ[Pstar[a - 1]] == ctx.typ[a], "Lemma 7 types kept", a=a)
    # certificates of P*
    KT = set(inst.N_of(O, P[p - 1]))
    KO = set(inst.N_of(T, P[x - 1]))
    singlesT = [inst.partner[Pstar[c - 1]] for c in (x - 1, x + 1)
                if 1 <= c <= ctx.r and inst.typ[Pstar[c - 1]] == T and inst.partner[Pstar[c - 1]] is not None]
    singlesO = [inst.partner[Pstar[c - 1]] for c in (p - 1, p + 1)
                if 1 <= c <= ctx.r and inst.typ[Pstar[c - 1]] == O and inst.partner[Pstar[c - 1]] is not None]
    KT |= set(singlesT)
    KO |= set(singlesO)
    sT, sO, stot = cert_check(inst, Pstar, KT, KO, T, "Lemma 7")
    need(sT <= 3 and sO <= 3, "Lemma 7 storage", sT=sT, sO=sO)
    K = KT | KO
    W = search5(inst, K, stot)
    need(W is not None and is_valid_walk(inst, W), "Lemma 7 search accepts", st=st)
    return {"Pstar": Pstar, "K": sorted(K), "B": stot, "sT": sT, "sO": sO}


# ---------------------------------------------------------------- Theorem 8

def max_disjoint(spans):
    """Maximum number of pairwise disjoint integer intervals (greedy by right end)."""
    cnt, last = 0, NEG
    for lo, hi in sorted(spans, key=lambda s: s[1]):
        if lo > last:
            cnt += 1
            last = hi
    return cnt


def theorem8(ctx, T, stats):
    """T-certificate of Theorem 8 for a path without T-straddle: returns (Zs, singles, step).

    Zs: list of side indices Z (the sets N_O[Z]); singles: list of side indices.
    """
    inst = ctx.inst
    O = 1 - T
    Tm, Om = ctx.members(T), ctx.members(O)
    Xp, X, kind, P = ctx.Xp, ctx.X, ctx.kind, ctx.P

    def partners_at(cs):
        out = []
        for c in cs:
            if 1 <= c <= ctx.r and ctx.typ[c] == T and ctx.pidx[c] is not None:
                out.append(ctx.pidx[c])
        return out

    # (0)
    emp = [a for a in Tm if ctx.pidx[a] is None]
    if emp:
        a = emp[0]
        need(all(abs(b - a) <= 1 for b in Tm), "Thm 8 (0)", a=a)
        return [], partners_at((a - 1, a + 1)), 0
    # (1)
    for a in Tm:
        if len(ctx.f(a)) <= 3:
            return [ctx.pidx[a]], partners_at((a - 1, a + 1)), 1
    for a in Tm:
        need(kind[a] != 'L', "Thm 8 after (1): no local T-member", a=a)
    # (2)
    for q in Om:
        if kind[q] == 'L':
            return [P[q - 1]], partners_at((q - 1, q + 1)), 2
    need(len(Om) > 0, "Thm 8 (2): O-member exists")
    t4 = theorem4(ctx, T)
    need(t4 is not None, "Thm 8 (3): Theorem 4 applies")
    qf, qb, R = t4
    Zs, singles = [], []
    if qf != NEG:
        Zs.append(P[qf - 1])
    if qb != POS:
        Zs.append(P[qb - 1])
    singles += partners_at((qf - 1, qb + 1))
    for a in R:
        need(kind[a] in 'FB', "Thm 8 (3): R non-local", a=a)
    Rf = [a for a in R if kind[a] == 'F']
    Rb = [a for a in R if kind[a] == 'B']
    stats['step3'] = stats.get('step3', 0) + 1
    covered_R = set()
    rows_dirs = []
    for direction in ('fwd', 'bwd'):
        if direction == 'fwd':
            Cset = [c for c in Om if c >= qb]
            excl = qb - 1
            A = [a for a in Rf if a != excl]
            if excl in Rf:
                singles.append(ctx.pidx[excl])
                covered_R.add(excl)
        else:
            Cset = [c for c in Om if c <= qf]
            excl = qf + 1
            A = [a for a in Rb if a != excl]
            if excl in Rb:
                singles.append(ctx.pidx[excl])
                covered_R.add(excl)
        Cs = set(Cset)
        if not A:
            continue
        stats['rows'] = stats.get('rows', 0) + 1
        stats['rows_' + direction] = stats.get('rows_' + direction, 0) + 1
        rows_dirs.append(direction)
        fa = {a: ctx.f(a) for a in A}
        for a in A:
            need(set(fa[a]) <= Cs, "(F0)/(B0) f(a) in C", a=a, d=direction)
            for p in Cset:
                if direction == 'fwd':
                    need(p >= a + 2, "(F0) p >= a+2", a=a, p=p)
                else:
                    need(p <= a - 2, "(B0) p <= a-2", a=a, p=p)
        if direction == 'fwd':
            need(qb != POS, "(F0) qb finite")
        else:
            need(qf != NEG, "(B0) qf finite")
        bset = {p: {y for y in R if Xp[p] & X[y]} for p in Cset}
        for a in A:
            for p in Cset:
                need(p in fa[a] or a in bset[p], "(F1)/(B1)", a=a, p=p, d=direction)
        # holes
        holes_of = {p: [a for a in A if fa[a][0] < p < fa[a][-1] and p not in fa[a]] for p in Cset}
        for p in Cset:
            hs = holes_of[p]
            need(len(hs) <= 2, "(F3)/(B3) hole bound", p=p, holes=hs, d=direction)
            if hs:
                b = sorted(bset[p])
                for a in hs:
                    need(a in (b[0], b[-1]), "(F3)/(B3) extreme of b(p)", p=p, a=a)
                stats['holes'] = stats.get('holes', 0) + len(hs)
        spans = [(fa[a][0], fa[a][-1]) for a in A]
        md = max_disjoint(spans)
        need(md <= 4, "(F4)/(B4) at most 4 disjoint spans", md=md)
        stats['max_disjoint'] = max(stats.get('max_disjoint', 0), md)
        # (F5)/(B5) greedy piercing
        H = []
        for a in sorted(A, key=lambda a: fa[a][-1]):
            lo, hi = fa[a][0], fa[a][-1]
            if not any(lo <= h <= hi for h in H):
                H.append(hi)
        need(len(H) <= 4 and set(H) <= Cs, "(F5)/(B5) |H| <= 4", H=H)
        stats['maxH'] = max(stats.get('maxH', 0), len(H))
        for h in H:
            Zs.append(P[h - 1])
        for a in A:
            lo, hi = fa[a][0], fa[a][-1]
            inspan = [h for h in H if lo <= h <= hi]
            need(len(inspan) > 0, "(F5) span met", a=a)
            good = [h for h in inspan if h in fa[a]]
            if not good:
                h = inspan[0]
                need(a in holes_of[h], "(F5) chosen h is a hole", a=a, h=h)
                singles.append(ctx.pidx[a])
                stats['hole_singles'] = stats.get('hole_singles', 0) + 1
            covered_R.add(a)
    if len(rows_dirs) == 2:
        stats['rows_both'] = stats.get('rows_both', 0) + 1
    for a in R:
        need(a in covered_R, "Thm 8 (3): R covered", a=a)
    return Zs, singles, 3


def build_K(inst, T, Zs, singles):
    O = 1 - T
    K = set()
    for z in Zs:
        K |= inst.N_of(O, z)
    K |= set(singles)
    return K


# ---------------------------------------------------------------- driver

def check_path(inst, P, stats, run_search=True):
    """All claims on one shortest valid path; returns a summary dict.  Raises ClaimFailure on a failed claim."""
    ctx = Ctx(inst, P)
    check_basic(ctx)
    check_lemmas(ctx)
    check_S(ctx)
    for T in (0, 1):
        theorem4(ctx, T)
    sts = {T: straddles(ctx, T) for T in (0, 1)}
    out = {"r": ctx.r, "straddles": len(sts[0]) + len(sts[1])}
    swaps = []
    for T in (0, 1):
        for st in sts[T]:
            swaps.append(lemma7(ctx, T, st))
            stats['swaps'] = stats.get('swaps', 0) + 1
    certs = {}
    for T in (0, 1):
        if sts[T]:
            continue
        Zs, singles, step = theorem8(ctx, T, stats)
        for y in singles:
            need(y is not None, "Thm 8 single side non-empty")
        need(len(Zs) <= 10 and len(singles) <= 20, "Thm 8 counts", nZ=len(Zs), ns=len(singles))
        KT = build_K(inst, T, Zs, singles)
        # coverage of all T-members with non-empty partner, storage
        for a in ctx.members(T):
            if ctx.pidx[a] is not None:
                need(ctx.pidx[a] in KT, "Thm 8 coverage", T=T, a=a, step=step)
        stor = len(set(P) & KT)
        need(stor <= 30, "Thm 8 storage <= 30", stor=stor)
        if step == 3:
            need(stor <= 3 * len(Zs), "Thm 8 storage <= 3 per set")
        stats['step%d' % step + '_T'] = stats.get('step%d' % step + '_T', 0) + 1
        stats['maxZ'] = max(stats.get('maxZ', 0), len(Zs))
        stats['maxsingles'] = max(stats.get('maxsingles', 0), len(singles))
        stats['maxstorT'] = max(stats.get('maxstorT', 0), stor)
        certs[T] = (Zs, singles, step, KT, stor)
    # Corollary 9
    if sts[0] or sts[1]:
        sw = swaps[0]
        out["cor9"] = ("swap", sw["B"])
    else:
        K = certs[0][3] | certs[1][3]
        B = len(set(P) & K)
        need(B <= 60, "Cor 9 storage <= 60", B=B)
        out["cor9"] = ("thm8", B, len(certs[0][0]), len(certs[0][1]), len(certs[1][0]), len(certs[1][1]))
        if run_search:
            W = search5(inst, K, B)
            need(W is not None and is_valid_walk(inst, W), "Cor 9 search accepts", B=B)
        stats['maxB'] = max(stats.get('maxB', 0), B)
    out["certs"] = {T: (c[0], c[1], c[2], c[4]) for T, c in certs.items()}
    return out
