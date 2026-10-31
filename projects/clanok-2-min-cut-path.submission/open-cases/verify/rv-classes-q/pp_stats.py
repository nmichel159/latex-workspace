"""Statistics for Lemma PP (not a claim of r5-classes.md): the least |Err(u, b)| over ALL admissible pairs, per
shortest valid path and type, and per instance the best (least) value over its shortest paths and types.

usage: python pp_stats.py SEED COUNT r nTc nOc mates offc
"""
import json
import random
import sys
from collections import Counter

from qchecks import check_pp
from qgen2 import incremental, word_of


def main():
    seed, count, r, nTc, nOc, mates, offc = map(int, sys.argv[1:8])
    rng = random.Random(seed)
    per_path = Counter()
    per_inst = Counter()
    st = {}
    n_inst = 0
    for it in range(count):
        out = incremental(rng, r, nTc, nOc, mates=mates, offc=offc, word=word_of(rng, r, "blocks"))
        if out is None:
            continue
        I, P = out
        n_inst += 1
        L, paths = I.shortest_paths_dfs(limit=20)
        best = None
        for Q in paths:
            for T in (0, 1):
                v = check_pp(I, list(Q), T, st)
                per_path[v if v is not None else "nopair"] += 1
                if v is not None and (best is None or v < best):
                    best = v
                if v is None:
                    best = 0 if best is None else min(best, 0)
        per_inst[best] += 1
    print("instances", n_inst, "checked pairs", st.get("PP_pairs", 0), "fallbacks", st.get("PP_fallback", 0))
    print("per (path, type): least |Err| over all pairs:", sorted(per_path.items(), key=lambda kv: str(kv[0])))
    print("per instance: least over paths and types (0 = fallback with misclassification 0):",
          sorted(per_inst.items(), key=lambda kv: str(kv[0])), flush=True)


if __name__ == "__main__":
    main()
