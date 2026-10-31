"""Bounded-description mode vectors (agent r5-classes).

For a type tau and a set U of tau-sides, sigma_U puts a class into mode 1 - tau iff all its tau-sides lie in U
(a class without tau-sides included), and into mode tau otherwise.  decide_desc(inst, f, e) tries every tau, every
U = union of at most f sets N_tau[Z] (Z any side) and every set of at most e classes whose mode is flipped
relative to sigma_U, and checks s-t connectivity.  It is trivially sound (it only accepts a connecting mode
vector); its completeness on all yes-instances is Conjecture C' of r5-classes.md.

min_desc(inst, fmax, emax) returns the least (f, e) (lexicographic in f + e, then f) for which decide_desc accepts.
"""
import itertools
import ccore as C


def nb_sets(inst, tau):
    out = {}
    for z in inst.sides:
        S = inst.N_of(tau, z)
        if S not in out:
            out[S] = z
    return list(out.items())


def sigma_U(inst, tau, U):
    modes = {}
    for c in inst.classes:
        om = inst.Omega[(c, tau)]
        modes[c] = (1 - tau) if om <= U else tau
    return modes


def connects(inst, modes):
    return C.connected_masks(C.picked_masks(inst, modes), inst.s, inst.t)


def decide_desc(inst, f, e, want=False):
    if inst.s == inst.t:
        return True
    for tau in (0, 1):
        sets = nb_sets(inst, tau)
        for a in range(f + 1):
            for combo in itertools.combinations(sets, a):
                U = frozenset().union(*[S for S, _ in combo]) if combo else frozenset()
                base = sigma_U(inst, tau, U)
                for b in range(e + 1):
                    for flip in itertools.combinations(inst.classes, b):
                        modes = dict(base)
                        for c in flip:
                            modes[c] = 1 - modes[c]
                        if connects(inst, modes):
                            if want:
                                return (tau, [z for _, z in combo], flip, modes)
                            return True
    return None if want else False


def min_desc(inst, fmax=2, emax=2):
    best = None
    for tot in range(0, fmax + emax + 1):
        for f in range(0, min(fmax, tot) + 1):
            e = tot - f
            if e > emax:
                continue
            if decide_desc(inst, f, e):
                return (f, e)
    return None


if __name__ == "__main__":
    import sys
    import random
    import cfam
    import branchfam as BF
    for k in range(2, 6):
        for name, I in (("ytie0", cfam.ytie(k, 0)), ("ytie2", cfam.ytie(k, 2)), ("YB", BF.ybranch(k)),
                        ("YBF2", BF.ybranch_fake(k, contact=2, nfake=2))):
            r = decide_desc(I, 1, 2, want=True)
            print(k, name, "classes", I.k, "min_desc", min_desc(I, 2, 2),
                  "witness", None if r is None or r is False else (r[0], [I.sname(z) for z in r[1]], r[2]), flush=True)
