"""Exact single-term cost of saved instances (r7-lb.md Section 3).

usage: python scan_files.py LOG FILES...
Files: r5-core JSON (hunt_single.save), rv-r6-core JSON (adv8.dump), own JSON (lbcore.dump).  For each yes-instance:
number of minimal valid pairs, exact minimum total cost (tools + anchors + flips) of one connecting term, the term
(verified), and the profile (least anchors + flips with at most t tools, t = 0..3).
"""
import sys
import time
import json
import lbcore


def load_any(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if "medge" in d or "nn" in d:
        return lbcore.load(path)[0]
    raise ValueError("unknown format " + path)


def main():
    log = open(sys.argv[1], "a", encoding="utf-8")
    best = None
    for path in sys.argv[2:]:
        t0 = time.time()
        try:
            I = load_any(path)
        except Exception as e:  # noqa
            print("skip %s: %s" % (path, e), flush=True)
            continue
        pairs = lbcore.valid_pairs(I)
        if not pairs:
            line = "%s m=%d NO-instance" % (path, I.m)
        else:
            r = lbcore.mincost(I, cap=12, pairs=pairs)
            pr = lbcore.profile(I, pairs=pairs)
            line = "%s m=%d pairs=%d total=%s kind=%s T=%s Tp=%s anc=%s flips=%s verified=%s profile=%s (%.1fs)" % (
                path, I.m, len(pairs), r["total"], r.get("kind"), r.get("T"), r.get("Tp"), r.get("anchors"),
                r.get("flips"), r.get("verified"), {t: v[0] for t, v in pr.items()}, time.time() - t0)
            if isinstance(r["total"], int) and (best is None or r["total"] > best[0]):
                best = (r["total"], path)
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()
    line = "max total cost %s" % (best,)
    print(line)
    log.write(line + "\n")


if __name__ == "__main__":
    main()
