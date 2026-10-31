"""Families for dc-general.md: the rigid family R_L of dc-hardness.md (Helly form: t in every flip side) and its
extensions by mates (ties or one-way comparabilities), as general ZZ instances (gcert.Inst).

Switch model with members: nodes 0..N-1, s, t; members w with node sets E[w], F[w]; a preorder `mle` on the members
(mle[w][w2] = w <= w2).  ZZ form: one bottom b_x for every node in some E-set or equal to s (b_s = u), one top t_x
for every node in some F-set or equal to t (t_t = v), fixed edges b_x t_x; bottoms form the class of u, tops the class
of v; member w has R-edges to the bottoms of E[w] and to the tops of F[w]; members ordered by mle.

R_L: switches x_1..x_L; path side h_k = E for odd k, F for even k; flip side Fl_k = the other one.  Nodes s in h_1,
t in h_L, yy_k in h_k and h_{k+1}; for p < q: z_pq in Fl_p and h_q (q - p odd), w_pq in Fl_p and Fl_q (q - p even);
Helly form: t in every Fl_k.
Mates (one per switch, the class C_k = {x_k, m_k} or the order m_k < x_k (k even), m_k > x_k (k odd)):
  k even: E[m_k] = {p_k}, F[m_k] = {omF};  k odd: E[m_k] = {omE} + {p_j : j even}, F[m_k] = {q_k};
  p_k in Fl_j (j even, j != k), omF in Fl_j (j odd), q_k in Fl_i (i odd, i != k), omE in Fl_i (i even).
"""
import gcert


def to_inst(N, E, F, mle, s, t):
    nm = len(E)
    inE = set()
    inF = set()
    for w in range(nm):
        inE |= set(E[w])
        inF |= set(F[w])
    inE.add(s)
    inF.add(t)
    names = []
    bot = {}
    bot[s] = 0
    names.append(("b", s))
    for x in range(N):
        if x in inE and x != s:
            bot[x] = len(names)
            names.append(("b", x))
    mem0 = len(names)
    for w in range(nm):
        names.append(("m", w))
    top = {}
    for x in range(N):
        if x in inF and x != t:
            top[x] = len(names)
            names.append(("t", x))
    top[t] = len(names)
    names.append(("t", t))
    n = len(names)
    Bset = set(bot.values())
    Tset = set(top.values())
    le = [[False] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if a == b or a in Bset or b in Tset:
                le[a][b] = True
    for w in range(nm):
        for w2 in range(nm):
            if mle[w][w2]:
                le[mem0 + w][mem0 + w2] = True
    R = set()
    for x in range(N):
        if x in bot and x in top:
            R.add((bot[x], top[x]))
    for w in range(nm):
        for x in E[w]:
            R.add((bot[x], mem0 + w))
        for x in F[w]:
            R.add((mem0 + w, top[x]))
    R.discard((0, n - 1))
    return gcert.Inst(n, le, R, 0, n - 1), names


def rigid(L, mates=None, helly=True):
    """mates: None, 'tie' or 'oneway'.  Returns (Inst, names, info)."""
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
        yk = node(("y", k))
        h(k).add(yk)
        h(k + 1).add(yk)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
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
    Em = [sorted(E[k]) for k in range(1, L + 1)]
    Fm = [sorted(F[k]) for k in range(1, L + 1)]
    nm = L
    if mates:
        mE = {}
        mF = {}
        omE, omF = node("omE"), node("omF")
        for k in range(1, L + 1):
            if k % 2 == 0:
                pk = node(("p", k))
                mE[k] = {pk}
                mF[k] = {omF}
            else:
                qk = node(("q", k))
                mF[k] = {qk}
                mE[k] = {omE}
        for k in range(1, L + 1):
            if k % 2 == 1:
                mE[k] |= {nodes[("p", j)] for j in range(2, L + 1, 2)}
        for k in range(1, L + 1):
            if k % 2 == 0:
                for j in range(2, L + 1, 2):
                    if j != k:
                        Em[j - 1].append(nodes[("p", k)])
            else:
                for i in range(1, L + 1, 2):
                    if i != k:
                        Fm[i - 1].append(nodes[("q", k)])
        for j in range(1, L + 1):
            if j % 2 == 1:
                Fm[j - 1].append(omF)
            else:
                Em[j - 1].append(omE)
        for k in range(1, L + 1):
            Em.append(sorted(mE[k]))
            Fm.append(sorted(mF[k]))
        nm = 2 * L
    Em = [sorted(set(e)) for e in Em]
    Fm = [sorted(set(f)) for f in Fm]
    mle = [[w == w2 for w2 in range(nm)] for w in range(nm)]
    if mates == "tie":
        for k in range(L):
            mle[k][L + k] = mle[L + k][k] = True
    elif mates == "oneway":
        for k in range(L):
            if (k + 1) % 2 == 0:
                mle[L + k][k] = True     # m_k < x_k
            else:
                mle[k][L + k] = True     # x_k < m_k
    I, names = to_inst(len(nodes), Em, Fm, mle, s, t)
    return I, names, {"nodes": nodes, "E": Em, "F": Fm}


def solutions_2ch(N, E, F, cls, s, t):
    """All class-mode vectors (dict class -> 0 E / 1 F) connecting s and t (brute force)."""
    K = sorted(set(cls))
    out = []
    for mask in range(1 << len(K)):
        mode = {c: (mask >> i) & 1 for i, c in enumerate(K)}
        hyper = [set(F[w]) if mode[cls[w]] else set(E[w]) for w in range(len(E))]
        comp = {s}
        changed = True
        while changed:
            changed = False
            for hh in hyper:
                if hh & comp and not hh <= comp:
                    comp |= hh
                    changed = True
        if t in comp:
            out.append(mode)
    return out


def span(a, b):
    return list(range(a, b + 1)) if a is not None else []


def tic_rigid(L, mates=None, R=None):
    """Interval (TIC) form of R_L extended by a region Y = [L, L+R] and mates.
    Line 0..K, K = L + R (R = L + 1 by default), s = 0, t = K.  Switch x_k (k = 1..L): h_k = [k-1, k] (E for odd k,
    F for even k), Fl_k = [k, K] (the other type).  Switch Z: E = F = [L, K] (covers Y in either mode).
    Mates (classes C_k = {x_k, m_k}, or m_k < x_k for even k and m_k > x_k for odd k):
      k even: E[m_k] = {L + k} (a point), F[m_k] = {K};  k odd: E[m_k] = [L, K], F[m_k] = {L + k}.
    Every side is an interval of junctions, so same-type sides are Helly."""
    if R is None:
        R = L + 1
    K = L + R
    E, F = [], []
    for k in range(1, L + 1):
        h = (k - 1, k)
        fl = (k, K)
        if k % 2 == 1:
            E.append(span(*h)); F.append(span(*fl))
        else:
            F.append(span(*h)); E.append(span(*fl))
    E.append(span(L, K)); F.append(span(L, K))          # Z, index L
    nm = L + 1
    if mates:
        for k in range(1, L + 1):
            if k % 2 == 0:
                E.append([L + k]); F.append([K])
            else:
                E.append(span(L, K)); F.append([L + k])
        nm = 2 * L + 1
    mle = [[w == w2 for w2 in range(nm)] for w in range(nm)]
    if mates == "tie":
        for k in range(L):
            mle[k][L + 1 + k] = mle[L + 1 + k][k] = True
    elif mates == "oneway":
        for k in range(L):
            if (k + 1) % 2 == 0:
                mle[L + 1 + k][k] = True
            else:
                mle[k][L + 1 + k] = True
    I, names = to_inst(K + 1, E, F, mle, 0, K)
    return I, names, {"E": E, "F": F, "K": K}
