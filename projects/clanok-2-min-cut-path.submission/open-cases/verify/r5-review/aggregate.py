"""Sum the counters printed at the end of the test_general.py logs.  Usage: python aggregate.py LOG..."""
import ast
import sys
from collections import Counter


def main():
    tot = Counter()
    for p in sys.argv[1:]:
        txt = open(p, encoding="utf-8").read().strip().splitlines()
        last = [ln for ln in txt if ln.startswith("mode ")]
        if not last:
            print("no summary in", p)
            continue
        d = ast.literal_eval(last[-1].split(":", 1)[1].strip())
        tot.update(d)
        print(p, "count", d.get("yes", 0) + d.get("no", 0))
    for k in sorted(tot):
        print("%-22s %d" % (k, tot[k]))


if __name__ == "__main__":
    main()
