"""The structural facts used in the proof of Proposition D (iv) (r5-core §2.2), on the rebuilt Y^d_k, Y'^d_k.

(a) Pi(h_c) = {Fl_c, F(m_c)} for c <= k;
(b) the sides whose conflict family contains F(m_c) are exactly h_c and E(m_c);
(c) the sides meeting F(m_c) are F(m_c), Fl_b (b != c) and, in Y'^d_k, h_{k+c};
(d) N_F[Fl_b] contains every h_q, q > k;
(e) N_F[F(m_c)] and N_F[h_{k+c}] contain F(m_c') only for c' = c;
(f) for each of the two solutions, every s-t walk in the picked side graph passes every h_c (c <= k): removing h_c
    from the picked sides disconnects s from t.
usage: python test_d_iv.py KMAX
"""
import json
import sys

from glib import brute, comp_from, picked_masks
from fam import yfam


def main():
    kmax = int(sys.argv[1])
    allok = True
    for k in range(2, kmax + 1):
        for contact in (False, True):
            for dvar in ("plain", "back"):
                G, info = yfam(k, contact, dvar)
                h, Fl, mt = info["h"], info["Fl"], info["m"]
                Fm = lambda c: 2 * mt(c) + 1
                Em = lambda c: 2 * mt(c)
                res = {}
                res["a"] = all(G.Pi[h(c)] == frozenset({Fl(c), Fm(c)}) for c in range(1, k + 1))
                res["b"] = all({i for i in G.sides if Fm(c) in G.Pi[i]} == {h(c), Em(c)} for c in range(1, k + 1))
                okc = True
                for c in range(1, k + 1):
                    meet = {i for i in G.sides if G.mask(i) & G.mask(Fm(c))}
                    exp = {Fm(c)} | {Fl(b) for b in range(1, k + 1) if b != c} | ({h(k + c)} if contact else set())
                    okc &= meet == exp
                res["c"] = okc
                Fsides = lambda Z: {i for i in G.sides if (i & 1) == 1 and G.mask(i) & G.mask(Z)}
                res["d"] = all({h(q) for q in range(k + 1, 2 * k + 1)} <= Fsides(Fl(b)) for b in range(1, k + 1))
                oke = True
                for c in range(1, k + 1):
                    for Z in [Fm(c)] + ([h(k + c)] if contact else []):
                        got = {cc for cc in range(1, k + 1) if Fm(cc) in Fsides(Z)}
                        oke &= got == {c}
                res["e"] = oke
                okf = True
                for D in brute(G):
                    pm = picked_masks(G, D)
                    for c in range(1, k + 1):
                        x = info["x"](c)
                        pm2 = list(pm)
                        pm2[x] = 0          # remove the picked side of x_c, which is h_c
                        if (comp_from(G, G.s, pm2) >> G.t) & 1:
                            okf = False
                res["f"] = okf
                name = ("Y'" if contact else "Y") + "^d" + ("(back)" if dvar == "back" else "") + "_%d" % k
                print(name, json.dumps(res))
                allok &= all(res.values())
    print("ALL OK" if allok else "SOME FAILED")


if __name__ == "__main__":
    main()
