"""Switch model SW (theory-dc.md Section 5) with exact and relaxed solvers, and a search for minimal gap instances.

Instance: nb, nt bottoms 0..nb-1 (u = bottom 0) and tops 0..nt-1 (v = top 0); fixed edges F (pairs (b, t));
switches s with Nb[s] (set of bottoms) and Nt[s] (set of tops).  Mode P (switch on the v-side, a peak) joins
Nb[s]; mode V (switch on the u-side, a valley) joins Nt[s].  Question: is there a mode assignment with u ~ v?
P2: every two switches share a bottom or a top.

Vertices of the union-find: bottoms 0..nb-1, tops nb..nb+nt-1.
Usage: python sw2.py gaps SEED COUNT     (random P2 instances; exact vs relaxed; minimal gap instances)
"""
import sys
import random
import itertools


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def f(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def u(self, a, b):
        a, b = self.f(a), self.f(b)
        if a != b:
            self.p[a] = b


def p2(Nb, Nt):
    k = len(Nb)
    return all((Nb[a] & Nb[b]) or (Nt[a] & Nt[b]) for a in range(k) for b in range(a + 1, k))


def connected(nb, nt, F, Nb, Nt, modes):
    uf = UF(nb + nt)
    for b, t in F:
        uf.u(b, nb + t)
    for s, m in enumerate(modes):
        if m is None:
            continue
        grp = [x for x in Nb[s]] if m == 0 else [nb + t for t in Nt[s]]
        for x in grp[1:]:
            uf.u(grp[0], x)
    return uf.f(0) == uf.f(nb)


def exact(nb, nt, F, Nb, Nt):
    k = len(Nb)
    for modes in itertools.product((0, 1), repeat=k):
        if connected(nb, nt, F, Nb, Nt, modes):
            return modes
    return None


def relaxed(nb, nt, F, Nb, Nt):
    uf = UF(nb + nt)
    for b, t in F:
        uf.u(b, nb + t)
    for s in range(len(Nb)):
        g1 = list(Nb[s])
        for x in g1[1:]:
            uf.u(g1[0], x)
        g2 = [nb + t for t in Nt[s]]
        for x in g2[1:]:
            uf.u(g2[0], x)
    return uf.f(0) == uf.f(nb)


def random_inst(rng, nb, nt, k, pf, maxb, maxt):
    F = [(b, t) for b in range(nb) for t in range(nt) if (b, t) != (0, 0) and rng.random() < pf]
    Nb = [frozenset(rng.sample(range(nb), rng.randint(1, min(maxb, nb)))) for _ in range(k)]
    Nt = [frozenset(rng.sample(range(nt), rng.randint(1, min(maxt, nt)))) for _ in range(k)]
    return nb, nt, F, Nb, Nt


def is_gap(inst):
    nb, nt, F, Nb, Nt = inst
    return p2(Nb, Nt) and relaxed(nb, nt, F, Nb, Nt) and exact(nb, nt, F, Nb, Nt) is None


def minimise(inst):
    """Greedy: drop switches, fixed edges, members of Nb/Nt while the instance stays a P2 gap instance."""
    nb, nt, F, Nb, Nt = inst
    changed = True
    while changed:
        changed = False
        for s in range(len(Nb)):
            cand = (nb, nt, F, Nb[:s] + Nb[s + 1:], Nt[:s] + Nt[s + 1:])
            if is_gap(cand):
                nb, nt, F, Nb, Nt = cand
                changed = True
                break
        if changed:
            continue
        for i in range(len(F)):
            cand = (nb, nt, F[:i] + F[i + 1:], Nb, Nt)
            if is_gap(cand):
                F = F[:i] + F[i + 1:]
                changed = True
                break
        if changed:
            continue
        for s in range(len(Nb)):
            for x in Nb[s]:
                if len(Nb[s]) == 1:
                    continue
                Nb2 = Nb[:s] + [Nb[s] - {x}] + Nb[s + 1:]
                if is_gap((nb, nt, F, Nb2, Nt)):
                    Nb = Nb2
                    changed = True
                    break
            if changed:
                break
            for x in Nt[s]:
                if len(Nt[s]) == 1:
                    continue
                Nt2 = Nt[:s] + [Nt[s] - {x}] + Nt[s + 1:]
                if is_gap((nb, nt, F, Nb, Nt2)):
                    Nt = Nt2
                    changed = True
                    break
            if changed:
                break
    # drop unused bottoms / tops (renumber), keeping u = 0, v = 0
    usedb = {0} | {b for b, t in F} | set().union(*Nb) if Nb else {0}
    usedt = {0} | {t for b, t in F} | set().union(*Nt) if Nt else {0}
    mb = {b: i for i, b in enumerate(sorted(usedb))}
    mt = {t: i for i, t in enumerate(sorted(usedt))}
    F = [(mb[b], mt[t]) for b, t in F]
    Nb = [frozenset(mb[b] for b in S) for S in Nb]
    Nt = [frozenset(mt[t] for t in S) for S in Nt]
    return len(mb), len(mt), F, Nb, Nt


def fmt(inst):
    nb, nt, F, Nb, Nt = inst
    s = "bottoms %d tops %d  F=%s\n" % (nb, nt, sorted(F))
    for i in range(len(Nb)):
        s += "   s%d: Nb=%s Nt=%s\n" % (i, sorted(Nb[i]), sorted(Nt[i]))
    return s


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "gaps":
        seed, count = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        found = {}
        stats = {"p2": 0, "gap": 0}
        for it in range(count):
            inst = random_inst(rng, rng.randint(2, 7), rng.randint(2, 7), rng.randint(2, 8), rng.choice([0.05, 0.1, 0.2]),
                               3, 3)
            if not p2(inst[3], inst[4]):
                continue
            stats["p2"] += 1
            if not is_gap(inst):
                continue
            stats["gap"] += 1
            m = minimise(inst)
            key = (len(m[3]), m[0], m[1], len(m[2]))
            if key not in found:
                found[key] = m
        print(stats)
        for key in sorted(found):
            print("switches %d, bottoms %d, tops %d, fixed %d" % key)
            print(fmt(found[key]))
