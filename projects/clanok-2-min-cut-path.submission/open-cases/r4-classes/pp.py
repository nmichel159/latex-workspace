"""Partner-pair descriptions (agent r4-classes; r4-classes.md §3).

For a type tau and two sides Z1, Z2 of type tau, U = N_tau[Z1] ∪ N_tau[Z2] ∪ Ω(cls(Z1), tau) ∪ Ω(cls(Z2), tau)
(N_tau[Z] = sides of type tau meeting Z; Ω(C, tau) = tau-sides of the switches of class C).  sigma_U puts a class C
into mode 1 - tau iff Ω(C, tau) ⊆ U, else into mode tau (r5-classes §2a).  Also the 'few classes' descriptions
U = union of at most 3 class groups Ω(C, tau).
decide_pp(inst, e): try every such U for both tau and every set Phi of at most e classes to flip; accept iff some
sigma_U^Phi connects s and t.  Sound for every e (it accepts only a connecting mode vector); complete whenever some
shortest valid path satisfies the partner-pair condition with misclassification <= e (r4-classes.md Prop. 3.1).
Time O(D^2 k^e (N + D)) for D sides, k classes.
Instances: r5-classes/ccore.Inst (read-only import).
"""
import os
import sys
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "r5-classes"))
import ccore as C  # noqa: E402


class PP:
    def __init__(self, inst):
        self.I = inst
        S = inst.sides
        self.idx = {x: i for i, x in enumerate(S)}
        self.nb = {}
        for z in S:
            for tau in (0, 1):
                m = 0
                for y in S:
                    if (y & 1) == tau and inst.mask[y] & inst.mask[z]:
                        m |= 1 << self.idx[y]
                self.nb[(z, tau)] = m
        self.om = {}
        for c in inst.classes:
            for tau in (0, 1):
                m = 0
                for y in inst.Omega[(c, tau)]:
                    m |= 1 << self.idx[y]
                self.om[(c, tau)] = m

    def sigma(self, tau, U):
        return {c: (1 - tau) if (self.om[(c, tau)] & ~U) == 0 else tau for c in self.I.classes}

    def connects(self, modes):
        I = self.I
        return C.connected_masks(C.picked_masks(I, modes), I.s, I.t)

    def descriptions(self):
        I = self.I
        seen = set()
        for tau in (0, 1):
            Ts = [z for z in I.sides if (z & 1) == tau]
            for a in range(len(Ts)):
                for b in range(a, len(Ts)):
                    z1, z2 = Ts[a], Ts[b]
                    U = (self.nb[(z1, tau)] | self.nb[(z2, tau)] | self.om[(I.scls[z1], tau)]
                         | self.om[(I.scls[z2], tau)])
                    if (tau, U) not in seen:
                        seen.add((tau, U))
                        yield tau, U, ("pp", z1, z2)
            for g in range(0, 4):
                for cs in itertools.combinations(I.classes, g):
                    U = 0
                    for c in cs:
                        U |= self.om[(c, tau)]
                    if (tau, U) not in seen:
                        seen.add((tau, U))
                        yield tau, U, ("groups", cs)

    def decide(self, e, want=False):
        I = self.I
        if I.s == I.t:
            return (True, None) if want else True
        for tau, U, lab in self.descriptions():
            base = self.sigma(tau, U)
            for j in range(e + 1):
                for Phi in itertools.combinations(I.classes, j):
                    modes = dict(base)
                    for c in Phi:
                        modes[c] = 1 - modes[c]
                    if self.connects(modes):
                        return (True, (tau, lab, Phi, modes)) if want else True
        return (False, None) if want else False

    def least_e(self, emax):
        """least e <= emax for which decide accepts (None if none)."""
        I = self.I
        best = None
        for tau, U, lab in self.descriptions():
            base = self.sigma(tau, U)
            for j in range(emax + 1 if best is None else best):
                found = False
                for Phi in itertools.combinations(I.classes, j):
                    modes = dict(base)
                    for c in Phi:
                        modes[c] = 1 - modes[c]
                    if self.connects(modes):
                        found = True
                        break
                if found:
                    best = j
                    break
            if best == 0:
                return 0
        return best


def decide_pp(inst, e, want=False):
    return PP(inst).decide(e, want)
