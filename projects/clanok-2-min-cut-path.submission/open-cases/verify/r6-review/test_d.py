"""Proposition D (r5-core §2.2) and Proposition CF (§3.3) on the rebuilt families.

usage: python test_d.py KMAX [hyb]
  for k = 2..KMAX, Y_k, Y'_k, Y^d_k, Y'^d_k (both variants): P2, solutions (brute force), pruning, CF centres;
  with 'hyb': HYB plain / refined with several parameter sets (expensive).
"""
import json
import sys
import time

from glib import p2_violations, brute, prune, e_desc, NE, connects, bits, hyb, cdesc, shortest_len
from fam import yfam, xfam


def show(D, G):
    return sorted(bits(D))


def main():
    kmax = int(sys.argv[1])
    dohyb = len(sys.argv) > 2 and sys.argv[2] == "hyb"
    out = []
    for k in range(2, kmax + 1):
        for contact in (False, True):
            for dvar in (None, "plain", "back"):
                G, info = yfam(k, contact, dvar)
                name = ("Y'" if contact else "Y") + ("^d" if dvar else "") + ("(back)" if dvar == "back" else "") + "_%d" % k
                rec = {"name": name, "m": G.m, "N": G.N}
                rec["p2_viol"] = p2_violations(G)
                sols = brute(G)
                rec["nsol"] = len(sols)
                x, mt = info["x"], info["m"]
                expect = sum(1 << x(j) for j in range(k + 1, 2 * k + 1))
                exp_sols = {expect} | ({expect | (1 << info["d"])} if dvar else set())
                rec["sols_as_claimed"] = set(sols) == exp_sols
                fixed, dead = prune(G)
                rec["pruned_fixed"] = None if dead is None else sorted(fixed.items())
                # CF (i), (ii): centre Fl_2k, no flip
                Fl2k = G.mask(info["Fl"](2 * k))
                U = NE(G, Fl2k)
                D = e_desc(G, U, 0)
                rec["CF_D"] = sorted(bits(D))
                rec["CF_ok"] = (D in exp_sols) and connects(G, D)
                rec["shortest"] = shortest_len(G)
                if dohyb and k >= 3:
                    for params in ((1, 0, 1, 3), (1, 1, 1, 3), (2, 0, 1, 3), (1, 0, 2, 3), (1, 1, 2, 6)):
                        if params[0] + params[1] + params[2] >= k and params[3] >= k and params != (1, 1, 2, 6):
                            continue
                        t0 = time.time()
                        rec["hyb%s" % (params,)] = hyb(G, *params)
                        rec["hyb%s_time" % (params,)] = round(time.time() - t0, 1)
                    if contact or True:
                        t0 = time.time()
                        rec["hyb_refined(1,0,1,3)"] = hyb(G, 1, 0, 1, 3, refined=True)
                        rec["hyb_refined_time"] = round(time.time() - t0, 1)
                print(json.dumps(rec), flush=True)
                out.append(rec)
    for L in range(2, 9):
        G, info = xfam(L)
        rec = {"name": "X_%d" % L, "m": G.m, "p2_viol": p2_violations(G)}
        sols = brute(G)
        rec["nsol"] = len(sols)
        x, mt = info["x"], info["m"]
        U = NE(G, G.E[mt(1)])
        Phi = (1 << x(L)) if L % 2 == 1 else 0
        D = e_desc(G, U, Phi)
        rec["CF_D"] = sorted(bits(D))
        rec["CF_ok"] = len(sols) == 1 and D == sols[0]
        rec["CF_noflip_ok"] = len(sols) == 1 and e_desc(G, U, 0) == sols[0]
        print(json.dumps(rec), flush=True)
        out.append(rec)
    with open("runs/d-%d%s.json" % (kmax, "-hyb" if dohyb else ""), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
