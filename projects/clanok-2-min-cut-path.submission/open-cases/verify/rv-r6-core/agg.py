"""Sum the counters of the SUMMARY blocks of several logs (maximum for keys starting with 'max').
usage: python agg.py LOG [LOG ...] > TOTAL"""
import sys
from collections import Counter

tot = Counter()
mx = {}
fails = []
for fp in sys.argv[1:]:
    insum = False
    with open(fp, encoding="utf-8") as f:
        for line in f:
            if line.startswith("SUMMARY"):
                insum = True
                continue
            if line.startswith("FAILURES"):
                insum = False
                if "none" not in line:
                    fails.append((fp, line.strip()))
                continue
            if insum and line.startswith("  ") and ": " in line:
                k, v = line.strip().rsplit(": ", 1)
                v = int(v)
                if k.startswith("max"):
                    mx[k] = max(mx.get(k, v), v)
                else:
                    tot[k] += v
print("TOTAL of %d logs: %s" % (len(sys.argv) - 1, ", ".join(sys.argv[1:])))
for k in sorted(set(tot) | set(mx)):
    print("  %s: %d" % (k, mx[k] if k in mx else tot[k]))
print("FAILURES: %s" % (fails if fails else "none"))
