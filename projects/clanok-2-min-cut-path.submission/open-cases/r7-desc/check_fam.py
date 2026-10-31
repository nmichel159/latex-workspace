"""r7-desc: Theorem B and Lemmas J, G on the known families: Y_k, Y'_k, Y^d_k, Y'^d_k, X_L, Z_k, Z^B_k, W_n, OB, BP_n,
all shortest valid paths (at most 40 per instance), true thresholds.

  python check_fam.py KMAX LMAX BPMAX

Generators of r4-general/, r5-core/, r5-hard/ are imported read-only and only build the instances; the checks run on
the conversion to the reviewed library verify/rv-r6-core/zzl.py.
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
sys.path.append(HERE)
for d in ("r5-core", "r4-general", "r5-hard"):
    sys.path.append(os.path.join(OC, d))
from check_b import run_path, shortest_len  # noqa: E402
from zzl import SW, Budget, all_shortest_valid_paths  # noqa: E402
from gcore import from_inst  # noqa: E402


def to_sw(G):
    me = [(int(y), int(x), int(p)) for p, (y, x) in G.medge.items()]
    return SW(G.m, [list(map(bool, r)) for r in G.le], G.E, G.F, G.s, G.t, G.N, me)


def main():
    kmax, lmax, bpmax = map(int, sys.argv[1:4])
    import yfam
    import xfam
    import zfam
    from fool import yd
    from wfam import wfam
    from obfam import ob
    from bpfam import bp
    insts = []
    for k in range(2, kmax + 1):
        for contact in (False, True):
            I, full, info = yfam.yfam(k, contact=contact)
            insts.append(("Y", from_inst(I)[0]))
            for back in (False, True):
                Gd, _ = yd(k, back=back, contact=contact)
                insts.append(("Yd", Gd))
        for B in (False, True):
            try:
                I = zfam.zfam(k, B) if B else zfam.zfam(k)
                if isinstance(I, tuple):
                    I = I[0]
                insts.append(("Z", from_inst(I)[0]))
            except Exception as e:      # noqa: BLE001
                print("zfam skipped", k, B, e)
    for L in range(2, lmax + 1):
        I, full, info = xfam.xfam(L)
        insts.append(("X", from_inst(I)[0]))
    for n in (1, 2, 3):
        for pairing in ("F", "E"):
            G = wfam(n, pairing=pairing)
            if isinstance(G, tuple):
                G = G[0]
            insts.append(("W", G))
    for args in ((2, 2, 2, 1, 1), (3, 3, 3, 2, 1)):
        G = ob(*args)
        if isinstance(G, tuple):
            G = G[0]
        if hasattr(G, "realise"):
            G = G.realise()[0]
        insts.append(("OB", G))
    for n in range(2, bpmax + 1):
        G = bp(n)
        if isinstance(G, tuple):
            G = G[0]
        insts.append(("BP", G))
    cnt = Counter()
    for name, G in insts:
        I = to_sw(G)
        cnt["instances " + name] += 1
        try:
            r0, ps = all_shortest_valid_paths(I, cap=40, budget=1000000)
        except Budget:
            cnt["search budget " + name] += 1
            continue
        if r0 is None:
            cnt["no-instance " + name] += 1
            continue
        for P in ps:
            run_path(I, P, cnt)
    for k_ in sorted(cnt):
        print("%-60s %d" % (k_, cnt[k_]))
    fails = [k_ for k_ in cnt if k_.endswith("FAIL")]
    print("FAILURES:", fails if fails else "none")


if __name__ == "__main__":
    main()
