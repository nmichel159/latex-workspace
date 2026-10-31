"""Portfolio on the known families (timing and verdicts).  Usage: python try_known.py LEVEL"""
import sys
import time
import known
from portfolio import portfolio, summary

level = int(sys.argv[1]) if len(sys.argv) > 1 else 2
which = sys.argv[2] if len(sys.argv) > 2 else "all"
cases = []
if which in ("all", "small"):
    cases += [known.a14(), known.ladder(3), known.ladder(4), known.ladder(3, True)]
    cases += [known.rigid_2ch(L) for L in (4, 6, 8)]
    cases += [known.tic_mates(L, m) for L in (4, 6) for m in ("tie", "oneway")]
if which in ("all", "hub"):
    cases += [known.hub(2, 2), known.hub(2, 2, True)]
if which in ("big",):
    cases += [known.rigid_2ch(L) for L in (9, 10)]
    cases += [known.tic_mates(L, m) for L in (8,) for m in ("tie", "oneway")]
for name, z, names, sw in cases:
    t = time.time()
    r = portfolio(z, level=level, sw=sw, stop_early=False)
    print("%-14s %s %s" % (name, summary(r), r["time"]), flush=True)
