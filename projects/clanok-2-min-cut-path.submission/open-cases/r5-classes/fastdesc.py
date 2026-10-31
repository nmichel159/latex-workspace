"""Fast guided DESC costs with bit masks (agent r5-classes, third run).

For a realised instance I and a valid path P: every side gets an index; for each type tau the candidate sets are
N_tau[Z] (Z a side), class groups Omega(C, tau) and single tau-sides, as bit masks over side indices.  mis_P(U) is
computed from per-class masks: a class used on P with type 1 - tau is correct iff Omega(C, tau) is inside U, a
class used with type tau is correct iff Omega(C, tau) is not inside U (r5-classes.md Lemma 2a.1).

guided(I, P, f, g): least mis_P over tau and U = union of <= f neighbourhood sets and <= g groups/single sides.
"""
import itertools


class Prep:
    def __init__(self, I, P):
        self.I = I
        self.P = P
        self.idx = {sd: i for i, sd in enumerate(I.sides)}
        self.pt = {}
        for x in P:
            self.pt[I.scls[x]] = x & 1
        self.nb = {}
        self.extra = {}
        self.om = {}
        for tau in (0, 1):
            nbs = {}
            for z in I.sides:
                m = 0
                Z = I.mask[z]
                for y in I.sides:
                    if (y & 1) == tau and I.mask[y] & Z:
                        m |= 1 << self.idx[y]
                if m and m not in nbs:
                    nbs[m] = z
            self.nb[tau] = list(nbs.items())
            ex = {}
            for C in I.classes:
                m = 0
                for y in I.Omega[(C, tau)]:
                    m |= 1 << self.idx[y]
                if m and m not in ex:
                    ex[m] = ("g", C)
            for y in I.sides:
                if (y & 1) == tau:
                    m = 1 << self.idx[y]
                    if m not in ex:
                        ex[m] = ("1", y)
            self.extra[tau] = list(ex.items())
            # per class of P: (mask of Omega(C, tau), class needs coverage?)
            lst = []
            for C, ty in self.pt.items():
                m = 0
                for y in I.Omega[(C, tau)]:
                    m |= 1 << self.idx[y]
                lst.append((m, ty == 1 - tau))
            self.om[tau] = lst

    def mis(self, tau, U):
        c = 0
        for m, need in self.om[tau]:
            inside = (m & ~U) == 0
            if need != inside:
                c += 1
        return c

    def guided(self, f, g, want=False, cap=None):
        best, arg = None, None
        for tau in (0, 1):
            nbl = self.nb[tau]
            exl = self.extra[tau]
            for a in range(f + 1):
                for combo in itertools.combinations(nbl, a):
                    U0 = 0
                    for m, _ in combo:
                        U0 |= m
                    for b in range(g + 1):
                        for gc in itertools.combinations(exl, b):
                            U = U0
                            for m, _ in gc:
                                U |= m
                            v = self.mis(tau, U)
                            if best is None or v < best:
                                best = v
                                arg = (tau, [z for _, z in combo], [w for _, w in gc])
                                if v == 0 and not want:
                                    return 0
        return (best, arg) if want else best


def guided(I, P, f, g, want=False):
    return Prep(I, P).guided(f, g, want)
