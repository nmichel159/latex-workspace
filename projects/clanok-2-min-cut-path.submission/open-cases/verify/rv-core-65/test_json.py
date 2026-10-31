"""Run the checks of test_lemmas and test_thm65 on ZZ instances stored as JSON (n, u, v, le, R), converted to the
general switch form by the reviewer's own converter gsf.from_zz.  Instance files are data of other agents
(r4-search/instances), read only.

usage: python test_json.py GLOB [MMAX] [PATHCAP] [GDESC_MMAX]
"""
import sys
import glob
import json
import math
import time
import random
from collections import Counter
from gsf import from_zz, bits
from thy import Stars
import test_lemmas
import test_thm65


def main():
    pat = sys.argv[1]
    mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    gd = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    rng = random.Random(0)
    st = Counter()
    t0 = time.time()
    rows = []
    for fn in sorted(glob.glob(pat)):
        with open(fn) as fh:
            d = json.load(fh)
        I = from_zz(d["n"], d["u"], d["v"], d["le"], d["R"], d.get("name", fn))
        I.validate()
        st["files"] += 1
        if I.m > mmax:
            st["skipped (m > %d)" % mmax] += 1
            continue
        if not I.p2():
            st["not P2 in switch form"] += 1
            continue
        if I.s == I.t:
            st["s = t"] += 1
            continue
        t1 = time.time()
        r, paths = I.shortest_paths(cap=cap)
        if r is None:
            st["no-instances"] += 1
            exp = d.get("verdict", {}).get("exact")
            if exp is True:
                st["ANSWER DISAGREES WITH FILE VERDICT"] += 1
            continue
        exp = d.get("verdict", {}).get("exact")
        if exp is False:
            st["ANSWER DISAGREES WITH FILE VERDICT"] += 1
        St = Stars(I)
        for P in paths:
            test_lemmas.check_path(I, St, P, st, 3)
        test_thm65.analyse(I, st, cap, rng, gd)
        rows.append((d.get("name", fn), I.m, r, len(paths), round(time.time() - t1, 1)))
    print("test_json %s mmax %d cap %d gdesc<=%d (%.0fs)" % (pat, mmax, cap, gd, time.time() - t0))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))
    print("  instances (name, m, r, paths, seconds):")
    for row in rows:
        print("   ", row)


if __name__ == "__main__":
    main()
