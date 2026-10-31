"""r7-desc: Theorem B and Lemmas J, G on the stored ZZ instances of r4-search/instances, all shortest valid paths (cap 20)."""
import glob
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
sys.path.append(HERE)
from check_b import run_path  # noqa: E402
from zzl import Budget, all_shortest_valid_paths, zz_to_sw  # noqa: E402


def main():
    cnt = Counter()
    for path in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        if "le" not in d or "R" not in d:
            cnt["other format"] += 1
            continue
        le = [[bool(b) for b in row] for row in d["le"]]
        R = [tuple(e) for e in d["R"]]
        I, _ = zz_to_sw(d["n"], d["u"], d["v"], le, R)
        cnt["instances"] += 1
        if I.s == I.t:
            cnt["s = t"] += 1
            continue
        try:
            r0, ps = all_shortest_valid_paths(I, cap=20, budget=1000000)
        except Budget:
            cnt["search budget"] += 1
            continue
        if r0 is None:
            cnt["no-instances"] += 1
            continue
        for P in ps:
            run_path(I, P, cnt)
    for k_ in sorted(cnt):
        print("%-60s %d" % (k_, cnt[k_]))
    fails = [k_ for k_ in cnt if k_.endswith("FAIL")]
    print("FAILURES:", fails if fails else "none")


if __name__ == "__main__":
    main()
