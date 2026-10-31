"""Generators of planted instances whose planted path P is a shortest valid path.

band():        levels design: every side spans at most one level (P shortest by the level argument, asserted
               by the exact search as well); all non-member sides lie in a band; random tournaments between the
               mates of T-classes and of O-classes; many classes with many positions.
incremental(): general planted path, P2 completed pair by pair with fresh or shared nodes, each addition kept
               only if no valid path shorter than r appears (exact iterative-deepening search); far contacts,
               multi-position classes, mates, off-path classes, extra random intersections.
"""
import random

from qcore import Inst, bits


class B:
    def __init__(self):
        self.N = 2
        self.sw = []
        self.cl = []

    def node(self):
        self.N += 1
        return self.N - 1

    def switch(self, C):
        self.sw.append([0, 0])
        self.cl.append(C)
        return len(self.sw) - 1

    def inst(self):
        return Inst(self.N, 0, 1, [list(s) for s in self.sw], list(self.cl))


def band(rng, r, lam, nTc, nOc, mates_T, mates_O, offc=0, p_tour=0.5, p_memb=0.5, word=None, T=0):
    """Levels: s = 0, junction j_a (between X_a and X_{a+1}, 1-based) = a, t = r.  Member X_a spans [a-1, a].
    Every non-member side spans the band [lam, lam + 1].  Positions in Wd = {lam, lam+1, lam+2} may have either
    type; the others have type T.  Classes: T-positions spread over nTc classes, O-positions over nOc classes.
    Mates: mates_T per T-class, mates_O per O-class (all their sides in the band); offc off-path classes with 2
    switches each.  P2 for each pair of switches of different classes by a private node at a common level of the
    chosen sides (random among the feasible options).  Returns (Inst, P, info)."""
    O = 1 - T
    b = B()
    Wd = {lam, lam + 1, lam + 2}
    if word is None:
        word = [T if (a + 1) not in Wd else rng.randrange(2) for a in range(r)]
    Tcls = list(range(nTc))
    Ocls = list(range(nTc, nTc + nOc))
    pos_cls = []
    tcount, ocount = 0, 0
    for a in range(r):
        if word[a] == T:
            pos_cls.append(Tcls[tcount % nTc] if rng.random() < 0.5 else rng.choice(Tcls))
            tcount += 1
        else:
            pos_cls.append(Ocls[ocount % nOc] if rng.random() < 0.5 else rng.choice(Ocls))
            ocount += 1
    members = [b.switch(pos_cls[a]) for a in range(r)]
    level = {0: 0, 1: r}
    b.sw[members[0]][word[0]] |= 1 << 0
    b.sw[members[-1]][word[-1]] |= 1 << 1
    for a in range(r - 1):
        x = b.node()
        level[x] = a + 1
        b.sw[members[a]][word[a]] |= 1 << x
        b.sw[members[a + 1]][word[a + 1]] |= 1 << x
    used = sorted(set(pos_cls))
    ctype = {C: (T if C in Tcls else O) for C in used}
    mates = {}
    for C in used:
        cnt = mates_T if ctype[C] == T else mates_O
        mates[C] = [b.switch(C) for _ in range(cnt)]
    nxt = nTc + nOc
    for _ in range(offc):
        b.switch(nxt)
        b.switch(nxt)
        nxt += 1
    memb_pos = {w: a for a, w in enumerate(members)}

    def interval(w, ty):
        if w in memb_pos:
            a = memb_pos[w]
            if word[a] == ty:
                return (a, a + 1)          # 0-based a -> member X_{a+1} spans [a, a+1]
        return (lam, lam + 1)

    n = len(b.sw)
    for i in range(n):
        for j in range(i + 1, n):
            if b.cl[i] == b.cl[j]:
                continue
            if (b.sw[i][0] & b.sw[j][0]) or (b.sw[i][1] & b.sw[j][1]):
                continue
            opts = []
            for ty in (0, 1):
                li, lj = interval(i, ty), interval(j, ty)
                lo, hi = max(li[0], lj[0]), min(li[1], lj[1])
                if lo <= hi:
                    opts.append((ty, lo, hi))
            assert opts, ("no feasible P2 option", i, j)
            # tournament bias between mates of T-classes and of O-classes
            ci, cj = ctype.get(b.cl[i]), ctype.get(b.cl[j])
            if len(opts) == 2 and ci is not None and cj is not None and ci != cj:
                ty = O if rng.random() < p_tour else T
                opt = [o for o in opts if o[0] == ty][0]
            elif len(opts) == 2 and (i in memb_pos or j in memb_pos):
                opt = opts[0] if rng.random() < p_memb else opts[1]
            else:
                opt = rng.choice(opts)
            ty, lo, hi = opt
            x = b.node()
            level[x] = rng.randint(lo, hi)
            b.sw[i][ty] |= 1 << x
            b.sw[j][ty] |= 1 << x
    I = b.inst()
    # assert the level property: every side spans at most one level
    for x in I.sides:
        lv = [level[v] for v in bits(I.mask[x])]
        assert max(lv) - min(lv) <= 1, ("level span", x, lv)
    P = tuple(2 * members[a] + word[a] for a in range(r))
    return I, P, {"word": word, "pos_cls": pos_cls}


def no_shorter(I, r):
    """True iff no valid path of length < r exists"""
    L, _ = I.shortest_paths_dfs(limit=1, maxlen=r - 1)
    return L is None


def incremental(rng, r, nTc, nOc, mates=1, offc=0, offn=1, p_extra=0.3, n_extra=None, p_fresh=0.6,
                word=None, T=0, max_checks=4000):
    """Planted path; P2 completed pair by pair (random order); an addition is kept only if no shorter valid path
    appears.  Returns (Inst, P) or None if some P2 pair cannot be completed."""
    O = 1 - T
    b = B()
    if word is None:
        word = [rng.randrange(2) for _ in range(r)]
    Tcls = list(range(nTc))
    Ocls = list(range(nTc, nTc + nOc))
    pos_cls = [rng.choice(Tcls) if word[a] == T else rng.choice(Ocls) for a in range(r)]
    members = [b.switch(pos_cls[a]) for a in range(r)]
    b.sw[members[0]][word[0]] |= 1 << 0
    b.sw[members[-1]][word[-1]] |= 1 << 1
    for a in range(r - 1):
        x = b.node()
        b.sw[members[a]][word[a]] |= 1 << x
        b.sw[members[a + 1]][word[a + 1]] |= 1 << x
    used = sorted(set(pos_cls))
    for C in used:
        for _ in range(mates):
            b.switch(C)
    nxt = nTc + nOc
    for _ in range(offc):
        for _ in range(offn):
            b.switch(nxt)
        nxt += 1
    P = tuple(2 * members[a] + word[a] for a in range(r))
    checks = [0]

    def ok():
        checks[0] += 1
        I = b.inst()
        return no_shorter(I, r)

    def try_add(i, ty_i, j, ty_j):
        """add a node to side (i, ty_i) and (j, ty_j): fresh, or an existing node of one of them"""
        cands = []
        if rng.random() < p_fresh:
            cands.append(None)
        ni = bits(b.sw[i][ty_i])
        nj = bits(b.sw[j][ty_j])
        ex = [(x, j, ty_j) for x in ni if x not in (0, 1)] + [(x, i, ty_i) for x in nj if x not in (0, 1)]
        rng.shuffle(ex)
        cands.extend(ex[:3])
        if None not in cands:
            cands.append(None)
        for cnd in cands:
            if cnd is None:
                x = b.node()
                b.sw[i][ty_i] |= 1 << x
                b.sw[j][ty_j] |= 1 << x
                if ok():
                    return True
                b.sw[i][ty_i] &= ~(1 << x)
                b.sw[j][ty_j] &= ~(1 << x)
            else:
                x, w, ty = cnd
                if (b.sw[w][ty] >> x) & 1:
                    continue
                b.sw[w][ty] |= 1 << x
                if ok():
                    return True
                b.sw[w][ty] &= ~(1 << x)
        return False

    n = len(b.sw)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if b.cl[i] != b.cl[j]]
    rng.shuffle(pairs)
    for (i, j) in pairs:
        if (b.sw[i][0] & b.sw[j][0]) or (b.sw[i][1] & b.sw[j][1]):
            continue
        tys = [0, 1]
        rng.shuffle(tys)
        done = False
        for ty in tys:
            if try_add(i, ty, j, ty):
                done = True
                break
        if not done:
            return None
        if checks[0] > max_checks:
            return None
    # extra intersections between random sides (any types)
    sides = [(w, ty) for w in range(n) for ty in (0, 1)]
    ne = n_extra if n_extra is not None else int(p_extra * n)
    for _ in range(ne):
        (i, ti), (j, tj) = rng.sample(sides, 2)
        if i == j:
            continue
        try_add(i, ti, j, tj)
    I = b.inst()
    assert I.p2()
    return I, P


def word_of(rng, r, kind, T=0):
    """type words: rand (independent), zones (O-zone, T-run, O-zone), blocks (runs of length 2-4)"""
    O = 1 - T
    if kind == "rand":
        return [rng.randrange(2) for _ in range(r)]
    if kind == "zones":
        k = rng.randint(1, max(1, r // 3))
        m = rng.randint(1, max(1, r // 3))
        w = [O if rng.random() < 0.75 else T for _ in range(k)] + [T] * m
        w += [O if rng.random() < 0.75 else T for _ in range(r - len(w))]
        return w[:r]
    if kind == "blocks":
        w = []
        while len(w) < r:
            w += [rng.randrange(2)] * rng.randint(2, 4)
        return w[:r]
    raise ValueError(kind)
