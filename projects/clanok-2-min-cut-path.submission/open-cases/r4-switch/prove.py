"""Constructive check of the certificate theorem (r4-switch.md §5).

Given an instance and a shortest valid path P, build a typed certificate following the proof step by step, or a
straddle swap P* with its certificate, and verify it:
  K ⊇ partners of the path, storage |path ∩ K| within the proved bound, every claimed lemma on the way
  (Lemma 1, Lemma 2 consequence q_b >= q_f - 1, column hole bound, disjoint span bound, f(a) ⊆ C, ...).
Raises AssertionError on any violation (a counterexample to a step of the proof).

Certificate = per type T in {0 (E), 1 (F)}: (dominators, singletons): K_T = ∪ N_O[Z] (Z in dominators, O = 1 - T,
N_O[Z] = sides of type O meeting Z or equal to Z) ∪ singletons.  K_T must contain the partners of the T-members.
"""
import sw


class Path:
    def __init__(self, inst, P):
        self.inst = inst
        self.P = list(P)
        self.r = len(P)
        self.allsides = set(sw.side_ids(inst))
        self.X = [sw.side_mask(inst, i) for i in P]
        self.typ = [i & 1 for i in P]
        self.pid = [(i ^ 1) if (i ^ 1) in self.allsides else None for i in P]
        self.Xp = [sw.side_mask(inst, j) if j is not None else 0 for j in self.pid]

    def contacts(self, a):
        return [c for c in range(self.r) if c != a and (self.Xp[a] & self.X[c])]

    def kind(self, a):
        cs = self.contacts(a)
        fwd = any(c >= a + 2 for c in cs)
        bwd = any(c <= a - 2 for c in cs)
        assert not (fwd and bwd), "Lemma 1 violated"
        if fwd:
            assert all(c >= a + 1 for c in cs), "Lemma 1 (forward) violated"
            return "fwd"
        if bwd:
            assert all(c <= a - 1 for c in cs), "Lemma 1 (backward) violated"
            return "bwd"
        return "loc"

    def f(self, a):
        """members of the other type meeting the partner of a"""
        T = self.typ[a]
        return [c for c in self.contacts(a) if self.typ[c] != T]


def side_cover(inst, Z, O):
    """N_O[Z]: sides of type O meeting Z (Z itself if of type O)."""
    m = sw.side_mask(inst, Z)
    return set(i for i in sw.side_ids(inst) if (i & 1) == O and (sw.side_mask(inst, i) & m))


def cert_for_type(pp, T):
    """Return ('ok', dominators, singletons, info) or ('straddle', (r, p, r1, r2, p1, p2), info)."""
    inst = pp.inst
    r = pp.r
    O = 1 - T
    Tm = [a for a in range(r) if pp.typ[a] == T]
    Om = [a for a in range(r) if pp.typ[a] == O]
    if not Tm:
        return ("ok", [], [], "no members")
    # empty partner: then all T-members lie within distance 1 of it
    for a in Tm:
        if pp.pid[a] is None:
            assert all(abs(b - a) <= 1 for b in Tm), "empty partner but far member of same type"
            return ("ok", [], [pp.pid[b] for b in Tm if pp.pid[b] is not None], "empty partner")
    # 3a: a member whose partner meets at most 3 members of the other type
    best = min(Tm, key=lambda a: len(pp.f(a)))
    if len(pp.f(best)) <= 3:
        sing = [pp.pid[b] for b in Tm if abs(b - best) == 1]
        return ("ok", [pp.pid[best]], sing, "3a low-contact partner at %d (f=%d)" % (best, len(pp.f(best))))
    kinds = {q: pp.kind(q) for q in Om}
    for a in Tm:
        pp.kind(a)
    loc = [q for q in Om if kinds[q] == "loc"]
    if loc:
        q = loc[0]
        sing = [pp.pid[b] for b in Tm if abs(b - q) == 1]
        return ("ok", [pp.P[q]], sing, "case (i) local partner at %d" % q)
    fw = [q for q in Om if kinds[q] == "fwd"]
    bw = [q for q in Om if kinds[q] == "bwd"]
    qf = max(fw) if fw else -10
    qb = min(bw) if bw else r + 10
    assert qb >= qf - 1, "Lemma 2 consequence q_b >= q_f - 1 violated"
    dom = []
    if fw:
        dom.append(pp.P[qf])
    if bw:
        dom.append(pp.P[qb])
    sing = [pp.pid[b] for b in Tm if b in (qf - 1, qb + 1)]
    R = [a for a in Tm if qf < a < qb]
    assert all(pp.typ[c] == T for c in range(max(qf + 1, 0), min(qb, r))), "positions between q_f, q_b not all T"
    for a in Tm:
        if a <= qf - 2:
            assert (pp.Xp[a] & pp.X[qf]), "domination by X_qf fails"
        if a >= qb + 2:
            assert (pp.Xp[a] & pp.X[qb]), "domination by X_qb fails"
    info = ["q_f=%d q_b=%d |R|=%d" % (qf, qb, len(R))]
    for direction in ("fwd", "bwd"):
        rows = [a for a in R if pp.kind(a) == direction]
        if direction == "fwd":
            cols = [q for q in Om if q >= qb]
            rows_core = [a for a in rows if a != qb - 1]
            sing += [pp.pid[a] for a in rows if a == qb - 1]
        else:
            cols = [q for q in Om if q <= qf]
            rows_core = [a for a in rows if a != qf + 1]
            sing += [pp.pid[a] for a in rows if a == qf + 1]
        assert all(pp.kind(a) != "loc" for a in R), "local row in bad case"
        fset = {a: set(pp.f(a)) for a in rows_core}
        for a in rows_core:
            assert fset[a] <= set(cols), "f(a) not inside the columns"
            assert len(fset[a]) >= 4
        bset = {p: set(a for a in R if (pp.Xp[p] & pp.X[a])) for p in cols}
        # straddle search
        for a in rows_core:
            lo, hi = min(fset[a]), max(fset[a])
            for p in cols:
                if not (lo < p < hi):
                    continue
                bs = bset[p]
                below = [x for x in bs if x < a]
                above = [x for x in bs if x > a]
                if below and above:
                    r1, r2 = max(below), min(above)
                    p1 = max(x for x in fset[a] if x < p)
                    p2 = min(x for x in fset[a] if x > p)
                    return ("straddle", (a, p, r1, r2, p1, p2), info)
        # holes per column
        for p in cols:
            holes = [a for a in rows_core if min(fset[a]) < p < max(fset[a]) and p not in fset[a]]
            assert len(holes) <= 2, "more than 2 holes in a column without straddle"
        # disjoint spans
        spans = sorted(((min(fset[a]), max(fset[a]), a) for a in rows_core), key=lambda x: x[1])
        pts = []
        last = None
        for lo, hi, a in spans:
            if last is None or lo > last:
                pts.append(hi)
                last = hi
        assert len(pts) <= 4, "more than 4 disjoint spans without straddle"
        for p in pts:
            dom.append(pp.P[p])
        for a in rows_core:
            if not any(p in fset[a] for p in pts):
                sing.append(pp.pid[a])
        info.append("%s: rows %d, hitting points %d" % (direction, len(rows_core), len(pts)))
    return ("ok", dom, sing, "; ".join(info))


def build_K(inst, dom, sing, O):
    K = set()
    for Z in dom:
        K |= side_cover(inst, Z, O)
    K |= set(x for x in sing if x is not None)
    return K


def verify_cert(inst, P, certs):
    """certs[T] = (dom, sing).  Check K ⊇ partners and return storage."""
    pp = Path(inst, P)
    K = set()
    for T in (0, 1):
        dom, sing = certs[T]
        KT = build_K(inst, dom, sing, 1 - T)
        for a in range(pp.r):
            if pp.typ[a] == T and pp.pid[a] is not None:
                assert pp.pid[a] in KT, "partner not covered (type %d, position %d)" % (T, a)
        K |= KT
    assert sw.is_valid_walk(inst, tuple(P))
    return len(set(P) & K)


def any_straddle(pp):
    """Some straddle of the path (any type), as (a, p, r1, r2, p1, p2), or None."""
    r = pp.r
    for a in range(r):
        if pp.pid[a] is None:
            continue
        T = pp.typ[a]
        for p in range(r):
            if pp.typ[p] == T or pp.pid[p] is None:
                continue
            bl = [x for x in range(a) if pp.typ[x] == T and (pp.Xp[p] & pp.X[x])]
            ab = [x for x in range(a + 1, r) if pp.typ[x] == T and (pp.Xp[p] & pp.X[x])]
            fl = [x for x in range(p) if pp.typ[x] != T and (pp.Xp[a] & pp.X[x])]
            fa = [x for x in range(p + 1, r) if pp.typ[x] != T and (pp.Xp[a] & pp.X[x])]
            if bl and ab and fl and fa:
                r1, r2, p1, p2 = max(bl), min(ab), max(fl), min(fa)
                if r2 < p1 or p2 < r1:
                    return (a, p, r1, r2, p1, p2)
    return None


def certificate(inst, P, prefer_swap=False):
    """Follow the proof.  Returns (path used, certs, storage, info).  With prefer_swap, any straddle of P (of any
    type, anywhere) is used for the swap of Lemma 7 first."""
    pp = Path(inst, P)
    res = {}
    for T in (0, 1):
        out = cert_for_type(pp, T)
        if prefer_swap:
            sd = any_straddle(pp)
            if sd is not None:
                out = ("straddle", sd, None)
        if out[0] == "straddle":
            a, p, r1, r2, p1, p2 = out[1]
            assert r2 - r1 == 2 and p2 - p1 == 2, "straddle not tight on a shortest path"
            Pn = list(P)
            Pn[a] = pp.pid[p]
            Pn[p] = pp.pid[a]
            assert sw.is_valid_walk(inst, tuple(Pn)), "swap path invalid"
            q2 = Path(inst, Pn)
            Ttyp = q2.typ[a]  # type of the new member at a (= type of X'_p)
            certs = {}
            # type of position a in P* is the type of X'_p = T; partner at a is X_p (type O)
            certs[Ttyp] = ([q2.pid[a]], [q2.pid[b] for b in range(q2.r) if q2.typ[b] == Ttyp and abs(b - a) == 1])
            certs[1 - Ttyp] = ([q2.pid[p]], [q2.pid[b] for b in range(q2.r) if q2.typ[b] == 1 - Ttyp and abs(b - p) == 1])
            st = verify_cert(inst, Pn, certs)
            assert st <= 6, "swap certificate storage > 6"
            return Pn, certs, st, "swap at (%d,%d) type %d" % (a, p, T)
        res[T] = (out[1], out[2])
        res[("info", T)] = out[3]
    certs = {0: res[0], 1: res[1]}
    st = verify_cert(inst, P, certs)
    return P, certs, st, "E: %s | F: %s" % (res[("info", 0)], res[("info", 1)])
