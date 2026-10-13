"""2CH with classes (2CHC): the switch model with ties.

Instance: (N, E, F, s, t, cls).  Nodes 0..N-1, terminals s != t; members i = 0..n-1 with node sets E[i], F[i]
(bit masks) and a class cls[i].  A mode vector assigns one mode (E or F) to every class; every member of a class
picks the side of its class's mode.  Question: are s and t connected in the hypergraph of picked sides?
P2 (with ties): for members i, l of DIFFERENT classes, E[i] & E[l] != 0 or F[i] & F[l] != 0.  Members of one class
need nothing.

ZZ form (theory-dc.md, Theorem 13): bottoms (all equivalent to u), tops (all equivalent to v), one element per member,
elements of one class equivalent, different classes incomparable.  A node x in some E-side gets a bottom b_x, a node in
some F-side gets a top t_x, a node with both gets the fixed real edge b_x t_x; member i is joined to b_x for x in E[i]
and to t_x for x in F[i].  A member outside the down-set (a peak) joins the bottoms of its E-side, inside (a valley)
the tops of its F-side, so the cut graph of a down-set has a u-v path iff the mode vector connects s and t.
Incomparable pairs are exactly the members of different classes; a common real neighbour below both is a bottom b_x
with x in both E-sides, above both a top t_x with x in both F-sides; so ZZ-P2 is 2CHC-P2.

Routines: brute force over class modes, P2 test, conversion to ZZ (zz.ZZ with a preorder), AC / PC answers through
dc-algorithm/zz.py and pcfast.py (imported read-only).
"""
import os
import sys
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
sys.setrecursionlimit(100000)
import zz  # noqa: E402  (read-only import)
import pcfast  # noqa: E402  (read-only import)
from twoch import connected  # noqa: E402


def bits_of(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def classes_of(cls):
    """sorted list of class ids and, for each, the list of members"""
    ids = sorted(set(cls))
    mem = {c: [i for i, ci in enumerate(cls) if ci == c] for c in ids}
    return ids, mem


def p2_missing(E, F, cls):
    n = len(E)
    return [(i, l) for i in range(n) for l in range(i + 1, n)
            if cls[i] != cls[l] and not (E[i] & E[l]) and not (F[i] & F[l])]


def p2_ok(E, F, cls):
    return not p2_missing(E, F, cls)


def picked(inst, modes):
    """modes: dict class -> 0 (E) / 1 (F)"""
    N, E, F, s, t, cls = inst
    return [F[i] if modes[cls[i]] else E[i] for i in range(len(E))]


def solve(inst):
    """brute force: a connecting mode dict, or None"""
    N, E, F, s, t, cls = inst
    ids, _ = classes_of(cls)
    for mask in range(1 << len(ids)):
        modes = {c: (mask >> k) & 1 for k, c in enumerate(ids)}
        if connected(N, picked(inst, modes), s, t):
            return modes
    return None


def all_solutions(inst):
    N, E, F, s, t, cls = inst
    ids, _ = classes_of(cls)
    out = []
    for mask in range(1 << len(ids)):
        modes = {c: (mask >> k) & 1 for k, c in enumerate(ids)}
        if connected(N, picked(inst, modes), s, t):
            out.append(mask)
    return out


def to_zz(inst):
    """2CHC -> zz.ZZ (preorder with ties) and the element names."""
    N, E, F, s, t, cls = inst
    n = len(E)
    inE = 0
    inF = 0
    for i in range(n):
        inE |= E[i]
        inF |= F[i]
    names = ["u"]
    bottom, top = {s: 0}, {}
    for x in range(N):
        if x != s and (inE >> x) & 1:
            bottom[x] = len(names)
            names.append(("b", x))
    m0 = len(names)
    for i in range(n):
        names.append(("m", i))
    for x in range(N):
        if x != t and (inF >> x) & 1:
            top[x] = len(names)
            names.append(("t", x))
    top[t] = len(names)
    names.append("v")
    q = len(names)
    u, v = 0, q - 1
    B = set(bottom.values())
    T = set(top.values())
    le = [[False] * q for _ in range(q)]
    for a in range(q):
        for b in range(q):
            if a == b or a in B or b in T:
                le[a][b] = True
            elif m0 <= a < m0 + n and m0 <= b < m0 + n and cls[a - m0] == cls[b - m0]:
                le[a][b] = True
    R = []
    for x in range(N):
        if x in bottom and x in top and (bottom[x], top[x]) != (u, v):
            R.append((bottom[x], top[x]))
    for i in range(n):
        for x in bits_of(E[i]):
            R.append((bottom[x], m0 + i))
        for x in bits_of(F[i]):
            R.append((m0 + i, top[x]))
    return zz.ZZ(q, None, R, u, v, le=le), names


def zz_answers(inst, do_pc=True, L=None):
    """(exact answer of the ZZ form, AC answer, PC answer or None, the ZZ instance)"""
    z, _ = to_zz(inst)
    ex = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z, L)
    pc = None
    if do_pc:
        pc = pcfast.pc_answer(z, L) if ac else False
    return ex, ac, pc, z


class Builder:
    """Named construction of 2CHC instances."""

    def __init__(self):
        self.nodes = {}
        self.E, self.F, self.cls, self.mname = [], [], [], []

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def member(self, name, cl):
        self.E.append(0)
        self.F.append(0)
        self.cls.append(cl)
        self.mname.append(name)
        return len(self.E) - 1

    def add(self, i, side, *names):
        for nm in names:
            b = 1 << self.node(nm)
            if side == "E":
                self.E[i] |= b
            else:
                self.F[i] |= b

    def inst(self, s="s", t="t"):
        return (len(self.nodes), list(self.E), list(self.F), self.node(s), self.node(t), list(self.cls))


def random_p2_instance(rng, N, n, k, pe, pf, fresh=0.5):
    """N base nodes (s = 0, t = 1), n members in k classes, random sides, then every cross-class pair violating P2
    gets a node in both E-sides or both F-sides (a fresh node with probability `fresh`, else an existing one)."""
    cls = [rng.randrange(k) for _ in range(n)]
    E = [sum(1 << x for x in range(N) if rng.random() < pe) for _ in range(n)]
    F = [sum(1 << x for x in range(N) if rng.random() < pf) for _ in range(n)]
    NN = N
    for i, l in p2_missing(E, F, cls):
        if (E[i] & E[l]) or (F[i] & F[l]):
            continue
        if rng.random() < fresh:
            z = NN
            NN += 1
        else:
            z = rng.randrange(NN)
        if rng.random() < 0.5:
            E[i] |= 1 << z
            E[l] |= 1 << z
        else:
            F[i] |= 1 << z
            F[l] |= 1 << z
    return (NN, E, F, 0, 1, cls)


def fmt(inst):
    N, E, F, s, t, cls = inst
    return "N=%d s=%d t=%d " % (N, s, t) + " ".join(
        "[%d c%d: E=%s F=%s]" % (i, cls[i], bits_of(E[i]), bits_of(F[i])) for i in range(len(E)))


if __name__ == "__main__":
    # self-test: brute force over class modes = exact ZZ answer of the conversion; P2 transfers
    import random
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(seed)
    stats = {"yes": 0, "no": 0, "p2zz_ok": 0, "mismatch": 0}
    for it in range(count):
        N = rng.randint(3, 7)
        n = rng.randint(2, 8)
        k = rng.randint(1, min(n, 5))
        inst = random_p2_instance(rng, N, n, k, rng.choice([0.2, 0.3, 0.4]), rng.choice([0.2, 0.3, 0.4]))
        b = solve(inst) is not None
        z, _ = to_zz(inst)
        e = zz.exact_dfs(z)[0]
        stats["yes" if b else "no"] += 1
        if not z.p2_bad():
            stats["p2zz_ok"] += 1
        if b != e:
            stats["mismatch"] += 1
            print("MISMATCH", fmt(inst), b, e)
        # without P2 repair as well
        cls = [rng.randrange(k) for _ in range(n)]
        E = [sum(1 << x for x in range(N) if rng.random() < 0.3) for _ in range(n)]
        F = [sum(1 << x for x in range(N) if rng.random() < 0.3) for _ in range(n)]
        inst2 = (N, E, F, 0, 1, cls)
        b2 = solve(inst2) is not None
        z2, _ = to_zz(inst2)
        if b2 != zz.exact_dfs(z2)[0]:
            stats["mismatch"] += 1
            print("MISMATCH (no P2)", fmt(inst2))
        if (not z2.p2_bad()) != p2_ok(E, F, cls):
            stats["mismatch"] += 1
            print("P2 MISMATCH", fmt(inst2))
    print(stats)
