"""Test of the claim of theory-hardness.md, Section 5 (table) and Corollary 1.4:
  graphs with c(x,y) <= 3 for all pairs: [cp(u,v) = c(u,v)] is decided by testing the u-v paths of odd length <= c(u,v)
  (lengths 1 and 3) with one max flow each: P qualifies iff lambda(even(P), odd(P)) = c(u,v)  (Lemma 1.3 (b)).
Also the general procedure of Corollary 1.4 (all odd lengths <= c) on unrestricted random graphs, and Lemma 1.3
(a) <=> (b) <=> (c) for every u-v path of odd length <= c.

Ground truth: all minimum cuts (residual closure; also all vertex sets when n <= 16) with the cut-graph test, and
the definition-based search cp_eq_c_bb2.

Graph sources:
  A  all connected graphs with 2..7 vertices whose pairs all have c <= 3 (networkx atlas)
  B  random connected subcubic graphs, 8..22 vertices
  C  random connected graphs with c(x,y) <= 3 for all pairs, grown edge by edge to maximality (8..16 vertices)
  D  wheels and fans with 4..14 rim vertices, and wheels with extra rim chords kept inside the class
  E  unrestricted random connected graphs G(n, p), n = 8..11, p = 0.25..0.5 (general procedure of Corollary 1.4 and
     Lemma 1.3); a pair with more than PATH_CAP u-v paths of length <= c is skipped and counted ("skipped")
Output: results-c3.txt
"""

import os
import random
import sys
import time
from multiprocessing import Pool

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vlib  # noqa: E402

PATH_CAP = 4000


def procedure(g, Gx, u, v, c):
    """Corollary 1.4: some u-v path of odd length <= c with lambda(even, odd) = c."""
    for p in nx.all_simple_paths(Gx, u, v, cutoff=c):
        l = len(p) - 1
        if l % 2 == 0:
            continue
        ev, od = p[0::2], p[1::2]
        if vlib.flow_value(g, ev, od) == c:
            return True, p
    return False, None


def maxc(g):
    C = vlib.all_pairs_c(g)
    return int(C.max())


def check_graph(job):
    n, edges, tag, mode, maxpairs, seed = job
    g = vlib.Gr(n, edges)
    Gx = nx.Graph()
    Gx.add_nodes_from(range(n))
    Gx.add_edges_from(edges)
    fails = []
    st = dict(pairs=0, yes=0, d2=0, d2yes=0, paths13=0, skipped=0)
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
    rng = random.Random(seed)
    if len(pairs) > maxpairs:
        pairs = rng.sample(pairs, maxpairs)
    if mode == "c3":
        mc = maxc(g)
        if mc > 3:
            return tag, st, [("not-in-class", tag, edges, mc)]
    for u, v in pairs:
        c = vlib.flow_value(g, [u], [v])
        if mode == "any":
            # unrestricted graphs: skip (and count) a pair with more than PATH_CAP paths of length <= c
            cnt = 0
            for _ in nx.all_simple_paths(Gx, u, v, cutoff=c):
                cnt += 1
                if cnt > PATH_CAP:
                    break
            if cnt > PATH_CAP:
                st["skipped"] += 1
                continue
        _, cuts = vlib.min_cuts_residual(g, u, v)
        truth = any(vlib.cut_graph_connects(g, A, u, v) for A in cuts)
        if n <= 16:
            cb, bc = vlib.min_cuts_brute(g, u, v)
            if cb != c or set(bc) != set(cuts):
                fails.append(("cuts", tag, edges, u, v))
        bb, _, _ = vlib.cp_eq_c_bb2(g, u, v, c)
        pr, path = procedure(g, Gx, u, v, c)
        st["pairs"] += 1
        st["yes"] += truth
        d = nx.shortest_path_length(Gx, u, v)
        if d == 2:
            st["d2"] += 1
            st["d2yes"] += truth
        if not (truth == bb == pr):
            fails.append(("answer", tag, edges, u, v, c, truth, bb, pr, path))
        # Lemma 1.3 on every odd path of length <= c
        eid = {e: i for i, e in enumerate(g.edges)}
        for p in nx.all_simple_paths(Gx, u, v, cutoff=c):
            l = len(p) - 1
            if l % 2 == 0:
                continue
            st["paths13"] += 1
            a = any(all((x in A) != (y in A) for x, y in zip(p, p[1:])) for A in cuts)
            b = vlib.flow_value(g, p[0::2], p[1::2]) == c
            rem = [eid[(min(x, y), max(x, y))] for x, y in zip(p, p[1:])]
            cc = vlib.flow_value(g, [u], [v], rem) == c - l
            if not (a == b == cc):
                fails.append(("lemma1.3", tag, edges, u, v, p, a, b, cc))
    return tag, st, fails


def subcubic(rng, n):
    while True:
        deg = [0] * n
        edges = set()
        order = list(range(n))
        rng.shuffle(order)
        for i in range(1, n):  # random tree with max degree 3
            cand = [x for x in order[:i] if deg[x] < 3]
            p = rng.choice(cand)
            edges.add((min(p, order[i]), max(p, order[i])))
            deg[p] += 1
            deg[order[i]] += 1
        tries = rng.randint(0, 2 * n)
        for _ in range(tries):
            a, b = rng.sample(range(n), 2)
            if deg[a] < 3 and deg[b] < 3 and (min(a, b), max(a, b)) not in edges:
                edges.add((min(a, b), max(a, b)))
                deg[a] += 1
                deg[b] += 1
        return sorted(edges)


def grow_c3(rng, n):
    T = nx.random_labeled_tree(n, seed=rng.randrange(10 ** 9)) if hasattr(nx, "random_labeled_tree") else nx.random_tree(n, seed=rng.randrange(10 ** 9))
    edges = set((min(a, b), max(a, b)) for a, b in T.edges())
    cand = [(a, b) for a in range(n) for b in range(a + 1, n) if (a, b) not in edges]
    rng.shuffle(cand)
    for e in cand:
        trial = sorted(edges | {e})
        if maxc(vlib.Gr(n, trial)) <= 3:
            edges.add(e)
    return sorted(edges)


def wheels(rng):
    out = []
    for k in range(4, 15):
        rim = [(i, (i + 1) % k) for i in range(k)]
        spokes = [(i, k) for i in range(k)]
        out.append((k + 1, rim + spokes, "wheel%d" % k))
        out.append((k + 1, rim[:-1] + spokes, "fan%d" % k))
        # wheel plus random chords kept in the class
        for t in range(3):
            edges = set((min(a, b), max(a, b)) for a, b in rim + spokes)
            ch = [(a, b) for a in range(k) for b in range(a + 2, k) if not (a == 0 and b == k - 1)]
            rng.shuffle(ch)
            for e in ch[:3]:
                trial = sorted(edges | {e})
                if maxc(vlib.Gr(k + 1, trial)) <= 3:
                    edges.add(e)
            out.append((k + 1, sorted(edges), "wheelchord%d_%d" % (k, t)))
    return out


def build_jobs():
    rng = random.Random(4242)
    jobs = []
    for i, G in enumerate(nx.graph_atlas_g()):
        if G.number_of_nodes() < 2 or not nx.is_connected(G):
            continue
        g = vlib.from_nx(G)
        if maxc(g) <= 3:
            jobs.append((g.n, g.edges, "A%d" % i, "c3", 10 ** 6, i))
    na = len(jobs)
    for i in range(300):
        n = rng.randint(8, 22)
        jobs.append((n, subcubic(rng, n), "B%d" % i, "c3", 60, i))
    for i in range(150):
        n = rng.randint(8, 16)
        jobs.append((n, grow_c3(rng, n), "C%d" % i, "c3", 80, i))
    for n, e, tag in wheels(rng):
        jobs.append((n, e, "D" + tag, "c3", 80, 0))
    nc3 = len(jobs)
    for i in range(200):
        n = rng.randint(8, 11)
        while True:
            G = nx.gnp_random_graph(n, rng.uniform(0.25, 0.5), seed=rng.randrange(10 ** 9))
            if nx.is_connected(G):
                break
        jobs.append((n, list(G.edges()), "E%d" % i, "any", 30, i))
    return jobs, na, nc3


def main():
    t0 = time.time()
    jobs, na, nc3 = build_jobs()
    tot = {}
    tot_c3 = dict(pairs=0, yes=0, d2=0, d2yes=0, paths13=0, skipped=0)
    tot_any = dict(pairs=0, yes=0, d2=0, d2yes=0, paths13=0, skipped=0)
    allf = []
    with Pool(int(os.environ.get("NPROC", "30"))) as pool:
        for tag, st, fl in pool.imap_unordered(check_graph, jobs, chunksize=2):
            tgt = tot_any if tag.startswith("E") else tot_c3
            for k in st:
                tgt[k] += st[k]
            allf += fl
    lines = ["check_c3.py: %d atlas graphs in the class, %d other graphs in the class (B subcubic, C grown, D wheels), "
             "%d unrestricted random graphs (E)" % (na, nc3 - na, len(jobs) - nc3),
             "class c(x,y) <= 3: " + repr(tot_c3),
             "unrestricted: " + repr(tot_any),
             "failures: %d" % len(allf)]
    allf.sort(key=lambda f: len(f[2]) if len(f) > 2 and isinstance(f[2], list) else 0)
    lines += [repr(f) for f in allf[:20]]
    lines.append("time %.0f s" % (time.time() - t0))
    with open(os.path.join(HERE, "results-c3.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
