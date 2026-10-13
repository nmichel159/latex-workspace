"""Per-family summary of the info-*.jsonl files written by check_reduction.py / resume_family.py (Markdown rows).

Usage: python summarize.py  ->  prints the table of Section 3.2 and the list of Section 3.3 of hardness-compute.md,
and writes them to results-summary.txt.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FAMS = [("F1", ["info-F1.jsonl"]), ("F1s", ["info-F1s.jsonl"]), ("F2", ["info-F2.jsonl"]),
        ("F3", ["info-F3.jsonl", "info-F3-rest.jsonl"]), ("F4", ["info-F4.jsonl"])]


def load(fn):
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        return []
    with open(p) as fh:
        return [json.loads(x) for x in fh if x.strip()]


def main():
    out = ["| Family | formulas | sat / unsat | sync orders | `n` | `abs(E)` | `c` | minimum cuts | R6 (brute / branch) | "
           "R8 finished | R10 (all `2^L` sets) | failing formulas |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    budget = []
    tot = dict(f=0, fails=0, bb=0)
    for name, files in FAMS:
        recs = [r for fn in files for r in load(fn)]
        if not recs:
            continue
        I = [r["info"] for r in recs if "error" not in r["info"]]
        err = sum(1 for r in recs if "error" in r["info"])
        nf = sum(1 for r in recs if r["fails"]) + 0
        sat = sum(1 for i in I if i["sat"])
        syncs = sorted({r["sync"] for r in recs})
        bb = sum(1 for i in I if i["R8"].startswith("bb"))
        tot["f"] += len(recs)
        tot["fails"] += nf
        tot["bb"] += bb
        out.append("| %s | %d | %d / %d | %s | %d-%d | %d-%d | %d-%d | %d-%d | %d / %d | %d | %d | %d%s |" % (
            name, len(recs), sat, len(I) - sat, ", ".join(syncs),
            min(i["n"] for i in I), max(i["n"] for i in I), min(i["e"] for i in I), max(i["e"] for i in I),
            min(i["c"] for i in I), max(i["c"] for i in I), min(i["cuts"] for i in I), max(i["cuts"] for i in I),
            sum(i["R6"] == "brute" for i in I), sum(i["R6"] == "branch" for i in I), bb,
            sum(i["R10"] == "all" for i in I), nf, (" (%d exceptions)" % err) if err else ""))
        for r in recs:
            i = r["info"]
            if i.get("R8") == "budget":
                budget.append((name, r["seed"], r["sync"], i["m"], i["L"], i["n"], i["e"], i["c"], i["sat"], i["cuts"]))
    out.append("| total | %d | | | | | | | | %d | | %d |" % (tot["f"], tot["bb"], tot["fails"]))
    out.append("")
    out.append("R8 not finished (node budget 20000 of cp_eq_c_bb2): %d formulas" % len(budget))
    out.append("family seed sync m L n |E| c sat cuts")
    for b in sorted(budget, key=lambda b: (b[0], b[3], b[1])):
        out.append(" ".join(str(x) for x in b))
    # path lengths (m, minlen) over satisfiable formulas
    lens = {}
    for name, files in FAMS:
        for fn in files:
            for r in load(fn):
                i = r["info"]
                if "error" in i or not i["sat"]:
                    continue
                key = (i["m"], i["minlen"])
                lens[key] = lens.get(key, 0) + 1
    out.append("")
    out.append("(m, shortest path inside a minimum cut): count, satisfiable formulas of all families")
    out.append(" ".join("(%d,%d):%d" % (k[0], k[1], c) for k, c in sorted(lens.items())))
    viol = sum(c for (m, l), c in lens.items() if l < 2 * m + 1 or l % 2 == 0)
    out.append("violations of 'odd and >= 2m + 1': %d" % viol)
    text = "\n".join(out)
    with open(os.path.join(HERE, "results-summary.txt"), "w") as fh:
        fh.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
