"""Generators of the review rv-classes-q: random instances with classes and P2 repair, planted paths with
multi-position classes, mates and bipartite tournaments between the two types."""
import random

from qcore import Inst


def rand_mask(rng, N, p):
    m = 0
    for x in range(N):
        if rng.random() < p:
            m |= 1 << x
    return m


def p2_repair(rng, N, sw, cl, fresh=0.5):
    """for every pair of switches of different classes without P2 add a node to both E-sides or both F-sides
    (a fresh private node with probability `fresh`, else a random existing node).  Returns the new N."""
    n = len(sw)
    for w in range(n):
        for v in range(w + 1, n):
            if cl[w] == cl[v]:
                continue
            if (sw[w][0] & sw[v][0]) or (sw[w][1] & sw[v][1]):
                continue
            ty = rng.randrange(2)
            if rng.random() < fresh:
                x = N
                N += 1
            else:
                x = rng.randrange(N)
            sw[w][ty] |= 1 << x
            sw[v][ty] |= 1 << x
    return N


def random_instance(rng, N, n, c, pE, pF, fresh=0.5, p2=True):
    sw = [[rand_mask(rng, N, pE), rand_mask(rng, N, pF)] for _ in range(n)]
    cl = [rng.randrange(c) for _ in range(n)]
    if p2:
        N = p2_repair(rng, N, sw, cl, fresh)
    return Inst(N, 0, 1, sw, cl)


class Builder:
    def __init__(self):
        self.N = 2          # s = 0, t = 1
        self.sw = []
        self.cl = []

    def node(self):
        self.N += 1
        return self.N - 1

    def switch(self, C):
        self.sw.append([0, 0])
        self.cl.append(C)
        return len(self.sw) - 1

    def add(self, w, ty, x):
        self.sw[w][ty] |= 1 << x

    def share(self, a, b):
        """a fresh private node in the sides a = (w, ty) and b = (w', ty')"""
        x = self.node()
        self.add(a[0], a[1], x)
        self.add(b[0], b[1], x)
        return x

    def inst(self):
        return Inst(self.N, 0, 1, [list(s) for s in self.sw], list(self.cl))


def planted(rng, r, nTc, nOc, T=0, mates=2, offc=0, offn=1, p_contact=0.3, p_live=0.2, p_tour=0.5,
            local_only=False, word=None):
    """A planted path X_1 .. X_r with types (T or O = 1 - T) and classes: nTc classes of type T and nOc of type O
    distributed over the positions (several positions per class), `mates` extra switches per class of P,
    `offc` classes off the path with `offn` switches each.  P2 between switches of different classes is completed
    by private nodes; the option is chosen by the rules below (exact shortest-path test is done by the caller).
    Rules: member-member pairs of the same type at distance >= 2: partners meet (forced); opposite types: cross
    contact chosen at random among the orientations whose contact keeps the span rule (A3) and, if local_only,
    only for |a - b| = 1.  Mates are dead (their P-consistent side meets no member) except with probability p_live.
    Mate-mate pairs of a T-class and an O-class: O-sides meet with probability p_tour, else T-sides (tournament).
    Returns (Inst, P) with P the planted path (side ids)."""
    O = 1 - T
    b = Builder()
    if word is None:
        word = [rng.randrange(2) for _ in range(r)]
    word = list(word)
    Tcls = list(range(nTc))
    Ocls = list(range(nTc, nTc + nOc))
    pos_cls = []
    for a in range(r):
        if word[a] == T:
            pos_cls.append(rng.choice(Tcls))
        else:
            pos_cls.append(rng.choice(Ocls))
    used = sorted(set(pos_cls))
    members = []
    for a in range(r):
        w = b.switch(pos_cls[a])
        members.append(w)
    # path nodes
    b.add(members[0], word[0], 0)
    b.add(members[-1], word[-1], 1)
    for a in range(r - 1):
        x = b.node()
        b.add(members[a], word[a], x)
        b.add(members[a + 1], word[a + 1], x)
    span = {}
    for a, C in enumerate(pos_cls):
        lo, hi = span.get(C, (a, a))
        span[C] = (min(lo, a), max(hi, a))
    # mates
    mates_of = {}
    for C in used:
        mates_of[C] = [b.switch(C) for _ in range(mates)]
    # off-path classes
    off = []
    nxt = nTc + nOc
    for _ in range(offc):
        off.append([b.switch(nxt) for _ in range(offn)])
        nxt += 1
    ctype = {C: (T if C in Tcls else O) for C in used}
    # member-member P2
    for a in range(r):
        for c in range(a + 1, r):
            wa, wc = members[a], members[c]
            if pos_cls[a] == pos_cls[c]:
                continue
            if word[a] == word[c]:
                if c - a >= 2:
                    b.share((wa, 1 - word[a]), (wc, 1 - word[c]))
                continue
            # opposite types: X'_a meets X_c (c contact of a) or X_a meets X'_c (a contact of c)
            opts = []
            for (x, y) in ((a, c), (c, a)):
                # partner of x meets member y; span rule for the class of x: contacts not on both sides
                lo, hi = span[pos_cls[x]]
                if local_only and abs(x - y) > 1:
                    continue
                opts.append((x, y))
            if not opts:
                opts = [(a, c), (c, a)]
            x, y = rng.choice(opts)
            b.share((members[x], 1 - word[x]), (members[y], word[y]))
    # extra contacts of partners (random, local)
    for a in range(r):
        for c in (a - 1, a + 1):
            if 0 <= c < r and rng.random() < p_contact:
                b.share((members[a], 1 - word[a]), (members[c], word[c]))
    # mates vs members, mates vs mates, off-path
    allsw = list(range(len(b.sw)))
    clsof = b.cl
    memb_pos = {w: a for a, w in enumerate(members)}

    def typeof(w):
        C = clsof[w]
        return ctype.get(C)

    for i in allsw:
        for j in allsw:
            if j <= i or clsof[i] == clsof[j]:
                continue
            if i in memb_pos and j in memb_pos:
                continue
            # i or j is a mate or an off-path switch
            ti, tj = typeof(i), typeof(j)
            if i in memb_pos or j in memb_pos:
                m, z = (i, j) if i in memb_pos else (j, i)     # m member, z mate/off
                a = memb_pos[m]
                tz = typeof(z)
                ta = word[a]
                live = rng.random() < p_live
                if tz is None:
                    # off-path switch: both sides P-consistent; meet the partner of the member (dead)
                    b.share((m, 1 - ta), (z, 1 - ta))
                    continue
                # z is a mate of a class of type tz
                if ta == tz:
                    # z^{tz} meets X_a (live contact) or z^{1-tz} meets X'_a (dead)
                    if live:
                        b.share((m, ta), (z, tz))
                    else:
                        b.share((m, 1 - ta), (z, 1 - tz))
                else:
                    # ta = 1 - tz: z^{1-tz} meets X_a (contact of the needed side) or z^{tz} meets X'_a (dead)
                    if live:
                        b.share((m, ta), (z, 1 - tz))
                    else:
                        b.share((m, 1 - ta), (z, tz))
                continue
            # both mates / off-path
            if ti is not None and tj is not None and ti != tj:
                # tournament between a mate of a T-class and a mate of an O-class
                if rng.random() < p_tour:
                    b.share((i, O), (j, O))
                else:
                    b.share((i, T), (j, T))
            else:
                ty = rng.randrange(2)
                b.share((i, ty), (j, ty))
    P = tuple(2 * members[a] + word[a] for a in range(r))
    return b.inst(), P
