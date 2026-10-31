"""Family W_n ("wheel" base with floating mates), r5-core.md Section 4.

Base (switch model): positions 1..4n in four blocks A = [1, n] (type E), B = [n+1, 2n] (F), C = [2n+1, 3n] (E),
D = [3n+1, 4n] (F).  Switch x_j with path side h_j of the block type and flip side Fl_j of the other type.
Nodes: s in h_1, t in h_4n, y_j in h_j and h_{j+1}; for same-type p < q a node w_pq in Fl_p and Fl_q; for
opposite-type pairs the contact rule  A->B, B->C, C->D, D->A:  for a in A, b in B a node in Fl_a and h_b; for b in B,
c in C a node in Fl_b and h_c; for c in C, d in D a node in Fl_c and h_d; for d in D, a in A a node in Fl_d and h_a.
So every member has n contacts of the other type (f(A) = B, f(B) = C, f(C) = D, f(D) = A).
Mates (mates=True): an up-mate m_j > x_j for every E-position j (A and C), a down-mate mu_j < x_j for every
F-position j (B and D):
  F(m_j)  = {f_jb : b E-position, b != j}, f_jb added to Fl_b;   E(m_j) = {e_jq : q F-position}, e_jq added to Fl_q,
            plus g-nodes shared pairwise by the up-mates;
  E(mu_j) = {f'_jq : q F-position, q != j}, f'_jq added to Fl_q;  F(mu_j) = {e'_ja : a E-position}, e'_ja added to
            Fl_a, plus g'-nodes shared pairwise by the down-mates;
  up-mate m_a and down-mate mu_q share a node of F(m_a) and F(mu_q).
Every mate side meets only flip sides and other mate sides ("floating").
"""
from gcore import Gen


def wfam(n, mates=True, rule=("AB", "BC", "CD", "DA"), pairing="F", seed=0):
    """pairing: how an up-mate m_a and a down-mate mu_q meet P2: "F" (node in F(m_a) and F(mu_q)), "E" (node in
    E(m_a) and E(mu_q)), "random" (each pair E or F with probability 1/2, generator seeded by `seed`)."""
    import random as _random
    rng = _random.Random(seed)
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    L = 4 * n

    def block(j):
        return "ABCD"[(j - 1) // n]

    def typ(j):
        return "E" if block(j) in "AC" else "F"

    E = {j: set() for j in range(1, L + 1)}
    F = {j: set() for j in range(1, L + 1)}

    def h(j):
        return E[j] if typ(j) == "E" else F[j]

    def fl(j):
        return F[j] if typ(j) == "E" else E[j]

    s, t = node("s"), node("t")
    h(1).add(s)
    h(L).add(t)
    for j in range(1, L):
        y = node(("y", j))
        h(j).add(y)
        h(j + 1).add(y)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if typ(p) == typ(q):
                w = node(("w", p, q))
                fl(p).add(w)
                fl(q).add(w)
            else:
                bp, bq = block(p), block(q)
                pair = bp + bq
                if pair in rule:            # p's flip side meets q's path side
                    z = node(("z", p, q))
                    fl(p).add(z)
                    h(q).add(z)
                elif (bq + bp) in rule:     # q's flip side meets p's path side
                    z = node(("z", q, p))
                    fl(q).add(z)
                    h(p).add(z)
                else:
                    raise ValueError("no contact rule for %s" % pair)
    swE = [E[j] for j in range(1, L + 1)]
    swF = [F[j] for j in range(1, L + 1)]
    names = [("x", j) for j in range(1, L + 1)]
    rel = []
    if mates:
        Epos = [j for j in range(1, L + 1) if typ(j) == "E"]
        Fpos = [j for j in range(1, L + 1) if typ(j) == "F"]
        up_idx, dn_idx = {}, {}
        for j in Epos:
            me, mf = set(), set()
            for b in Epos:
                if b != j:
                    x = node(("f", j, b))
                    mf.add(x)
                    fl(b).add(x)
            for q in Fpos:
                x = node(("e", j, q))
                me.add(x)
                fl(q).add(x)
            for j2 in Epos:
                if j2 != j:
                    me.add(node(("g",) + tuple(sorted((j, j2)))))
            swE.append(me)
            swF.append(mf)
            names.append(("m", j))
            up_idx[j] = len(names) - 1
            rel.append((j - 1, len(names) - 1))          # x_j <= m_j
        for q in Fpos:
            me, mf = set(), set()
            for q2 in Fpos:
                if q2 != q:
                    x = node(("f'", q, q2))
                    me.add(x)
                    fl(q2).add(x)
            for a in Epos:
                x = node(("e'", q, a))
                mf.add(x)
                fl(a).add(x)
            for q2 in Fpos:
                if q2 != q:
                    mf.add(node(("g'",) + tuple(sorted((q, q2)))))
            swE.append(me)
            swF.append(mf)
            names.append(("mu", q))
            dn_idx[q] = len(names) - 1
            rel.append((len(names) - 1, q - 1))          # mu_q <= x_q
        for a in Epos:
            for q in Fpos:
                x = node(("hm", a, q))
                side = pairing if pairing in ("E", "F") else rng.choice("EF")
                if side == "F":
                    swF[up_idx[a]].add(x)
                    swF[dn_idx[q]].add(x)
                else:
                    swE[up_idx[a]].add(x)
                    swE[dn_idx[q]].add(x)
    m = len(names)
    le = [[a == b for b in range(m)] for a in range(m)]
    for a, b in rel:
        le[a][b] = True
    N = len(nodes)
    Em = [sum(1 << x for x in e) for e in swE]
    Fm = [sum(1 << x for x in f) for f in swF]
    G = Gen(N, Em, Fm, le, s, t, names=names)
    return G, nodes
