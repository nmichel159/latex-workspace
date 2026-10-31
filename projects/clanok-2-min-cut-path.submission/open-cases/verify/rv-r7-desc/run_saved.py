"""Referee rv-r7-desc: construction of Theorem B on saved instances.  Usage: run_saved.py LOG.  Own loader, own solver."""
import glob
import json
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from swf import inst_from_json, inst_from_zz, ClaimFail, Budget  # noqa: E402
from proof import run_all  # noqa: E402

GROUPS = [
    ("r7-lb/inst", "r7-lb/inst/*.json"),
    ("r7-lb/adv", "r7-lb/runs/adv/*best-inst*.json"),
    ("r7-lb/sa", "r7-lb/runs/sa/*best-inst.json"),
    ("r4-search", "r4-search/instances/*.json"),
    ("r5-core/single", "r5-core/runs/single/*.json"),
    ("rv-r6/deep", "verify/rv-r6-core/runs/deep/*.json"),
]


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if "le" not in d:
        return None
    if "R" in d and "u" in d:
        return inst_from_zz(d["n"], d["le"], d["R"], d["u"], d["v"])
    if "E" in d:
        return inst_from_json(d)
    return None


def main():
    log = open(sys.argv[1], "w", encoding="utf-8")
    rng = random.Random(20261031)
    fails = []
    for name, pat in GROUPS:
        st = Counter()
        files = sorted(glob.glob(os.path.join(OC, pat)))
        t0 = time.time()
        for fp in files:
            try:
                I = load(fp)
            except Exception as e:
                st["load error"] += 1
                print("load error", fp, e, file=log, flush=True)
                continue
            if I is None:
                st["other format"] += 1
                continue
            st["files"] += 1
            I.validate()
            if not I.p2():
                st["no P2 (skipped)"] += 1
                continue
            if I.s == I.t:
                st["s = t"] += 1
                continue
            try:
                w = I.shortest(budget=3_000_000)
            except Budget:
                st["budget"] += 1
                continue
            if w is None:
                st["no-instances"] += 1
                if I.m <= 18:
                    assert not I.exact_downsets()[0], "solver and down-set enumeration disagree: " + fp
                continue
            st["yes-instances"] += 1
            r = len(w)
            st["max r"] = max(st["max r"], r)
            st["max m"] = max(st["max m"], I.m)
            paths = I.all_shortest(r, cap=300)
            assert any(p == w for p in paths) or len(paths) == 300, "enumerator misses a path " + fp
            for P in paths:
                try:
                    run_all(I, P, rng, st, trials=2)
                except ClaimFail as e:
                    fails.append((fp, str(e), P))
                    print("FAIL", fp, e, P, file=log, flush=True)
        print("==", name, len(files), "files, time", round(time.time() - t0, 1), file=log)
        for k in sorted(st):
            print("  ", k, st[k], file=log)
        log.flush()
    print("FAILURES:", fails if fails else "none", file=log)
    log.close()


if __name__ == "__main__":
    main()
