"""Re-check of the completion obstruction of dc-hardness.md Section 3 (agent verify-LTH).

The SW encoding of a formula is taken from dc-algorithm/sw_sat.encode (imported read-only, only to build the
instance). Everything else is own code: the SW instance [nb, nt, F, Nb, Nt] (u = bottom 0, v = top 0, F = fixed
bottom-top edges) is contracted to 2CH (nodes = components of the fixed edges; E_w = components of Nb(w),
F_w = components of Nt(w)), and answers are computed by the own brute force. For every pair of switches without a
common bottom or top, every single addition (shared existing bottom, shared existing top, new private bottom, new
private top) is tried. Usage: python check_p2options.py all4 x-notx"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from core import brute_2ch, p2_2ch

sys.path.insert(1, os.path.join(HERE, "..", "..", "dc-algorithm"))
import sw_sat  # noqa: E402  (read-only: only encode and FORMULAS are used)


def sw_to_2ch(nb, nt, F, Nb, Nt):
    parent = list(range(nb + nt))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (b, t) in F:
        parent[find(b)] = find(nb + t)
    roots = sorted(set(find(x) for x in range(nb + nt)))
    cid = {r: i for i, r in enumerate(roots)}
    comp = lambda x: cid[find(x)]
    sw = []
    for w in range(len(Nb)):
        E = 0
        for b in Nb[w]:
            E |= 1 << comp(b)
        Fm = 0
        for t in Nt[w]:
            Fm |= 1 << comp(nb + t)
        sw.append((E, Fm))
    return (len(roots), comp(0), comp(nb + 0), sw)


def answer(inst_sw):
    return brute_2ch(sw_to_2ch(*inst_sw))[0]


if __name__ == "__main__":
    for name in sys.argv[1:]:
        nv, cls = sw_sat.FORMULAS[name]
        inst, label = sw_sat.encode(nv, cls)
        nb, nt, F, Nb, Nt = inst
        print("formula", name, cls, "switches", len(Nb), "own answer", answer(inst),
              "satisfiable", sw_sat.satisfiable(nv, cls), "P2", p2_2ch(sw_to_2ch(*inst)))
        k = len(Nb)
        nopt = 0
        for a in range(k):
            for b in range(a + 1, k):
                if set(Nb[a]) & set(Nb[b]) or set(Nt[a]) & set(Nt[b]):
                    continue
                good = []
                for kind, x in [("b", x) for x in range(nb)] + [("t", t) for t in range(nt)] + [("nb", None), ("nt", None)]:
                    nb2, nt2 = nb, nt
                    Nb2, Nt2 = [set(y) for y in Nb], [set(y) for y in Nt]
                    if kind == "b":
                        Nb2[a].add(x); Nb2[b].add(x)
                    elif kind == "t":
                        Nt2[a].add(x); Nt2[b].add(x)
                    elif kind == "nb":
                        Nb2[a].add(nb); Nb2[b].add(nb); nb2 += 1
                    else:
                        Nt2[a].add(nt); Nt2[b].add(nt); nt2 += 1
                    if not answer((nb2, nt2, F, Nb2, Nt2)):
                        good.append((kind, x))
                nopt += not good
                print("  pair", a, label[a], b, label[b], "single additions keeping 'no':", good)
        print("  pairs with no option:", nopt)
