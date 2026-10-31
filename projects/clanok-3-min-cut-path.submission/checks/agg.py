"""Totals over the logs in runs/: one table per kind of log (planted, graph, climb, tiny).  Usage: agg.py PREFIX [KEY_SUBSTRING ...]"""
import glob
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
pref = sys.argv[1]
want = sys.argv[2:]
tot = Counter()
mx = Counter()
fails = []
n = 0
per = defaultdict(Counter)
for fn in sorted(glob.glob(os.path.join(HERE, "runs", pref + "*.txt"))):
    n += 1
    base = os.path.basename(fn)
    with open(fn, encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip()
            if ln.startswith("FAILURES:"):
                if "none" not in ln:
                    fails.append((base, ln[:400]))
                continue
            if ln.startswith(("accepted", "rejected", "base ", "mode ", "seed ", "graphs checked")):
                continue
            k, _, v = ln.rpartition(" ")
            if not v.isdigit():
                continue
            v = int(v)
            if k.startswith("max ") or " max " in k or k.endswith("max"):
                mx[k] = max(mx[k], v)
            else:
                tot[k] += v
            parts = base.split("-")
            if len(parts) >= 2:
                per[parts[1]][k] += v
print("logs", n)
for k in sorted(tot):
    if not want or any(w in k for w in want):
        print("%-60s %12d" % (k, tot[k]))
for k in sorted(mx):
    print("%-60s %12d" % (k, mx[k]))
print("FAILURES:", fails if fails else "none")
