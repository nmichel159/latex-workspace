"""Theorem 13(b) of theory-dc.md: random ZZ instances (P2 enforced, or not), realised as simple graphs G(Pi).
Checks: simple graph, size, d(u,v) = 2, c(u,v) = N, membership in DC (P2 instances), the cut formula of W on
every subset of Q, minimum cuts = down-sets, PIMC on G(Pi) by the independent prefix search = ZZ answer,
and the composition G(Pi) -> H -> ZZ' (Theorem 13(a) pipeline) gives the same answer.
Usage: python run_realise.py MODE SEED COUNT [workers]   (MODE = p2 | nop2)"""
import sys, time, random
from collections import Counter
from multiprocessing import Pool
from eqcore import (Small, Flow, adj_masks, all_dist, bfs_dist, bit_list, leq, lt, is_downset, realise, check_P2,
                    W_of_realisation, in_class_flow, pimc_flow_dfs, popcount)
from zzgen import random_preorder, random_R, enforce_P2, zz_answer, strict_pairs, pipeline_flow


def plant(q, down, R, rng, u=0, v=None):
    """Add R-edges along a random alternating path across a random down-set (a consistent zigzag)."""
    v = q - 1 if v is None else v
    for _ in range(20):
        D = 1 << u
        for x in range(q):
            if x not in (u, v) and rng.random() < 0.5:
                D |= down[x]
        if (D >> v) & 1:
            continue
        path = [u]
        used = {u}
        cur = u
        while True:
            peaks = [b for b in range(q) if not (D >> b) & 1 and b not in used and lt(down, cur, b)]
            if not peaks:
                break
            if v in peaks and (rng.random() < 0.35 or len(peaks) == 1):
                b = v
            else:
                b = rng.choice([p for p in peaks if p != v])
            path.append(b)
            used.add(b)
            if b == v:
                break
            vals = [a for a in range(q) if (D >> a) & 1 and a not in used and lt(down, a, b)]
            if not vals:
                break
            a = rng.choice(vals)
            path.append(a)
            used.add(a)
            cur = a
        if path[-1] == v and len(path) >= 4:
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                R.add((min(a, b), max(a, b)))
            return True
    return False


def work(args):
    mode, seed = args
    rng = random.Random(seed)
    st = Counter()
    viol = []
    for _ in range(100):
        q = rng.randint(4, 8)
        down = random_preorder(q, rng)
        N = len(strict_pairs(q, down))
        if N < 3:
            continue
        R = random_R(q, down, rng)
        planted = rng.random() < 0.5
        if planted:
            plant(q, down, R, rng)
        if mode == "p2":
            enforce_P2(q, down, R, rng)
        break
    else:
        return st, viol
    u, v = 0, q - 1
    ans, zpath = zz_answer(q, down, R)
    n, edges, N, info = realise(q, down, R, u, v)
    st["instances"] += 1
    st["planted" if planted else "random"] += 1
    st["ZZ yes" if ans else "ZZ no"] += 1
    if ans:
        st["zigzag length %d" % (len(zpath) - 1)] += 1
    st["max n of G(Pi)"] = n
    tag = (mode, seed, q, tuple(down), tuple(sorted(R)))
    if len(set(edges)) != len(edges) or any(a == b for a, b in edges):
        viol.append(tag + ("not simple",))
    eqv = info["eqv"]
    expect_n = q + sum(1 for a, b in info["pairs"] if (min(a, b), max(a, b)) not in R) \
        + sum(1 for a, b in info["pairs"] if a != u) + sum(1 for a, b in info["pairs"] if b != v) \
        + info["M"] * len(eqv)
    if expect_n != n:
        viol.append(tag + ("size formula", n, expect_n))
    adj = adj_masks(n, edges)
    if bfs_dist(adj, u)[v] != 2:
        viol.append(tag + ("d(u,v) != 2",))
    F = Flow(n, edges)
    c = F.conn(u, v)
    if c != N:
        viol.append(tag + ("c != N", c, N))
    if mode == "p2":
        if not in_class_flow(n, edges, 2):
            viol.append(tag + ("G(Pi) not in DC",))
    else:
        inDC = in_class_flow(n, edges, 2)
        hasP2 = not check_P2(q, down, adj_masks(q, R))
        st["nop2: G(Pi) in DC" if inDC else "nop2: G(Pi) not in DC"] += 1
        st["nop2: instance has P2" if hasP2 else "nop2: instance violates P2"] += 1
        if inDC != hasP2:
            viol.append(tag + ("G(Pi) in DC but P2 differs", inDC, hasP2))
    # cut function of W on all subsets of Q
    W, N2 = W_of_realisation(q, down, R, u, v, info["M"])
    sm = Small(q, [(a, b, w) for (a, b), w in W.items()])
    cW, cuts = sm.min_cuts(u, v)
    if cW != N:
        viol.append(tag + ("c_W != N",))
    ds = {D for D in range(1 << q) if (D >> u) & 1 and not (D >> v) & 1 and is_downset(down, D)}
    if set(cuts) != ds:
        viol.append(tag + ("minimum cuts of W != down-sets",))
    for A in range(1 << q):
        if not (A >> u) & 1 or (A >> v) & 1:
            continue
        splits = any(((A >> a) & 1) != ((A >> b) & 1) for a, b in eqv)
        if splits:
            if int(sm.cut[A]) <= N:
                viol.append(tag + ("class split with cut <= N", A))
            continue
        f = N + 2 * sum(1 for a, b in info["pairs"] if not (A >> a) & 1 and (A >> b) & 1)
        if int(sm.cut[A]) != f:
            viol.append(tag + ("cut formula", A, int(sm.cut[A]), f))
            break
    # independent PIMC on G(Pi)
    try:
        pans, ppath, nodes = pimc_flow_dfs(n, edges, u, v, c=c, node_limit=200000)
        st["prefix-search nodes max"] = max(st["prefix-search nodes max"], nodes)
        if pans != ans:
            viol.append(tag + ("PIMC(G(Pi)) != ZZ", pans, ans))
        if pans:
            if any(x >= q for x in ppath):
                viol.append(tag + ("witness path uses an ear vertex",))
    except RuntimeError:
        st["prefix-search node limit"] += 1
    # composition with Theorem 13(a)
    res = pipeline_flow(n, edges, u, v)
    if res is None:
        st["pipeline skipped (q too large)"] += 1
    else:
        if res["bad"]:
            viol.append(tag + ("pipeline: Lemma 4 bad", res["bad"][:2]))
        if not (res["ans"] == res["ans2"] == ans):
            viol.append(tag + ("pipeline answer differs", res["ans"], ans))
        if res["cH"] != N:
            viol.append(tag + ("pipeline c_H != N",))
        if res["P2fail"] and mode == "p2":
            viol.append(tag + ("pipeline: P2 fails on recovered instance",))
        sameQ = sorted(res["Q"]) == list(range(q))
        st["recovered Q = Q" if sameQ else "recovered Q != Q"] += 1
        if sameQ:
            same = all(res["down"][i] == down[i] for i in range(q))
            st["recovered preorder = preorder" if same else "recovered preorder differs"] += 1
            if not same:
                viol.append(tag + ("recovered preorder differs",))
            Rr = {(min(a, b), max(a, b)) for a, b in res["R"]}
            if Rr != {(min(a, b), max(a, b)) for a, b in R}:
                viol.append(tag + ("recovered R differs",))
    return st, viol


if __name__ == "__main__":
    mode = sys.argv[1]
    seed = int(sys.argv[2])
    count = int(sys.argv[3])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    t0 = time.time()
    total = Counter()
    viol = []
    mx = Counter()
    with Pool(workers) as pool:
        for st, vi in pool.imap_unordered(work, [(mode, seed * 10 ** 7 + i) for i in range(count)], chunksize=2):
            for key, val in st.items():
                if "max" in key:
                    mx[key] = max(mx[key], val)
                else:
                    total[key] += val
            viol.extend(vi)
    print("mode", mode, "seed", seed, "count", count)
    for key in sorted(total):
        print("%-45s %d" % (key, total[key]))
    for key in sorted(mx):
        print("%-45s %d" % (key, mx[key]))
    print("violations:", len(viol))
    for x in viol[:30]:
        print("  ", x)
    print("time %.1fs" % (time.time() - t0))
