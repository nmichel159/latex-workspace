"""rv-r6-chain, L1 sizes: over all graph-level records of runs/*.jsonl check m <= q - 2, q <= n, |R| <= |E|,
nodes N <= q + |R|; print the maxima of m / n and N / (n + |E|)."""
import glob
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
c = Counter()
mx = Counter()
for f in sorted(glob.glob(os.path.join(HERE, "runs", "*.jsonl"))):
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("skip") or r.get("n") is None or r.get("m") is None or r.get("e") is None:
                continue
            c["graph-level records"] += 1
            n, e, q, m, N, R = r["n"], r["e"], r["q"], r["m"], r["N"], r["R"]
            c["violations m > q - 2"] += m > q - 2
            c["violations q > n"] += q > n
            c["violations |R| > |E|"] += R > e
            c["violations N > q + |R|"] += N > q + R
            mx["max m"] = max(mx["max m"], m)
            mx["max N"] = max(mx["max N"], N)
            mx["max n"] = max(mx["max n"], n)
print(dict(c))
print(dict(mx))
