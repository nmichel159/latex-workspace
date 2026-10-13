"""Graph form of a ZZ + P2 instance (theory-dc.md Theorem 13(b)) and the round trip of Theorem 13(a), using the
independent implementation of agent verify-equivalence (verify/equivalence/eqcore.py, zzgen.py; imported read-only,
run with PYTHONDONTWRITEBYTECODE=1 so that nothing is written there).

For the instance in FILE.json: build G(Pi), check that it is simple, d(u,v) = 2, c(u,v) = N, G(Pi) in DC;
exact PIMC on G(Pi) by the prefix search of eqcore (independent of ZZ); then the pipeline G(Pi) -> H -> ZZ' and a
comparison of ZZ' with the input (same Q, preorder and R), and PC on ZZ' (verify_pcfp.pc).
Usage: python realise_check.py FILE.json"""
import os
import sys
import json
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "verify", "equivalence"))
import verify_pcfp  # noqa: E402
from eqcore import realise, Flow, adj_masks, bfs_dist, in_class_flow, pimc_flow_dfs  # noqa: E402
from zzgen import pipeline_flow  # noqa: E402

if __name__ == "__main__":
    n, le, R, u, v = verify_pcfp.load(sys.argv[1])
    assert u == 0 and v == n - 1
    down = [sum(1 << x for x in range(n) if le[x][y]) for y in range(n)]
    t0 = time.time()
    N_, edges, N, info = realise(n, down, R, u, v, M=1)
    print("G(Pi): vertices", N_, "edges", len(edges), "comparable pairs N", N, "equivalent pairs", len(info["eqv"]),
          flush=True)
    assert len(set(edges)) == len(edges) and all(a != b for a, b in edges)
    adj = adj_masks(N_, edges)
    print("d(u,v) =", bfs_dist(adj, u)[v], flush=True)
    F = Flow(N_, edges)
    c = F.conn(u, v)
    print("c(u,v) =", c, "(N =", N, ")", flush=True)
    print("in DC:", in_class_flow(N_, edges, 2), "%.0fs" % (time.time() - t0), flush=True)
    try:
        ans, path, nodes = pimc_flow_dfs(N_, edges, u, v, c=c, node_limit=2 * 10 ** 6)
        print("PIMC on G(Pi) by prefix search:", ans, "nodes", nodes, "%.0fs" % (time.time() - t0), flush=True)
    except RuntimeError:
        print("PIMC prefix search: node limit", flush=True)
    res = pipeline_flow(N_, edges, u, v, qmax=n)
    if res is None:
        print("pipeline skipped")
        sys.exit()
    same_Q = sorted(res["Q"]) == list(range(n))
    print("pipeline: q", res["q"], "c_H", res["cH"], "answer", res["ans"], res["ans2"], "same Q", same_Q, flush=True)
    if same_Q:
        # res["Q"][i] is the graph vertex of element i of ZZ'
        pos = {x: i for i, x in enumerate(res["Q"])}
        dn = res["down"]
        le2 = [[bool((dn[pos[y]] >> pos[x]) & 1) for y in range(n)] for x in range(n)]
        R2 = {(min(res["Q"][a], res["Q"][b]), max(res["Q"][a], res["Q"][b])) for a, b in res["R"]}
        print("same preorder:", le2 == le, "same R:", R2 == {(min(a, b), max(a, b)) for a, b in R}, flush=True)
        lt2, E2 = verify_pcfp.check_instance(n, le2, list(R2), u, v)
        L = n if n % 2 else n - 1
        print("PC of the recovered instance, L = %d:" % L, verify_pcfp.pc(le2, E2, u, v, L)[0],
              "%.0fs" % (time.time() - t0), flush=True)
