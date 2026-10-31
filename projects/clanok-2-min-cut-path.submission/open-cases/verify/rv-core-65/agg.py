"""Aggregate the final summaries of several run logs (reviewer rv-core-65): counters are summed, keys containing
'max' take the maximum.  Only the block after the last line starting with a script name is read.

usage: python agg.py LOG [LOG ...]
"""
import sys
from fractions import Fraction


def parse(fn):
    lines = open(fn).read().splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln and not ln.startswith(" "):
            start = i
    if start is None:
        return None, {}
    out = {}
    for ln in lines[start + 1:]:
        if not ln.startswith("  ") or ln.startswith("   "):
            continue
        parts = ln.strip().rsplit(None, 1)
        if len(parts) != 2:
            continue
        key, val = parts
        try:
            v = Fraction(val)
        except ValueError:
            continue
        out[key.strip()] = v
    return lines[start], out


tot = {}
for fn in sys.argv[1:]:
    head, d = parse(fn)
    print("#", fn, "|", head)
    for k, v in d.items():
        if "max" in k:
            tot[k] = max(tot.get(k, v), v)
        else:
            tot[k] = tot.get(k, 0) + v
for k in sorted(tot):
    print("  %-55s %s" % (k, tot[k]))
