"""Two-route family Z_k (r4-general.md §7): two copies R^0, R^1 of the rigid chain R(E^k F^k) between the same
terminals s, t, P2 between the routes by dead-end connectors, and one one-way mate above every E-member of both
routes.  Propagation fixes nothing (each route can be broken while the other is used), so every mate's F-side is
used by some solution, and the mates cannot be pruned.
block=True (family Z^B_k): every F-member of one route is put below the last F-member of the other route, so the
F-members never flip and their flip sides (the hubs of the counting obstruction) are never picked.

Route r (r = 0, 1): switches x^r_1..x^r_2k, path side h^r_j (E for j <= k, F for j > k), flip side Fl^r_j; nodes
s in h^r_1, t in h^r_2k, y^r_j, z^r_pq (Fl_p and h_q, p E-member, q F-member), w^r_pq (Fl_p and Fl_q, equal modes).
Cross P2 (route 0 switch a, route 1 switch b):
  equal modes: a node in Fl^0_a and Fl^1_b;
  a E-member, b F-member: a node in h^0_a (E) and Fl^1_b (E; flip sides of F-members are dead ends);
  a F-member, b E-member: a node in Fl^0_a (E) and h^1_b (E).
Mates m^r_c > x^r_c (c <= k):
  F(m^r_c) = f-nodes in Fl^{r'}_b for every E-member b of either route other than x^r_c itself
             + (contact=True) a private node in the path side h^{1-r}_{k+c} of the other route;
  E(m^r_c) = e-nodes in Fl^{r'}_q for every F-member q of either route + g-nodes shared with every other mate.
"""
import families


def zfam(k, contact=True, mates=True, block=False):
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    s, t = node("s"), node("t")
    sw = {}          # (r, j) -> [E set, F set]
    for r in (0, 1):
        for j in range(1, 2 * k + 1):
            sw[(r, j)] = [set(), set()]

    def mode(j):
        return "E" if j <= k else "F"

    def h(r, j):
        return sw[(r, j)][0] if mode(j) == "E" else sw[(r, j)][1]

    def fl(r, j):
        return sw[(r, j)][1] if mode(j) == "E" else sw[(r, j)][0]

    for r in (0, 1):
        h(r, 1).add(s)
        h(r, 2 * k).add(t)
        for j in range(1, 2 * k):
            y = node(("y", r, j))
            h(r, j).add(y)
            h(r, j + 1).add(y)
        for p in range(1, 2 * k + 1):
            for q in range(p + 1, 2 * k + 1):
                if mode(p) != mode(q):
                    z = node(("z", r, p, q))
                    fl(r, p).add(z)
                    h(r, q).add(z)
                else:
                    w = node(("w", r, p, q))
                    fl(r, p).add(w)
                    fl(r, q).add(w)
    for a in range(1, 2 * k + 1):
        for b in range(1, 2 * k + 1):
            c = node(("x", a, b))
            if mode(a) == mode(b):
                fl(0, a).add(c)
                fl(1, b).add(c)
            elif mode(a) == "E":
                h(0, a).add(c)
                fl(1, b).add(c)
            else:
                fl(0, a).add(c)
                h(1, b).add(c)
    keys = [(r, j) for r in (0, 1) for j in range(1, 2 * k + 1)]
    Elist = [sw[key][0] for key in keys]
    Flist = [sw[key][1] for key in keys]
    names = [("x", r, j) for r, j in keys]
    rel = []
    if mates:
        mlist = [(r, c) for r in (0, 1) for c in range(1, k + 1)]
        for (r, c) in mlist:
            me, mf = set(), set()
            for r2 in (0, 1):
                for b in range(1, k + 1):
                    if (r2, b) != (r, c):
                        x = node(("f", r, c, r2, b))
                        mf.add(x)
                        fl(r2, b).add(x)
                for q in range(k + 1, 2 * k + 1):
                    x = node(("e", r, c, r2, q))
                    me.add(x)
                    fl(r2, q).add(x)
            for other in mlist:
                if other != (r, c):
                    me.add(node(("g",) + tuple(sorted([(r, c), other]))))
            if contact:
                x = node(("fc", r, c))
                mf.add(x)
                h(1 - r, k + c).add(x)
            Elist.append(me)
            Flist.append(mf)
            names.append(("m", r, c))
            rel.append((len(names) - 1, keys.index((r, c))))
    nm = len(names)
    mle = [[a == b for b in range(nm)] for a in range(nm)]
    for mi, xi in rel:
        mle[xi][mi] = True
    if block:
        # block the hubs: every F-member of one route lies below the last F-member of the other route (this ties the
        # two last F-members and puts all F-members below that class)
        for r in (0, 1):
            top = keys.index((1 - r, 2 * k))
            for q in range(k + 1, 2 * k + 1):
                mle[keys.index((r, q))][top] = True
        for a in range(nm):
            mle[a][a] = True
        for c in range(nm):
            for a in range(nm):
                if mle[a][c]:
                    for b in range(nm):
                        if mle[c][b]:
                            mle[a][b] = True
    El = [sorted(e) for e in Elist]
    Fl = [sorted(f) for f in Flist]
    I, enames = families.to_inst(len(nodes), El, Fl, mle, s, t)
    full = []
    for e in enames:
        if e[0] == "m":
            full.append(names[e[1]])
        else:
            nn = [kk for kk, v in nodes.items() if v == e[1]][0]
            full.append((e[0], nn))
    return I, full, {"E": El, "F": Fl, "mle": mle, "nodes": nodes, "s": s, "t": t, "swnames": names}
