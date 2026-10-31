"""Hub family H(m, m') of dc-algorithm.md Section 6.1, rebuilt from the text only (agent verify-round3).

version 'classes': bottoms equivalent to u, tops equivalent to v.
version 'po'     : partial order, u least, v greatest, other bottoms pairwise incomparable, other tops pairwise
                   incomparable; extra real edges u b (bottoms b != u) and t v (tops t != v).
order of gadgets: list of pairs (i, j); default lexicographic.
"""
import itertools

from r3core import Inst, preorder_from_relations


def hub(m, mp, version='classes', order=None, drop_edges=()):
    if order is None:
        order = [(i, j) for i in range(m) for j in range(mp)]
    K = len(order)
    names = []
    idx = {}

    def add(nm):
        idx[nm] = len(names)
        names.append(nm)
        return idx[nm]

    bs = add('b_s')            # = u
    ba = add('b_a')
    bb = add('b_beta')
    bt = add('b_t')
    tops = [add('t_n%d' % p) for p in range(K + 1)]   # t_{n_0} .. t_{n_K} = t_a
    tt = add('t_t')            # = v
    eps = [add('eps%d' % i) for i in range(m)]
    xi = [add('xi%d' % j) for j in range(mp)]
    rA = {}
    rB = {}
    for (i, j) in order:
        rA[(i, j)] = add('rA%d%d' % (i, j))
        rB[(i, j)] = add('rB%d%d' % (i, j))
    q = len(names)
    u, v = bs, tt
    bottoms = [bs, ba, bb, bt]
    topsall = tops + [tt]
    middle = eps + xi + list(rA.values()) + list(rB.values())
    rel = []
    for b in bottoms:
        for x in middle + topsall:
            rel.append((b, x))
    for x in middle:
        for t in topsall:
            rel.append((x, t))
    for (i, j) in order:
        rel.append((eps[i], rA[(i, j)]))
        rel.append((xi[j], rB[(i, j)]))
    if version == 'classes':
        classes = [bottoms, topsall]
    else:
        for b in bottoms:
            if b != u:
                rel.append((u, b))
        for t in topsall:
            if t != v:
                rel.append((t, v))
        classes = None
    le = preorder_from_relations(q, rel, classes)
    R = [(bs, tops[0]), (ba, tops[K]), (bt, tt)]
    for p, (i, j) in enumerate(order, start=1):
        for rho in (rA[(i, j)], rB[(i, j)]):
            R += [(bb, rho), (rho, tops[p - 1]), (rho, tops[p])]
    for i in range(m):
        R += [(ba, eps[i]), (bb, eps[i])]
    for j in range(mp):
        R += [(bb, xi[j]), (bt, xi[j])]
    if version != 'classes':
        for b in bottoms:
            if b != u:
                R.append((u, b))
        for t in topsall:
            if t != v:
                R.append((t, v))
    R = [e for e in R if e not in set(drop_edges)]
    return Inst(q, le, R, u, v, names=names)


if __name__ == "__main__":
    for ver in ('classes', 'po'):
        H = hub(2, 2, ver)
        H.check()
        print(ver, 'q', H.q, '|R|', len(H.R), 'P2', H.p2())
