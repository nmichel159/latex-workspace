"""Families built from the text only (rv-core): Y_k, Y'_k (r4-general.md 6), Y^d_k, Y'^d_k (r5-core.md 2.1),
X_L (r4-general.md 4), R_L in the 2CH form of r4-general 6 (word of types), with optional extra nodes."""
from sw import SW


class Builder:
    def __init__(self):
        self.nodes = {}
        self.E = []
        self.F = []
        self.names = []
        self.rel = []

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def switch(self, name):
        self.names.append(name)
        self.E.append(0)
        self.F.append(0)
        return len(self.names) - 1

    def add(self, w, ty, name):
        n = self.node(name)
        if ty == "E":
            self.E[w] |= 1 << n
        else:
            self.F[w] |= 1 << n
        return n

    def build(self, s="s", t="t"):
        nn = [None] * len(self.nodes)
        for k, v in self.nodes.items():
            nn[v] = k
        return SW(len(self.nodes), self.nodes[s], self.nodes[t], self.E, self.F, self.rel, names=self.names,
                  nodenames=nn)


def other(ty):
    return "F" if ty == "E" else "E"


def yfam(k, contact=False, d=False, back=False):
    """Y_k (contact: Y'_k), with d: Y^d_k (back variant optional)."""
    b = Builder()
    x = [None] + [b.switch("x%d" % j) for j in range(1, 2 * k + 1)]
    mate = [None] + [b.switch("m%d" % c) for c in range(1, k + 1)]
    dd = b.switch("d") if d else None
    pt = lambda j: "E" if j <= k else "F"          # path type
    b.node("s")
    b.node("t")
    b.add(x[1], pt(1), "s")
    b.add(x[2 * k], pt(2 * k), "t")
    for j in range(1, 2 * k):
        b.add(x[j], pt(j), "y%d" % j)
        b.add(x[j + 1], pt(j + 1), "y%d" % j)
    for p in range(1, 2 * k + 1):
        for q in range(p + 1, 2 * k + 1):
            if pt(p) != pt(q):           # z_pq in Fl_p & h_q
                b.add(x[p], other(pt(p)), "z%d_%d" % (p, q))
                b.add(x[q], pt(q), "z%d_%d" % (p, q))
            else:                        # w_pq in Fl_p & Fl_q
                b.add(x[p], other(pt(p)), "w%d_%d" % (p, q))
                b.add(x[q], other(pt(q)), "w%d_%d" % (p, q))
    for c in range(1, k + 1):
        b.rel.append((x[c], mate[c]))     # x_c < m_c
        for bb in range(1, k + 1):
            if bb != c:                   # f_cb in F(m_c) & Fl_b (= F(x_b))
                b.add(mate[c], "F", "f%d_%d" % (c, bb))
                b.add(x[bb], "F", "f%d_%d" % (c, bb))
        for q in range(k + 1, 2 * k + 1):  # e_cq in E(m_c) & Fl_q (= E(x_q))
            b.add(mate[c], "E", "e%d_%d" % (c, q))
            b.add(x[q], "E", "e%d_%d" % (c, q))
        for c2 in range(1, k + 1):
            if c2 != c:
                nm = "g%d_%d" % (min(c, c2), max(c, c2))
                b.add(mate[c], "E", nm)
        if contact:                       # fc_c in F(m_c) & h_{k+c}
            b.add(mate[c], "F", "fc%d" % c)
            b.add(x[k + c], "F", "fc%d" % c)
    if d:
        b.add(dd, "E", "s")
        for c in range(1, k + 1):
            b.add(dd, "E", "gam%d" % c)
            b.add(mate[c], "E", "gam%d" % c)
        for q in range(k + 1, 2 * k + 1):
            b.add(dd, "E", "del%d" % q)
            b.add(x[q], "E", "del%d" % q)
        for bb in range(1, k + 1):
            b.add(dd, "F", "eps%d" % bb)
            b.add(x[bb], "F", "eps%d" % bb)
        if back:
            b.add(dd, "F", "t")
            b.add(dd, "F", "kap")
            b.add(mate[1], "E", "kap")
    G = b.build()
    G.x, G.mate, G.d, G.k = x, mate, dd, k
    return G


def xfam(L):
    """X_L of r4-general 4 (built from the text)."""
    b = Builder()
    x = [None] + [b.switch("x%d" % j) for j in range(1, L + 1)]
    mate = [None] + [b.switch("m%d" % j) for j in range(1, L + 1)]
    pt = lambda j: "E" if j % 2 == 1 else "F"
    b.node("s")
    b.node("t")
    b.add(x[1], pt(1), "s")
    b.add(x[L], pt(L), "t")
    for j in range(1, L):
        b.add(x[j], pt(j), "y%d" % j)
        b.add(x[j + 1], pt(j + 1), "y%d" % j)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                b.add(x[p], other(pt(p)), "z%d_%d" % (p, q))
                b.add(x[q], pt(q), "z%d_%d" % (p, q))
    for j in range(1, L + 1):
        b.add(x[j], other(pt(j)), "t")
    for kk in range(1, L + 1):
        if kk % 2 == 0:
            b.rel.append((mate[kk], x[kk]))      # m_k < x_k
            for nm in ("n%d" % kk, "nn%d" % kk):
                b.add(mate[kk], "E", nm)
                b.add(x[kk], "F", nm)            # h_k = F(x_k)
            for j in range(2, L + 1, 2):
                if j != kk:
                    b.add(mate[kk], "E", "n%d_%d" % (kk, j))
                    b.add(x[j], "E", "n%d_%d" % (kk, j))   # Fl_j = E(x_j)
            for i in range(1, L + 1, 2):
                b.add(mate[kk], "E", "c%d_%d" % (i, kk))
            b.add(mate[kk], "F", "t")
        else:
            b.rel.append((x[kk], mate[kk]))      # m_k > x_k
            b.add(mate[kk], "E", "t")
            for j in range(2, L + 1, 2):
                b.add(mate[kk], "E", "c%d_%d" % (kk, j))
            for nm in ("e%d" % kk, "ee%d" % kk):
                b.add(mate[kk], "F", nm)
                b.add(x[kk], "E", nm)            # h_k = E(x_k)
            for j in range(1, L + 1, 2):
                if j != kk:
                    b.add(mate[kk], "F", "nn%d_%d" % (kk, j))
                    b.add(x[j], "F", "nn%d_%d" % (kk, j))  # Fl_j = F(x_j)
    G = b.build()
    G.x, G.mate = x, mate
    return G


def rword(word, kappa_F=(), kappa_E=()):
    """rigid word family R(word) in the 2CH form of r4-general 6 (z_pq for p<q of different modes, w_pq for equal
    modes); kappa_F: positions j of F-members whose two sides get a common node (E_x & F_x); kappa_E likewise."""
    b = Builder()
    L = len(word)
    x = [None] + [b.switch("x%d" % j) for j in range(1, L + 1)]
    pt = lambda j: word[j - 1]
    b.node("s")
    b.node("t")
    b.add(x[1], pt(1), "s")
    b.add(x[L], pt(L), "t")
    for j in range(1, L):
        b.add(x[j], pt(j), "y%d" % j)
        b.add(x[j + 1], pt(j + 1), "y%d" % j)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if pt(p) != pt(q):
                b.add(x[p], other(pt(p)), "z%d_%d" % (p, q))
                b.add(x[q], pt(q), "z%d_%d" % (p, q))
            else:
                b.add(x[p], other(pt(p)), "w%d_%d" % (p, q))
                b.add(x[q], other(pt(q)), "w%d_%d" % (p, q))
    for j in list(kappa_F) + list(kappa_E):
        b.add(x[j], "E", "kap%d" % j)
        b.add(x[j], "F", "kap%d" % j)
    G = b.build()
    G.x = x
    return G
