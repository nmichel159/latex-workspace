"""Families of 2CH-with-classes instances (agent r5-classes).

Builder: named nodes, switches with E/F node sets and a class name.
rword(W, ...): the rigid word family R(W) of r4-general.md section 6 (2CH form; every switch its own class), with
optional tied mates (the family Y_k of r4-general.md with the one-way relation m_c > x_c replaced by a tie
m_c ~ x_c), contact nodes (Y'_k) and two-sided contact nodes (shortcut contacts).
"""
import ccore as C


class Builder:
    def __init__(self):
        self.nodes = {}
        self.sw = []          # [Eset, Fset]
        self.cl = []
        self.names = []
        self.byname = {}

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def switch(self, name, cls=None):
        self.sw.append([set(), set()])
        self.cl.append(cls if cls is not None else name)
        self.names.append(name)
        self.byname[name] = len(self.sw) - 1
        return len(self.sw) - 1

    def add(self, w, ty, *nodenames):
        if isinstance(w, str) or isinstance(w, tuple):
            w = self.byname[w]
        for nm in nodenames:
            self.sw[w][ty].add(self.node(nm))

    def witness(self, w, v, ty, name=None):
        """a private node in side ty of both switches w and v"""
        if name is None:
            name = ("wit", w, v, ty, len(self.nodes))
        self.add(w, ty, name)
        self.add(v, ty, name)

    def inst(self, s="s", t="t"):
        s_, t_ = self.node(s), self.node(t)
        sw = [(C.orbits(E), C.orbits(F)) for E, F in self.sw]
        clmap = {}
        cl = []
        for c in self.cl:
            if c not in clmap:
                clmap[c] = len(clmap)
            cl.append(clmap[c])
        I = C.Inst(len(self.nodes), s_, t_, sw, cl)
        I.names = list(self.names)
        I.nodenames = {v: k for k, v in self.nodes.items()}
        return I


def rword(W, mates=False, tie=True, contact=0, mate_set=None, builder=None, prefix="", s="s", t="t"):
    """R(W) (word W over 'EF'), optionally with mates of the E-members (tied to their switch if tie=True, else in
    their own class).  contact=1: a private node of F(m_c) in the path side of the c-th F-member (Y'_k);
    contact=2: also a second private node in the path side two positions later (a blocked shortcut)."""
    B = builder or Builder()
    L = len(W)
    xs = []
    for j in range(1, L + 1):
        xs.append(B.switch((prefix + "x", j), cls=(prefix + "x", j)))

    def ty_h(j):
        return 0 if W[j - 1] == "E" else 1

    def h(j, *nm):
        B.add(xs[j - 1], ty_h(j), *nm)

    def fl(j, *nm):
        B.add(xs[j - 1], 1 - ty_h(j), *nm)

    h(1, s)
    h(L, t)
    for j in range(1, L):
        y = (prefix + "y", j)
        h(j, y)
        h(j + 1, y)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if W[p - 1] != W[q - 1]:
                z = (prefix + "z", p, q)
                fl(p, z)
                h(q, z)
            else:
                w = (prefix + "w", p, q)
                fl(p, w)
                fl(q, w)
    if mates:
        Em = [j for j in range(1, L + 1) if W[j - 1] == "E"]
        Fm = [j for j in range(1, L + 1) if W[j - 1] == "F"]
        cs = Em if mate_set is None else [c for c in Em if c in mate_set]
        ms = {}
        for c in cs:
            ms[c] = B.switch((prefix + "m", c), cls=(prefix + "x", c) if tie else (prefix + "m", c))
        for c in cs:
            m = ms[c]
            for b in Em:
                if b != c:
                    nm = (prefix + "f", c, b)
                    B.add(m, 1, nm)
                    fl(b, nm)
            if contact >= 1:
                i = cs.index(c)
                q1 = Fm[i % len(Fm)]
                nm = (prefix + "fc", c, q1)
                B.add(m, 1, nm)
                h(q1, nm)
                if contact >= 2:
                    q2 = q1 + 2
                    if q2 <= L and W[q2 - 1] == "F":
                        nm = (prefix + "fc2", c, q2)
                        B.add(m, 1, nm)
                        h(q2, nm)
            for q in Fm:
                nm = (prefix + "e", c, q)
                B.add(m, 0, nm)
                B.add(xs[q - 1], 0, nm)      # Fl_q = E(x_q) for an F-member
            for c2 in cs:
                if c2 != c:
                    B.add(m, 0, (prefix + "g",) + tuple(sorted((c, c2))))
    return B


def ytie(k, contact=0):
    B = rword("E" * k + "F" * k, mates=True, tie=True, contact=contact)
    return B.inst()


if __name__ == "__main__":
    import sys
    for k in range(2, 6):
        for contact in (0, 1, 2):
            I = ytie(k, contact)
            sols = C.all_solutions(I) if I.k <= 18 else None
            st, fx = C.prune(I)
            print("k=%d contact=%d n=%d classes=%d N=%d P2=%s sols=%s prune=%s fixed=%d" % (
                k, contact, I.n, I.k, I.N, C.p2_ok(I), None if sols is None else len(sols), st, len(fx)))
