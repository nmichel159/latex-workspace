"""Round trip G -> ZZ (Theorem 13(a)) -> G(Pi) (Theorem 13(b)) on random DC graphs with 9..16 vertices.
For every pair with d = 2, c >= 3: build H and the ZZ instance (small engine), check P2, realise it with
M = N + 1 (as stated) and with M = 1 (remark), check DC, d = 2, c = N, and compare PIMC of G(Pi)
(independent prefix search) with PIMC of G.
Usage: python run_roundtrip.py SEED COUNT [workers]"""
import sys, time, random
from collections import Counter
from multiprocessing import Pool
from eqcore import (Small, Flow, adj_masks, all_dist, bfs_dist, build_H, H_weights, preorder_from_cuts, leq,
                    lt, check_P2, pimc_from_cuts, realise, in_class_flow, pimc_flow_dfs, in_class_small, bridges)
from randgraphs import gen_core_ears, gen_planted


def work(seed):
    rng = random.Random(seed)
    st = Counter()
    viol = []
    g = None
    for _ in range(50):
        g = gen_core_ears(rng, k=2) if rng.random() < 0.4 else gen_planted(rng, k=2)
        if g is not None:
            break
    if g is None:
        return st, viol
    n, edges = g[0], g[1]
    if bridges(n, edges):
        return st, viol  # Lemma 1 is checked elsewhere; here G itself must be 2-edge-connected
    adj = adj_masks(n, edges)
    sm = Small(n, [(a, b, 1) for a, b in edges])
    dist = all_dist(adj)
    if not in_class_small(sm, dist, n, 2):
        return st, viol
    st["graphs"] += 1
    for u in range(n):
        for v in range(u + 1, n):
            if dist[u][v] != 2 or sm.conn(u, v) < 3:
                continue
            c, cuts = sm.min_cuts(u, v)
            ansG, _ = pimc_from_cuts(adj, cuts, u, v)
            H = build_H(n, edges, adj, u, lambda x: sm.conn(u, x))
            Q, qi = H["Q"], H["qi"]
            q = len(Q)
            W = H_weights(q, H["real"], H["earE"])
            smH = Small(q, [(a, b, w) for (a, b), w in W.items()])
            cH, cutsH = smH.min_cuts(qi[u], qi[v])
            down = preorder_from_cuts(q, cutsH)
            R = [(a, b) for a, b in H["real"] if not (leq(down, a, b) and leq(down, b, a))]
            if check_P2(q, down, adj_masks(q, R)):
                viol.append((seed, u, v, "P2 fails"))
                continue
            N = sum(1 for a in range(q) for b in range(q) if a != b and lt(down, a, b))
            if q > 10 or N > 40:
                st["skipped (instance too large to realise)"] += 1
                continue
            st["pairs realised"] += 1
            st["pairs realised, PIMC yes" if ansG else "pairs realised, PIMC no"] += 1
            for M in (None, 1):
                n2, e2, N2, info = realise(q, down, R, qi[u], qi[v], M=M)
                tag = (seed, u, v, "M=%s" % M)
                F = Flow(n2, e2)
                c2 = F.conn(qi[u], qi[v])
                if c2 != N2:
                    viol.append(tag + ("c(G(Pi)) != N", c2, N2))
                if bfs_dist(adj_masks(n2, e2), qi[u])[qi[v]] != 2:
                    viol.append(tag + ("d != 2",))
                if not in_class_flow(n2, e2, 2):
                    viol.append(tag + ("G(Pi) not in DC",))
                try:
                    pans, _, nodes = pimc_flow_dfs(n2, e2, qi[u], qi[v], c=c2, node_limit=100000)
                    if pans != ansG:
                        viol.append(tag + ("PIMC(G(Pi)) != PIMC(G)", pans, ansG))
                except RuntimeError:
                    st["node limit"] += 1
                st["max n of G(Pi), M=%s" % M] = max(st["max n of G(Pi), M=%s" % M], n2)
    return st, viol


if __name__ == "__main__":
    seed = int(sys.argv[1])
    count = int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    t0 = time.time()
    total = Counter()
    mx = Counter()
    viol = []
    with Pool(workers) as pool:
        for st, vi in pool.imap_unordered(work, [seed * 10 ** 7 + i for i in range(count)], chunksize=2):
            for key, val in st.items():
                if key.startswith("max"):
                    mx[key] = max(mx[key], val)
                else:
                    total[key] += val
            viol.extend(vi)
    print("round trip seed", seed, "count", count)
    for key in sorted(total):
        print("%-45s %d" % (key, total[key]))
    for key in sorted(mx):
        print("%-45s %d" % (key, mx[key]))
    print("violations:", len(viol))
    for x in viol[:30]:
        print("  ", x)
    print("time %.1fs" % (time.time() - t0))
