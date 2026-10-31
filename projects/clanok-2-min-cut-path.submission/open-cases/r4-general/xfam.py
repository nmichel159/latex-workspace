"""Family X_L (r4-general.md, Section 4): the rigid family R_L in Helly form *without* the w-nodes, plus one
one-way mate per switch whose sides make it junk for every pin of Theorem NG and need a private piercer in Theorem GC.

Switch model with an order on the members (dc-general/families.to_inst: bottoms ~ u, tops ~ v, fixed edges b_x t_x).
Base switches x_1..x_L: path side h_k (E for odd k, F for even k), flip side Fl_k (the other type);
  s in h_1, t in h_L, y_k in h_k and h_{k+1}, z_pq in Fl_p and h_q (p < q, q - p odd), t in every Fl_k.
Even mates m_k < x_k:  E(m_k) = {n_k, n'_k} + {n_kj : j even, j != k} + {c_ik : i odd},  F(m_k) = {t};
  n_k, n'_k are added to h_k = F(x_k); n_kj is added to Fl_j = E(x_j).
Odd mates  m_k > x_k:  E(m_k) = {t} + {c_kj : j even},  F(m_k) = {e_k, e'_k} + {n'_kj : j odd, j != k};
  e_k, e'_k are added to h_k = E(x_k); n'_kj is added to Fl_j = F(x_j).
Variants: mates in {None, 'even', 'odd', 'both'}; w=True keeps the w-nodes of R_L (w_pq in Fl_p and Fl_q, q - p even).
"""
import families


def xfam(L, mates="both", w=False):
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    s, t = node("s"), node("t")
    E = {k: set() for k in range(1, L + 1)}
    F = {k: set() for k in range(1, L + 1)}

    def h(k):
        return E[k] if k % 2 == 1 else F[k]

    def fl(k):
        return F[k] if k % 2 == 1 else E[k]

    h(1).add(s)
    h(L).add(t)
    for k in range(1, L):
        y = node(("y", k))
        h(k).add(y)
        h(k + 1).add(y)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                z = node(("z", p, q))
                fl(p).add(z)
                h(q).add(z)
            elif w:
                ww = node(("w", p, q))
                fl(p).add(ww)
                fl(q).add(ww)
    for k in range(1, L + 1):
        fl(k).add(t)
    swE = [None] + [E[k] for k in range(1, L + 1)]
    swF = [None] + [F[k] for k in range(1, L + 1)]
    names = [None] + [("x", k) for k in range(1, L + 1)]
    rel = []          # (a, b): switch a < switch b (indices into the final list)
    even = [k for k in range(2, L + 1, 2)]
    odd = [k for k in range(1, L + 1, 2)]
    use_even = mates in ("even", "both")
    use_odd = mates in ("odd", "both")
    if use_even:
        for k in even:
            me, mf = set(), {t}
            for nm in (("n", k), ("n'", k)):
                x = node(nm)
                me.add(x)
                F[k].add(x)
            for j in even:
                if j != k:
                    x = node(("nkj", k, j))
                    me.add(x)
                    E[j].add(x)
            if use_odd:
                for i in odd:
                    me.add(node(("c", i, k)))
            swE.append(me)
            swF.append(mf)
            names.append(("m", k))
            rel.append((len(names) - 1, k))
    if use_odd:
        for k in odd:
            me, mf = {t}, set()
            if use_even:
                for j in even:
                    me.add(node(("c", k, j)))
            for nm in (("e", k), ("e'", k)):
                x = node(nm)
                mf.add(x)
                E[k].add(x)
            for j in odd:
                if j != k:
                    x = node(("n'kj", k, j))
                    mf.add(x)
                    F[j].add(x)
            swE.append(me)
            swF.append(mf)
            names.append(("m", k))
            rel.append((k, len(names) - 1))
    nm = len(names) - 1
    Elist = [sorted(swE[i]) for i in range(1, nm + 1)]
    Flist = [sorted(swF[i]) for i in range(1, nm + 1)]
    mle = [[a == b for b in range(nm)] for a in range(nm)]
    for a, b in rel:
        mle[a - 1][b - 1] = True
    I, enames = families.to_inst(len(nodes), Elist, Flist, mle, s, t)
    swnames = names[1:]
    full = []
    for e in enames:
        if e[0] == "m":
            full.append(swnames[e[1]])
        else:
            nn = [k for k, v in nodes.items() if v == e[1]][0]
            full.append((e[0], nn))
    return I, full, {"E": Elist, "F": Flist, "mle": mle, "nodes": nodes, "s": s, "t": t, "swnames": swnames}


def brute(info):
    """All mode vectors (dict switch -> 'E'/'F') consistent with the order (a < b: b in F implies a in F) that connect
    s and t.  Exponential in the number of switches."""
    E, F, mle, s, t = info["E"], info["F"], info["mle"], info["s"], info["t"]
    m = len(E)
    out = []
    for mask in range(1 << m):
        inD = [(mask >> i) & 1 for i in range(m)]
        ok = True
        for a in range(m):
            for b in range(m):
                if a != b and mle[a][b] and inD[b] and not inD[a]:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        hyper = [set(F[i]) if inD[i] else set(E[i]) for i in range(m)]
        comp = {s}
        ch = True
        while ch:
            ch = False
            for hh in hyper:
                if hh & comp and not hh <= comp:
                    comp |= hh
                    ch = True
        if t in comp:
            out.append(mask)
    return out
