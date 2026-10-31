"""Rigid word family R(W) in 2CH form and the family Y_k (r4-general.md §6): R(E^k F^k) plus one one-way mate
above every E-member, with sides that make the mate an irrelevant but unavoidable conflict partner.

R(W), W a word over {E, F} of length L: switches x_1..x_L; path side h_k of type W_k, flip side Fl_k of the other
type; nodes s in h_1, t in h_L, y_k in h_k and h_{k+1}; for p < q: z_pq in Fl_p and h_q if W_p != W_q (same type),
w_pq in Fl_p and Fl_q if W_p == W_q.
Mates (Y_k = R(E^k F^k) + mates): for every E-member c (1 <= c <= k) a switch m_c > x_c with
  F(m_c) = {f_cb : b E-member, b != c}, f_cb added to Fl_b (= F(x_b));
  E(m_c) = {e_cq : q F-member} + {g_cc' : c' != c}, e_cq added to Fl_q (= E(x_q)), g_cc' = g_c'c shared with m_c'.
Options: helly=True adds t to every flip side (then the w-nodes are kept as well); contact=True (family Y'_k) adds
a private node of F(m_c) to the path side h_{k+c} of the c-th F-member.
"""
import families


def rword(W, mates=False, helly=False, mate_set=None, contact=False):
    L = len(W)
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    s, t = node("s"), node("t")
    E = {k: set() for k in range(1, L + 1)}
    F = {k: set() for k in range(1, L + 1)}

    def h(k):
        return E[k] if W[k - 1] == "E" else F[k]

    def fl(k):
        return F[k] if W[k - 1] == "E" else E[k]

    h(1).add(s)
    h(L).add(t)
    for k in range(1, L):
        y = node(("y", k))
        h(k).add(y)
        h(k + 1).add(y)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if W[p - 1] != W[q - 1]:
                z = node(("z", p, q))
                fl(p).add(z)
                h(q).add(z)
            else:
                w = node(("w", p, q))
                fl(p).add(w)
                fl(q).add(w)
    if helly:
        for k in range(1, L + 1):
            fl(k).add(t)
    swE = [E[k] for k in range(1, L + 1)]
    swF = [F[k] for k in range(1, L + 1)]
    names = [("x", k) for k in range(1, L + 1)]
    rel = []
    if mates:
        Em = [k for k in range(1, L + 1) if W[k - 1] == "E"]
        Fm = [k for k in range(1, L + 1) if W[k - 1] == "F"]
        cs = Em if mate_set is None else [c for c in Em if c in mate_set]
        for c in cs:
            me, mf = set(), set()
            for b in Em:
                if b != c:
                    x = node(("f", c, b))
                    mf.add(x)
                    F[b].add(x)
            if contact:
                # Y'_k: a private contact node of F(m_c) with the path side of the c-th F-member
                qc = Fm[cs.index(c) % len(Fm)]
                x = node(("fc", c, qc))
                mf.add(x)
                h(qc).add(x)
            for q in Fm:
                x = node(("e", c, q))
                me.add(x)
                E[q].add(x)
            for c2 in cs:
                if c2 != c:
                    me.add(node(("g",) + tuple(sorted((c, c2)))))
            swE.append(me)
            swF.append(mf)
            names.append(("m", c))
            rel.append((len(names) - 1, c - 1))     # m_c > x_c: x_c <= m_c
    nm = len(names)
    Elist = [sorted(e) for e in swE]
    Flist = [sorted(f) for f in swF]
    mle = [[a == b for b in range(nm)] for a in range(nm)]
    for mi, xi in rel:
        mle[xi][mi] = True
    I, enames = families.to_inst(len(nodes), Elist, Flist, mle, s, t)
    full = []
    for e in enames:
        if e[0] == "m":
            full.append(names[e[1]])
        else:
            nn = [k for k, v in nodes.items() if v == e[1]][0]
            full.append((e[0], nn))
    return I, full, {"E": Elist, "F": Flist, "mle": mle, "nodes": nodes, "s": s, "t": t, "swnames": names}


def yfam(k, helly=False, contact=False):
    return rword("E" * k + "F" * k, mates=True, helly=helly, contact=contact)
