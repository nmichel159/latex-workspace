"""Resume an interrupted run of check_reduction.py for one family.

Usage: python resume_family.py <family> <processes>
Reads info-<family>.jsonl (the formulas finished before the interruption), runs check_reduction.work on the jobs of
the family whose seed is missing (largest formulas first, one job per task), appends them to
info-<family>-rest.jsonl, and writes results-reduction-<family>.txt from both files together, in the format of
check_reduction.py. The jobs and the checks are those of check_reduction.py / redcheck.py, unchanged.
"""

import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_reduction as cr  # noqa: E402


def load(path):
    out = []
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
    return out


def summarize(name, recs, seconds, note):
    allf = []
    stats = dict(formulas=0, sat=0, unsat=0, bb=0, bb_budget=0, brute=0, branch=0, R10=0,
                 nmin=10 ** 9, nmax=0, emax=0, cmin=10 ** 9, cmax=0, fillers_M1=0)
    for r in recs:
        clauses, so, seed, info, fails = r["f"], r["sync"], r["seed"], r["info"], r["fails"]
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
    counts = {}
    smallest = {}
    for clauses, so, seed, fails in allf:
        for fl in fails:
            counts[fl[0]] = counts.get(fl[0], 0) + 1
            size = sum(len(C) for C in clauses)
            if fl[0] not in smallest or size < smallest[fl[0]][0]:
                smallest[fl[0]] = (size, clauses, so, seed, fl)
    lines = ["check_reduction.py %s: %d formulas, %.0f s (%s)" % (name, stats["formulas"], seconds, note),
             "stats: " + json.dumps(stats),
             "failing formulas: %d" % len(allf),
             "failures by check: " + json.dumps(counts)]
    for key, (size, clauses, so, seed, fl) in sorted(smallest.items()):
        lines.append("smallest %s: L=%d formula=%s sync=%s seed=%d detail=%s" % (key, size, clauses, so, seed, fl))
    return lines


def main():
    name, nproc = sys.argv[1], int(sys.argv[2])
    t0 = time.time()
    first = load(os.path.join(HERE, "info-%s.jsonl" % name))
    rest_path = os.path.join(HERE, "info-%s-rest.jsonl" % name)
    rest = load(rest_path)
    done = {(json.dumps(r["f"]), r["sync"], r["seed"]) for r in first + rest}
    jobs = [j for j in cr.family(name) if (json.dumps(j[0]), j[1], j[2]) not in done]
    jobs.sort(key=lambda j: -sum(len(C) for C in j[0]))
    print("%s: %d finished before, %d to run" % (name, len(done), len(jobs)), flush=True)
    with Pool(nproc) as pool, open(rest_path, "a") as fh:
        for k, (clauses, so, seed, info, fails) in enumerate(pool.imap_unordered(cr.work, jobs, chunksize=1)):
            fh.write(json.dumps(dict(f=clauses, sync=so, seed=seed, info=info, fails=fails), default=str) + "\n")
            fh.flush()
            print("%d/%d seed=%s m=%d time=%s fails=%d" % (k + 1, len(jobs), seed, len(clauses),
                                                          info.get("time"), len(fails)), flush=True)
    recs = load(os.path.join(HERE, "info-%s.jsonl" % name)) + load(rest_path)
    note = "%d formulas in info-%s.jsonl (interrupted run) + %d in info-%s-rest.jsonl; this resume took %.0f s" % (
        len(first), name, len(recs) - len(first), name, time.time() - t0)
    lines = summarize(name, recs, sum(r["info"].get("time", 0) for r in recs), "sum of per-formula times; " + note)
    with open(os.path.join(HERE, "results-reduction-%s.txt" % name), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
