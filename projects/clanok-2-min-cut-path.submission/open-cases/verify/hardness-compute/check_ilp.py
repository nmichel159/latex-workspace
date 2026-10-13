"""Third computation of cp(u,v) on reduction graphs: the integer program of vilp.py (CBC).
Claim tested (Corollary 2.6 (a), (c)): cp(u,v) = c0 if phi is satisfiable and c0 + 1 otherwise.
Formulas: F1 and F2 of check_reduction.py with m <= 2 clauses, and the natural-order formulas of F4 with at most
F4_NMAX vertices (a first run with all of F4 hung for more than 20 minutes on the four largest graphs, 108-142
vertices: CBC does not apply its time limit during the root-node work). Each ILP has a time limit; unsolved
instances are counted, not hidden. One line per formula goes to ilp-jobs.jsonl as soon as it is solved.
Validation of vilp.cp_ilp against cp_paths on small graphs: see the first block (atlas sample).
Output: results-ilp.txt
"""

import os
import random
import sys
import time
import warnings
from multiprocessing import Pool

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


F4_NMAX = 60


def work(job):
    warnings.filterwarnings("ignore")
    import vilp
    import vred
    clauses, tl = job
    R = vred.build(clauses)
    t = time.time()
    val, st = vilp.cp_ilp(R["g"], R["u"], R["v"], time_limit=tl)
    want = R["c0"] + (0 if vred.is_sat(clauses) else 1)
    return clauses, R["n"], val, st, want, round(time.time() - t, 1)


def atlas_job(args):
    warnings.filterwarnings("ignore")
    import networkx as nx
    import vlib
    import vilp
    idx = args
    G = nx.graph_atlas(idx)
    g = vlib.from_nx(G)
    bad = []
    cnt = 0
    for u in range(g.n):
        for v in range(g.n):
            if u != v:
                a = vilp.cp_ilp(g, u, v)[0]
                b = vlib.cp_paths(g, u, v)
                cnt += 1
                if a != b:
                    bad.append((idx, u, v, a, b))
    return cnt, bad


def main():
    import json
    import networkx as nx
    import check_reduction as cr
    import vred
    t0 = time.time()
    rng = random.Random(11)
    idxs = [i for i, G in enumerate(nx.graph_atlas_g()) if G.number_of_nodes() >= 2 and nx.is_connected(G)]
    sample = rng.sample(idxs, 150)
    jobs = []
    for fam in ("F1", "F2"):
        for clauses, so, seed in cr.family(fam):
            if len(clauses) <= 2:
                jobs.append((clauses, 120))
    skipped = []
    for clauses, so, seed in cr.family("F4"):
        if so == "natural":
            n = vred.build(clauses)["n"]
            if n <= F4_NMAX:
                jobs.append((clauses, 300))
            else:
                skipped.append((clauses, n))
    lines = []
    with Pool(int(os.environ.get("NPROC", "30"))) as pool:
        pairs, bad = 0, []
        for cnt, b in pool.imap_unordered(atlas_job, sample):
            pairs += cnt
            bad += b
        lines.append("vilp.cp_ilp vs vlib.cp_paths on %d atlas graphs (%d ordered pairs): mismatches %d %s"
                     % (len(sample), pairs, len(bad), bad[:5]))
        ok = unsolved = wrong = 0
        wrongs, unsol = [], []
        fh = open(os.path.join(HERE, "ilp-jobs.jsonl"), "w")
        for clauses, n, val, st, want, tt in pool.imap_unordered(work, jobs):
            fh.write(json.dumps(dict(f=clauses, n=n, cp=val, status=st, want=want, time=tt)) + "\n")
            fh.flush()
            if val is None:
                unsolved += 1
                unsol.append((clauses, n, st, tt))
            elif val != want:
                wrong += 1
                wrongs.append((clauses, n, val, want))
            else:
                ok += 1
        fh.close()
    lines.append("reduction graphs: %d formulas; cp(ILP) == c0 + [unsat]: %d; different: %d; not solved in the time limit: %d"
                 % (len(jobs), ok, wrong, unsolved))
    lines.append("F4 formulas left out (more than %d vertices): %r" % (F4_NMAX, skipped))
    lines += ["different: %r" % (w,) for w in wrongs[:20]]
    lines += ["unsolved: %r" % (w,) for w in unsol[:20]]
    lines.append("time %.0f s" % (time.time() - t0))
    with open(os.path.join(HERE, "results-ilp.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
