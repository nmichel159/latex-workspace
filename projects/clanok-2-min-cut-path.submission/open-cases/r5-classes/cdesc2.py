"""Mode descriptions sigma_U (r5-classes.md section 2a) with neighbourhoods, class groups and single sides, and the
exact least misclassification over all solutions.

desc_cost(inst, f, g, sols): least over tau in {E, F} and over U = union of at most f sets N_tau[Z] (Z any side) and
at most g sets that are class groups Omega(C, tau) or single tau-sides, of min over solutions mu of the Hamming
distance between sigma_U and mu.  DESC(f, g, e) accepts iff desc_cost <= e (Lemma 2a.1 and its converse: a mode
vector within distance e of sigma_U is sigma_U^Phi for some |Phi| <= e).
"""
import itertools
import ccore as C


def solutions_masks(inst):
    """all connecting mode vectors as class bitmasks (bit j = 1: class j in mode F)"""
    out = []
    for mask in range(1 << inst.k):
        modes = {c: (mask >> j) & 1 for j, c in enumerate(inst.classes)}
        if C.connected_masks(C.picked_masks(inst, modes), inst.s, inst.t):
            out.append(mask)
    return out


def side_index(inst):
    idx = {sd: i for i, sd in enumerate(inst.sides)}
    return idx


def prep(inst):
    idx = side_index(inst)
    P = {}
    for tau in (0, 1):
        nb = {}
        for z in inst.sides:
            m = 0
            for y in inst.sides:
                if (y & 1) == tau and inst.mask[y] & inst.mask[z]:
                    m |= 1 << idx[y]
            if m and m not in nb:
                nb[m] = z
        grp = {}
        for c in inst.classes:
            m = 0
            for y in inst.Omega[(c, tau)]:
                m |= 1 << idx[y]
            if m and m not in grp:
                grp[m] = ("class", c)
        for y in inst.sides:
            if (y & 1) == tau:
                m = 1 << idx[y]
                if m not in grp:
                    grp[m] = ("side", y)
        om = [0] * inst.k
        for j, c in enumerate(inst.classes):
            m = 0
            for y in inst.Omega[(c, tau)]:
                m |= 1 << idx[y]
            om[j] = m
        P[tau] = (list(nb.items()), list(grp.items()), om)
    return P


def sigma(om, U, tau):
    """class bitmask of sigma_U (bit = 1 means mode F)"""
    s = 0
    other = 1 - tau
    for j, m in enumerate(om):
        mode = other if (m & ~U) == 0 else tau
        if mode == 1:
            s |= 1 << j
    return s


def desc_cost(inst, f, g, sols=None, want=False, P=None):
    if sols is None:
        sols = solutions_masks(inst)
    if not sols:
        return None
    if P is None:
        P = prep(inst)
    best = None
    bw = None
    for tau in (0, 1):
        nb, grp, om = P[tau]
        for a in range(f + 1):
            for combo in itertools.combinations(nb, a):
                U0 = 0
                for m, _ in combo:
                    U0 |= m
                for b in range(g + 1):
                    for gc in itertools.combinations(grp, b):
                        U = U0
                        for m, _ in gc:
                            U |= m
                        s = sigma(om, U, tau)
                        d = min(bin(s ^ x).count("1") for x in sols)
                        if best is None or d < best:
                            best = d
                            bw = (tau, [inst.sname(z) for _, z in combo], [w for _, w in gc])
                            if best == 0 and not want:
                                return 0
    return (best, bw) if want else best
