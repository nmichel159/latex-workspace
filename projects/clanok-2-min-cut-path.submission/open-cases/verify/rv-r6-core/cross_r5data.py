"""Cross-check on r5-core's stored instances (DATA only, read from ../../r5-core/runs/*.json; no code imported):
the two-level example of r5-core.md 8.4 and the 23 'single' instances.  Each instance is loaded into the own switch
form (private nodes of middle edges from 'medge'), P2 is checked, all shortest valid paths are computed (exact, with
a cap) and the own program of the proof (proof8.levels, all picks and modes) runs on each; the final intersection is
tested in the switch form and in the ZZ realisation.

usage: python cross_r5data.py [LOG]
"""
import sys
import os
import json
import glob
from collections import Counter
from zzl import SW, Skel, all_shortest_valid_paths, sw_to_zz, kparam, popcount
import proof8
from adv8 import run_path

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "r5-core", "runs"))


def load_r5(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    N = d["N"]
    E = [int(x) for x in d["E"]]
    F = [int(x) for x in d["F"]]
    m = len(E)
    le = [[bool(b) for b in row] for row in d["le"]]
    me = [(int(v[0]), int(v[1]), int(p)) for p, v in d["medge"].items()]
    I = SW(m, le, E, F, d["s"], d["t"], N, me)
    P = None
    ex = d.get("extra") or {}
    if "P" in ex:
        P = [(i // 2, i % 2) for i in ex["P"]]
    return I, P, d


def main():
    logp = sys.argv[1] if len(sys.argv) > 1 else None
    logf = open(logp, "a", encoding="utf-8") if logp else None

    def out(s):
        print(s, flush=True)
        if logf:
            logf.write(s + "\n")
            logf.flush()
    files = [os.path.join(SRC, "two-levels-example.json")] + sorted(glob.glob(os.path.join(SRC, "single", "*.json")))
    st = Counter()
    out("cross_r5data pid=%d, %d files from %s" % (os.getpid(), len(files), SRC))
    for fp in files:
        I, P, d = load_r5(fp)
        # consistency of the private nodes: p in F_z and E_v
        for (z, v, p) in I.me:
            if not ((I.F[z] >> p) & 1 and (I.E[v] >> p) & 1):
                st["PRIVATE NODE NOT IN F_z AND E_v FAIL"] += 1
            if not (I.le[z][v] and not I.le[v][z]):
                st["MIDDLE EDGE NOT STRICT FAIL"] += 1
        if not I.p2_switch():
            st["R5 INSTANCE WITHOUT P2 FAIL"] += 1
        r, paths = all_shortest_valid_paths(I, cap=20)
        st["files"] += 1
        if r is None:
            st["R5 INSTANCE WITHOUT VALID PATH FAIL"] += 1
            continue
        if P is not None:
            if P not in [[tuple(x) for x in pp] for pp in paths]:
                st["stored path not among the shortest"] += 1
            else:
                st["stored path is shortest"] += 1
        zzc = sw_to_zz(I)
        for pp in paths:
            st["paths"] += 1
            Sk = Skel(I, [tuple(x) for x in pp])
            res = run_path(I, [tuple(x) for x in pp], st, "cross", zzc, "cross-" + os.path.basename(fp)[:-5])
            out("  %s m=%d k=%d r=%d |A|=%d levels %s" % (os.path.basename(fp), I.m, kparam(I.m)[0], r,
                                                         popcount(Sk.A), res))
    out("SUMMARY cross_r5data")
    for key in sorted(st):
        out("  %s: %d" % (key, st[key]))
    fails = [key for key in st if key.endswith("FAIL") and st[key]]
    out("FAILURES: %s" % (", ".join(fails) if fails else "none"))


if __name__ == "__main__":
    main()
