"""Referee rv-r7-desc: aggregate the logs of run_planted.py.  Usage: agg.py runs/planted-*.txt"""
import ast
import re
import sys
from collections import Counter, defaultdict

sums = defaultdict(Counter)
acc = defaultdict(Counter)
rej = defaultdict(Counter)
fails = []
for fn in sys.argv[1:]:
    base = re.search(r"planted-([a-zA-Z]+)-", fn).group(1)
    done = False
    for ln in open(fn, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if ln.startswith("FAILURES"):
            done = True
            if "none" not in ln:
                fails.append((fn, ln[:300]))
            continue
        if ln.startswith("FAIL"):
            fails.append((fn, ln[:300]))
            continue
        if ln.startswith("accepted moves") or ln.startswith("rejected moves"):
            d = ast.literal_eval(ln.split(" moves ", 1)[1])
            (acc if ln.startswith("acc") else rej)[base].update(d)
            continue
        m = re.match(r"(.*) (\d+)$", ln)
        if m:
            k, v = m.group(1), int(m.group(2))
            if k.startswith("max") or k.endswith("max"):
                sums[base][k] = max(sums[base][k], v)
            else:
                sums[base][k] += v
    if not done:
        fails.append((fn, "log incomplete (timeout?)"))
keys = sorted({k for c in sums.values() for k in c})
bases = sorted(sums)
print("%-48s" % "counter" + "".join("%11s" % b for b in bases))
for k in keys:
    print("%-48s" % k[:48] + "".join("%11d" % sums[b][k] for b in bases))
print("accepted moves")
for b in bases:
    print("  ", b, dict(acc[b]))
print("rejected moves")
for b in bases:
    print("  ", b, dict(rej[b]))
print("FAILURES:", fails if fails else "none")
