"""Driver: runs redcheck.check_formula on families of CNF formulas, in parallel.

Families (argument 1):
  F1    all 3-CNF formulas (three literals per clause, repetitions allowed) over x1..x3 with m = 1, 2, 3 clauses,
        one formula per class under renaming of variables (clause order and literal multisets kept); natural sync order
  F1s   F1 with m <= 2 in random and reverse sync order, plus a seeded sample of 2000 m = 3 formulas in random order
  F2    all CNF formulas with clauses of 1..3 literals over x1, x2, m = 1, 2, 3, at least one clause shorter than 3
  F3    seeded random 3-CNF, n = 3..7 variables, m = 4..30 clauses (natural or random sync order)
  F4    hand-picked: full unsatisfiable 3-CNF on 3 variables, examples of the text, variables with gaps, long clauses
Output: results-reduction-<family>.txt (summary, failures) and info-<family>.jsonl (one line per formula).
"""

import itertools
import json
import os
import random
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def lit_key(l):
    return (abs(l), l < 0)


def clause_types(nv, sizes):
    lits = sorted([i for i in range(1, nv + 1)] + [-i for i in range(1, nv + 1)], key=lit_key)
    out = []
    for s in sizes:
        out += [tuple(C) for C in itertools.combinations_with_replacement(lits, s)]
    return out


def canon(f, nv):
    best = None
    for p in itertools.permutations(range(1, nv + 1)):
        mp = {i + 1: p[i] for i in range(nv)}
        g = tuple(tuple(sorted(((mp[abs(l)] if l > 0 else -mp[abs(l)]) for l in C), key=lit_key)) for C in f)
        if best is None or g < best:
            best = g
    return best


def family(name):
    jobs = []
    if name in ("F1", "F1s"):
        T = clause_types(3, [3])
        for m in (1, 2, 3):
            fs = [f for f in itertools.product(T, repeat=m) if canon(f, 3) == f]
            if name == "F1":
                jobs += [(list(map(list, f)), "natural", 0) for f in fs]
            else:
                if m <= 2:
                    jobs += [(list(map(list, f)), "random", i) for i, f in enumerate(fs)]
                    jobs += [(list(map(list, f)), "reverse", 0) for f in fs]
                else:
                    rng = random.Random(7)
                    for i, f in enumerate(rng.sample(fs, 2000)):
                        jobs.append((list(map(list, f)), "random", i))
    elif name == "F2":
        T = clause_types(2, [1, 2, 3])
        for m in (1, 2, 3):
            for f in itertools.product(T, repeat=m):
                if min(len(C) for C in f) < 3 and canon(f, 2) == f:
                    jobs.append((list(map(list, f)), "natural", 0))
    elif name == "F3":
        rng = random.Random(20261012)
        for i in range(400):
            n = rng.randint(3, 7)
            m = rng.randint(4, min(30, 5 * n))
            f = [[rng.choice([1, -1]) * rng.randint(1, n) for _ in range(3)] for _ in range(m)]
            jobs.append((f, rng.choice(["natural", "random"]), i))
    elif name == "F4":
        full = [[s1 * 1, s2 * 2, s3 * 3] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]
        fs = [
            full,
            full[::-1],
            full[:7],                                   # satisfiable (one assignment)
            [[1], [1]],
            [[1], [2], [-3], [-4]],
            [[1], [2], [3], [-4], [-5], [-6]],
            [[1, 1, 1], [-1, -1, -1]],
            [[1, 1, -1], [-1, -1, 1], [1, -1, -1]],
            [[1, -1, 2], [-2, 2, -2], [-1, -2, 1]],
            [[5, 9, -5]],                               # variables with gaps
            [[2, -7], [7, -2], [2, 7], [-2, -7]],       # unsatisfiable, gaps
            [[1, 2, 3, 4, 5]],                          # long clause
            [[1, -2, 3, -4, 5, -6, 7]],
            [[1], [-1]],
            [[1, 2], [-1, 2], [1, -2], [-1, -2]],
            [[-1], [-1], [-1], [1]],
            [[1, 2, 3], [-1, -2, -3]] * 3,
        ]
        for i, f in enumerate(fs):
            for so in ("natural", "reverse", "random"):
                jobs.append((f, so, i))
    else:
        raise SystemExit("unknown family " + name)
    return jobs


def work(job):
    import redcheck
    clauses, so, seed = job
    try:
        info, fails = redcheck.check_formula(clauses, so, seed)
    except Exception as ex:  # report, never hide
        return clauses, so, seed, {"error": repr(ex)}, [("exception", repr(ex))]
    return clauses, so, seed, info, fails


def main():
    name = sys.argv[1]
    t0 = time.time()
    jobs = family(name)
    out_info = os.path.join(HERE, "info-%s.jsonl" % name)
    allf = []
    stats = dict(formulas=0, sat=0, unsat=0, bb=0, bb_budget=0, brute=0, branch=0, R10=0,
                 nmin=10 ** 9, nmax=0, emax=0, cmin=10 ** 9, cmax=0, fillers_M1=0)
    with Pool(30) as pool, open(out_info, "w") as fh:
        for clauses, so, seed, info, fails in pool.imap_unordered(work, jobs, chunksize=8):
            fh.write(json.dumps(dict(f=clauses, sync=so, seed=seed, info=info, fails=fails), default=str) + "\n")
            stats["formulas"] += 1
            if "error" in info:
                allf.append((clauses, so, seed, fails))
                continue
            stats["sat" if info["sat"] else "unsat"] += 1
            stats["bb"] += info["R8"].startswith("bb")
            stats["bb_budget"] += info["R8"] == "budget"
            stats["brute"] += info["R6"] == "brute"
            stats["branch"] += info["R6"] == "branch"
            stats["R10"] += info["R10"] == "all"
            stats["nmin"] = min(stats["nmin"], info["n"])
            stats["nmax"] = max(stats["nmax"], info["n"])
            stats["emax"] = max(stats["emax"], info["e"])
            stats["cmin"] = min(stats["cmin"], info["c"])
            stats["cmax"] = max(stats["cmax"], info["c"])
            stats["fillers_M1"] += info["c_fillers_is_M-1"]
            if fails:
                allf.append((clauses, so, seed, fails))
    # smallest failing instance per check name
    smallest = {}
    for clauses, so, seed, fails in allf:
        for fl in fails:
            key = fl[0]
            size = sum(len(C) for C in clauses)
            if key not in smallest or size < smallest[key][0]:
                smallest[key] = (size, clauses, so, seed, fl)
    counts = {}
    for _, _, _, fails in allf:
        for fl in fails:
            counts[fl[0]] = counts.get(fl[0], 0) + 1
    lines = ["check_reduction.py %s: %d formulas, %.0f s" % (name, stats["formulas"], time.time() - t0),
             "stats: " + json.dumps(stats),
             "failing formulas: %d" % len(allf),
             "failures by check: " + json.dumps(counts)]
    for key, (size, clauses, so, seed, fl) in sorted(smallest.items()):
        lines.append("smallest %s: L=%d formula=%s sync=%s seed=%d detail=%s" % (key, size, clauses, so, seed, fl))
    with open(os.path.join(HERE, "results-reduction-%s.txt" % name), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
