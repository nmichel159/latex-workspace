"""Comparison with the scripts of the agent "hardness" (open-cases/hardness/), run after all my own code was written.

The hardness/ modules are imported read-only (no bytecode is written: sys.dont_write_bytecode).
  H1  graph identity: vred.build(phi, "natural") and hardness/reduction.build(phi) give the same vertex count, u, v and
      edge set, for every formula of my families F1, F2, F4 and of the 399 formulas of hardness/check_reduction.py
  H2  the length of a shortest u-v path inside a minimum cut: my value (BFS in H_tau, recorded as "minlen" in every
      info-*.jsonl) against hardness/reduction.shortest_route(phi) (a dynamic program over the formula)
  H3  my checks R0-R11 (redcheck.check_formula, natural order) on the 399 formulas of hardness/check_reduction.py
  H4  the two libraries on random graphs: c (hardness exact.cut_value vs vlib.flow_value), the set of minimum cuts
      (exact.min_cuts_pq vs vlib.min_cuts_residual) and the answer "cp = c" (exact.cp_equals_c_paths vs
      vlib.cp_eq_c_bb2)
Output: results-compare.txt
"""

import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import random  # noqa: E402
import time  # noqa: E402
from multiprocessing import Pool  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
HARD = os.path.normpath(os.path.join(HERE, "..", "..", "hardness"))
sys.path.insert(0, HERE)
import check_reduction as cr  # noqa: E402  (mine)
import redcheck  # noqa: E402
import vlib  # noqa: E402
import vred  # noqa: E402

sys.path.append(HARD)
import exact as hx  # noqa: E402  (hardness/)
import reduction as hrd  # noqa: E402  (hardness/)

_spec = importlib.util.spec_from_file_location("hd_check_reduction", os.path.join(HARD, "check_reduction.py"))
hcr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hcr)


def norm_edges(edges):
    return sorted({(min(a, b), max(a, b)) for a, b in edges})


def h1(phi):
    R = vred.build(phi, "natural")
    g2, u2, v2, info2 = hrd.build(phi)
    same = (R["n"] == g2.n and R["u"] == u2 and R["v"] == v2 and norm_edges(R["g"].edges) == norm_edges(g2.edges))
    return same


def h3(phi):
    try:
        info, fails = redcheck.check_formula(phi, "natural", 0)
    except Exception as ex:  # report, never hide
        return phi, {"error": repr(ex)}, [("exception", repr(ex))]
    return phi, info, fails


def random_graph(rng):
    import networkx as nx
    while True:
        n = rng.randint(6, 14)
        G = nx.gnp_random_graph(n, rng.uniform(0.2, 0.5), seed=rng.randrange(10 ** 9))
        if nx.is_connected(G):
            return n, list(G.edges())


def h4(job):
    n, edges, pairs = job
    g1 = vlib.Gr(n, edges)
    g2 = hx.UG(n, edges)
    bad = []
    for u, v in pairs:
        c1 = vlib.flow_value(g1, [u], [v])
        c2 = hx.cut_value(g2, u, v)
        _, cuts1 = vlib.min_cuts_residual(g1, u, v)
        _, cuts2 = hx.min_cuts_pq(g2, u, v)
        a1, _, _ = vlib.cp_eq_c_bb2(g1, u, v, c1)
        try:
            a2 = hx.cp_equals_c_paths(g2, u, v)[0]
        except RuntimeError:            # their path budget; recorded as unknown
            a2 = a1
            bad.append(("budget", n, u, v))
            continue
        if c1 != c2 or set(cuts1) != set(cuts2) or a1 != a2:
            bad.append((n, edges, u, v, c1, c2, len(cuts1), len(cuts2), a1, a2))
    return len(pairs), bad


def main():
    """Usage: python compare_hardness.py <processes> [parts, e.g. H1,H3,H4]. Each part writes results-compare-<part>.txt;
    results-compare.txt is then rebuilt from all part files present."""
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    parts = sys.argv[2].split(",") if len(sys.argv) > 2 else ["H1", "H2", "H3", "H4"]
    theirs = hcr.family_a() + hcr.family_b() + hcr.family_c()
    mine = [j[0] for fam in ("F1", "F2") for j in cr.family(fam)] + [j[0] for j in cr.family("F4") if j[1] == "natural"]
    with Pool(nproc) as pool:
        for part in parts:
            t0 = time.time()
            if part == "H1":
                r_mine = pool.map(h1, mine, chunksize=64)
                r_theirs = pool.map(h1, theirs, chunksize=8)
                bad1 = [phi for phi, ok in zip(mine + theirs, r_mine + r_theirs) if not ok]
                line = ("H1 graph identity (natural sync order): my F1+F2+F4 %d formulas, hardness/ families (a)-(c) %d "
                        "formulas; different graphs: %d %s" % (len(mine), len(theirs), len(bad1), bad1[:3]))
            elif part == "H2":
                recs = []
                for fn in sorted(os.listdir(HERE)):
                    if fn.startswith("info-") and fn.endswith(".jsonl") and "run1" not in fn:
                        with open(os.path.join(HERE, fn)) as fh:
                            for ln in fh:
                                if ln.strip():
                                    r = json.loads(ln)
                                    recs.append((fn, r["f"], r["info"].get("minlen")))
                preds = pool.map(hrd.shortest_route, [f for _, f, _ in recs], chunksize=64)
                bad2 = [(fn, f, a, b) for (fn, f, a), b in zip(recs, preds) if a != b]
                nsat = sum(1 for _, _, a in recs if a is not None)
                line = ("H2 shortest path length in a minimum cut, my BFS value vs hardness/reduction.shortest_route: %d "
                        "records of info-*.jsonl (%d satisfiable); different: %d %s" % (len(recs), nsat, len(bad2),
                                                                                       bad2[:3]))
            elif part == "H3":
                allf, stats = [], dict(sat=0, unsat=0, bb=0, budget=0, nmax=0)
                for phi, info, fails in pool.imap_unordered(h3, theirs, chunksize=1):
                    if fails:
                        allf.append((phi, fails))
                    if "error" in info:
                        continue
                    stats["sat" if info["sat"] else "unsat"] += 1
                    stats["bb"] += info["R8"].startswith("bb")
                    stats["budget"] += info["R8"] == "budget"
                    stats["nmax"] = max(stats["nmax"], info["n"])
                line = ("H3 my checks R0-R11 on the %d formulas of hardness/check_reduction.py: %s; failing formulas: "
                        "%d %s" % (len(theirs), json.dumps(stats), len(allf), allf[:3]))
            elif part == "H4":
                rng = random.Random(99)
                jobs = []
                for _ in range(600):
                    n, edges = random_graph(rng)
                    ps = [(a, b) for a in range(n) for b in range(n) if a != b]
                    jobs.append((n, edges, rng.sample(ps, min(12, len(ps)))))
                tot, bad4 = 0, []
                for cnt, b in pool.imap_unordered(h4, jobs, chunksize=4):
                    tot += cnt
                    bad4 += b
                budget4 = [b for b in bad4 if b[0] == "budget"]
                bad4 = [b for b in bad4 if b[0] != "budget"]
                line = ("H4 libraries on 600 random connected G(n, p) graphs (n = 6..14, p = 0.2..0.5), %d ordered "
                        "pairs: c, the set of minimum cuts, the answer cp = c; mismatches: %d %s; pairs skipped because "
                        "cp_equals_c_paths hit its path budget: %d" % (tot, len(bad4), bad4[:2], len(budget4)))
            else:
                raise SystemExit("unknown part " + part)
            line += " (%.0f s)" % (time.time() - t0)
            with open(os.path.join(HERE, "results-compare-%s.txt" % part), "w") as fh:
                fh.write(line + "\n")
            print(line, flush=True)
    lines = ["compare_hardness.py (hardness/ imported read-only)"]
    for part in ("H1", "H2", "H3", "H4"):
        p = os.path.join(HERE, "results-compare-%s.txt" % part)
        if os.path.exists(p):
            with open(p) as fh:
                lines.append(fh.read().strip())
    with open(os.path.join(HERE, "results-compare.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
