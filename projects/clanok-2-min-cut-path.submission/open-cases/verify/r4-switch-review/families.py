"""Rigid family R_L of dc-hardness.md and its variants, built from the definition there:
switches x_1..x_L; h_k is E for odd k, F for even k, Fl_k is the other set; s in h_1, t in h_L,
y_k in h_k ∩ h_{k+1}; for p < q: z_pq in Fl_p ∩ h_q if q - p is odd, w_pq in Fl_p ∩ Fl_q if q - p is even.
Variants: helly (t added to every Fl_k), cut(k) (y_k removed), tflip(k) (t moved from h_L into Fl_k).

usage: python families.py Lmax [decide_Lmax]
"""
import sys
import json
from core import Inst, p2, brute_force, shortest_valid_paths, search5
from proof import check_path, ClaimFailure
from alg import decide


def rigid(L, helly=False, cut=None, tflip=None):
    N = [2]

    def new():
        N[0] += 1
        return N[0] - 1
    h = {k: set() for k in range(1, L + 1)}
    fl = {k: set() for k in range(1, L + 1)}
    h[1].add(0)
    h[L].add(1)
    for k in range(1, L):
        if cut == k:
            continue
        y = new()
        h[k].add(y)
        h[k + 1].add(y)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            x = new()
            if (q - p) % 2 == 1:
                fl[p].add(x)
                h[q].add(x)
            else:
                fl[p].add(x)
                fl[q].add(x)
    if helly:
        for k in range(1, L + 1):
            fl[k].add(1)
    if tflip is not None:
        h[L].discard(1)
        fl[tflip].add(1)
    sw = []
    for k in range(1, L + 1):
        sw.append((h[k], fl[k]) if k % 2 == 1 else (fl[k], h[k]))
    return Inst(N[0], 0, 1, sw)


def main():
    Lmax = int(sys.argv[1])
    dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    out = {"inst": 0, "yes": 0, "no": 0, "paths": 0, "fail": 0, "decide_runs": 0}
    stats = {}
    for L in range(2, Lmax + 1):
        variants = [("R", rigid(L)), ("helly", rigid(L, helly=True))]
        variants += [("cut%d" % k, rigid(L, cut=k)) for k in range(1, L)]
        variants += [("tflip%d" % k, rigid(L, tflip=k)) for k in range(1, L + 1)]
        for name, inst in variants:
            out["inst"] += 1
            if not p2(inst):
                out["fail"] += 1
                print("P2 fails", L, name)
            bf = brute_force(inst) if L <= 14 else None
            Lp, paths = shortest_valid_paths(inst, limit=50)
            if bf is not None and (Lp is not None) != bf:
                out["fail"] += 1
                print("solver mismatch", L, name)
            if Lp is None:
                out["no"] += 1
                if L <= dmax:
                    out["decide_runs"] += 1
                    if decide(inst, 1, 1, 8):
                        out["fail"] += 1
                        print("decide(1,1,8) accepted no-instance", L, name)
                if search5(inst, set(range(inst.D)), inst.D) is not None:
                    out["fail"] += 1
                    print("full search accepted no-instance", L, name)
                continue
            out["yes"] += 1
            prm = None
            for P in paths:
                out["paths"] += 1
                try:
                    o = check_path(inst, P, stats)
                    c9 = o["cor9"]
                    prm = (1, 2, c9[1]) if c9[0] == "swap" else (max(c9[2], c9[4]), max(c9[3], c9[5]), c9[1])
                    if name == "R":
                        print("R_%d path len %d certificate %s" % (L, len(P), json.dumps(o["cor9"])))
                except ClaimFailure as e:
                    out["fail"] += 1
                    print("FAIL", L, name, e.args[0])
            if L <= dmax and name in ("R", "helly"):
                out["decide_runs"] += 1
                if not decide(inst, *prm):
                    out["fail"] += 1
                    print("decide at proof parameters rejected", L, name, prm)
    print(json.dumps(out))
    print(json.dumps(stats, sort_keys=True))


if __name__ == "__main__":
    main()
