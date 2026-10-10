"""Brute-force checks of Section 3 on the executable model of Algorithm 1 (reduction.py).

For a 3-SAT formula the script builds the graph G and checks, on the graph itself:

  structure   Definitions 3.2-3.3 (chain, threads), the degree facts used in the proofs, the counts
              of the running-time paragraph (links, threads, connecting paths, Lambda, |E|)
  Lemma 3.5   the shortest u-v paths are exactly the chain paths
  Lemma 3.6   a chain path hits all synchronization threads iff it is consistent
  Lemma 3.7   a consistent chain path hits all clause threads iff its assignment satisfies the formula
  Lemma 3.8   the consistent chain path of a satisfying assignment is separating; items (a), (b)
              and Table 1 of its proof
  Theorem 3.9 G has a separating shortest u-v path iff the formula is satisfiable

A chain path that shares no edge with some thread is not separating, because the thread is a u-v
path of G that avoids it; this is the only fact used to skip a connectivity test.

Run:  python check_reduction.py            (all families, about fifteen minutes)
      python check_reduction.py --quick    (small families only, under a minute)
"""

import itertools
import random
import sys
import time

import networkx as nx

from reduction import Reduction, edge, satisfiable, satisfies


class Failure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


# -- structure ------------------------------------------------------------------------------------

def check_structure(R):
    n, m, u, v = R.n, R.m, R.u, R.v
    r = len(R.links)
    require(r == 2 * n + 3 * m, "number of chain links")
    require(len(R.threads) == 2 * n + 7 * m, "number of threads")
    require(sum(len(t.connecting) for t in R.threads) == 6 * n + 28 * m, "number of connecting paths")
    require(len(R.crossing) == 4 * n + 21 * m, "number of crossing edges")
    require(all(1 <= len(t.crossings) <= 3 and len(t.connecting) <= 4 for t in R.threads),
            "at most three crossing edges and four connecting paths per thread")
    require(all(len(t.crossings) >= 2 for t in R.threads), "every thread has at least two crossing edges")

    # Definition 3.2: equal path lengths in every link; consecutive parts share exactly one vertex
    for link in R.links:
        require(len(link.paths["+"]) == len(link.paths["-"]), "the two paths of a chain link differ in length")
        inner_plus, inner_minus = set(link.paths["+"][1:-1]), set(link.paths["-"][1:-1])
        require(not inner_plus & inner_minus, "the two paths of a chain link share an inner vertex")
    link_vertices = [set(link.paths["+"]) | set(link.paths["-"]) for link in R.links]
    for a in range(r):
        for b in range(a + 1, r):
            require(not link_vertices[a] & link_vertices[b], "two chain links share a vertex")
    require(R.singles[0] == edge(u, R.links[0].q) and R.singles[-1] == edge(R.links[-1].p, v), "ends of the chain")
    for i in range(1, r):
        require(R.singles[i] == edge(R.links[i - 1].p, R.links[i].q), "single edge between consecutive links")
    require(all(u not in s and v not in s for s in link_vertices), "u or v lies on a chain link")

    # the blocks are consecutive: I_i, the literal links of x_i, T_i
    for i, idxs in R.block.items():
        require(idxs == list(range(idxs[0], idxs[-1] + 1)), "block is not consecutive")
        require(R.links[idxs[0]].label == ("I", i) and R.links[idxs[-1]].label == ("T", i), "block ends")
        require(all(R.links[idx].label[0] == "L" for idx in idxs[1:-1]), "block interior")
        require(len(idxs) == 2 + len(R.M[i]), "block size")

    # Definition 3.3: threads are u-v paths; at most one edge in each link; no single edge;
    # pairwise edge-disjoint; any two share only u and v; a thread meets the chain in its crossing edges
    chain = R.chain_edges()
    link_edges = [set(link.path_edges("+")) | set(link.path_edges("-")) for link in R.links]
    thread_edges, thread_vertices = [], []
    for t in R.threads:
        seq = t.vertex_sequence()
        require(seq[0] == u and seq[-1] == v and len(set(seq)) == len(seq), "a thread is not a u-v path")
        edges = set(t.edges())
        require(edges == {edge(seq[i], seq[i + 1]) for i in range(len(seq) - 1)}, "thread edge set")
        require(all(b in R.adj[a] for a, b in edges), "thread edge missing in G")
        require(all(len(edges & le) <= 1 for le in link_edges), "a thread shares two edges with a link")
        require(not edges & set(R.singles), "a thread contains a single edge of the chain")
        require(edges & chain == set(t.crossing_edges()), "a thread meets the chain outside its crossing edges")
        thread_edges.append(edges)
        thread_vertices.append(set(seq))
    for a in range(len(R.threads)):
        for b in range(a + 1, len(R.threads)):
            require(not thread_edges[a] & thread_edges[b], "two threads share an edge")
            require(thread_vertices[a] & thread_vertices[b] == {u, v}, "two threads share a vertex other than u, v")
    require(chain | set().union(*thread_edges) == R.all_edges(), "an edge outside the chain and the threads")

    # threads follow their specification: crossing edge r lies on the path of K_r with the sign s_r
    for t in R.threads:
        require([R.crossing_location(c) for c in t.crossing_edges()] == list(t.spec), "thread specification")

    # degrees: inner vertices of connecting paths 2; ends of crossing edges 3 (two chain-link edges,
    # one connecting-path edge); every vertex other than u, v at most 3
    for t in R.threads:
        for path in t.connecting:
            require(all(len(R.adj[w]) == 2 for w in path[1:-1]), "inner vertex of a connecting path")
            if R.Lambda is not None and R.lengthen:
                require(len(path) - 1 == R.Lambda, "a connecting path does not have Lambda edges")
        for a, b in t.crossings:
            require(len(R.adj[a]) == 3 and len(R.adj[b]) == 3, "end of a crossing edge")
    require(all(len(R.adj[w]) <= 3 for w in R.adj if w not in (u, v)), "a vertex other than u, v of degree > 3")

    # counts of the running-time paragraph, as exact formulas
    require(R.Lambda == 10 * n + 33 * m + 1, "Lambda != 10n + 33m + 1")
    require(len(chain) == 18 * n + 63 * m + 1, "chain edges != 18n + 63m + 1")
    require(R.balancing_added == 6 * m, "balancing adds two edges per literal link")
    if R.lengthen:
        require(len(R.all_edges()) == len(chain) + (6 * n + 28 * m) * R.Lambda, "|E|")
    return True


# -- Lemma 3.5 ------------------------------------------------------------------------------------

def check_shortest_paths(R, enumerate_paths=False):
    """d(u,v) = Lambda and no shortest u-v path uses an edge outside the chain."""
    du, dv = R.bfs(R.u), R.bfs(R.v)
    require(du[R.v] == R.Lambda, "d(u,v) != Lambda")
    chain = R.chain_edges()
    for a, b in R.all_edges() - chain:
        require(min(du[a] + 1 + dv[b], du[b] + 1 + dv[a]) > R.Lambda,
                "an edge outside the chain lies on a u-v path with at most Lambda edges")
    signs_all = list(itertools.product("+-", repeat=len(R.links))) if len(R.links) <= 12 else []
    for signs in signs_all:
        require(len(R.chain_path(signs)) == R.Lambda, "a chain path does not have Lambda edges")
    if enumerate_paths:
        # independent enumeration of all shortest u-v paths of G
        G = nx.Graph(list(R.all_edges()))
        found = {frozenset(edge(p[i], p[i + 1]) for i in range(len(p) - 1))
                 for p in nx.all_shortest_paths(G, R.u, R.v)}
        expected = {frozenset(R.chain_path(signs)) for signs in signs_all}
        require(found == expected, "shortest u-v paths are not exactly the chain paths")
        # every u-v path inside the chain is a chain path (sentence after Definition 3.2)
        H = nx.Graph(list(chain))
        inside = {frozenset(edge(p[i], p[i + 1]) for i in range(len(p) - 1))
                  for p in nx.all_simple_paths(H, R.u, R.v)}
        require(inside == expected, "u-v paths of the chain are not exactly the chain paths")
    return True


# -- Lemmas 3.6-3.8, Theorem 3.9 ------------------------------------------------------------------

def thread_masks(R):
    """For each thread, the (link, sign) pairs of its crossing edges, located on the graph.

    A thread meets the chain only in its crossing edges (check_structure), so a chain path hits the
    thread iff it traverses the path that carries one of these edges.
    """
    return [[R.crossing_location(c) for c in t.crossing_edges()] for t in R.threads]


def check_hitting(R):
    """Lemmas 3.6 and 3.7 over all chain paths; returns the sign vectors that hit every thread."""
    r = len(R.links)
    locations = thread_masks(R)
    sync = [loc for t, loc in zip(R.threads, locations) if t.kind != "clause"]
    clause = [loc for t, loc in zip(R.threads, locations) if t.kind == "clause"]
    hit_all = []
    for signs in itertools.product("+-", repeat=r):
        hits_sync = all(any(signs[idx] == s for idx, s in loc) for loc in sync)
        consistent = all(len({signs[idx] for idx in idxs}) == 1 for idxs in R.block.values())
        require(hits_sync == consistent, "Lemma 3.6 fails for %s" % "".join(signs))
        if consistent:
            tau = {i: signs[idxs[0]] == "+" for i, idxs in R.block.items()}
            hits_clause = all(any(signs[idx] == s for idx, s in loc) for loc in clause)
            require(hits_clause == satisfies(tau, R.clauses), "Lemma 3.7 fails for %s" % "".join(signs))
            if hits_clause:
                hit_all.append(signs)
    return hit_all


def candidates_by_blocks(R):
    """All sign vectors that hit every thread, found block by block (exhaustive, for long chains).

    A synchronization thread of x_i has crossing edges only in the block of x_i, so the sign
    vectors that hit all synchronization threads are the products of the admissible sign vectors of
    the blocks; the clause threads are tested on every product.
    """
    locations = thread_masks(R)
    per_block = []
    for i, idxs in R.block.items():
        own = [loc for t, loc in zip(R.threads, locations) if t.kind != "clause" and t.owner == i]
        require(all(idx in idxs for loc in own for idx, _ in loc), "a synchronization thread leaves its block")
        good = []
        for part in itertools.product("+-", repeat=len(idxs)):
            local = dict(zip(idxs, part))
            if all(any(local[idx] == s for idx, s in loc) for loc in own):
                good.append(local)
        require(len(good) == 2 and all(len(set(g.values())) == 1 for g in good),
                "a block admits a sign vector that is not constant")
        per_block.append(good)
    clause = [loc for t, loc in zip(R.threads, locations) if t.kind == "clause"]
    result = []
    for combo in itertools.product(*per_block):
        signs = [""] * len(R.links)
        for local in combo:
            for idx, s in local.items():
                signs[idx] = s
        if all(any(signs[idx] == s for idx, s in loc) for loc in clause):
            result.append(tuple(signs))
    return result


def check_separation_details(R, tau):
    """Items (a), (b) and Table 1 of the proof of Lemma 3.8 for a satisfying assignment tau."""
    signs = R.consistent_signs(tau)
    P = R.chain_path(signs)
    removed = frozenset(P)
    open_edge = {}
    for t in R.threads:
        for c in t.crossing_edges():
            idx, sign = R.crossing_location(c)
            is_open = c not in P
            open_edge[c] = is_open
            label = R.links[idx].label
            var = label[1] if label[0] in "IT" else abs(R.clauses[label[2] - 1][label[1] - 1])
            # (a) open iff its sign differs from the sign of the paths that P traverses in the block
            require(is_open == (sign != ("+" if tau[var] else "-")), "item (a)")
            if not is_open:
                for w in c:
                    degree = sum(1 for x in R.adj[w] if edge(w, x) not in removed)
                    require(degree == 1, "end of a closed crossing edge has degree != 1 in G - P")
    for t in R.threads:
        cs = t.crossing_edges()
        usable = []
        for r in range(len(t.connecting)):
            left = True if r == 0 else open_edge[cs[r - 1]]
            right = True if r == len(cs) else open_edge[cs[r]]
            usable.append(left and right)
        if t.kind == "clause":
            false = [tau[abs(lit)] != (lit > 0) for lit in R.clauses[t.owner - 1]]
            # (b) the crossing edge in L_{j,k} is open iff tau does not satisfy the j-th literal
            require([open_edge[c] for c in cs] == false, "item (b)")
            expected = [false[0], false[0] and false[1], false[1] and false[2], false[2]]
            require(usable == expected, "Table 1, clause thread")
        else:
            require(not any(usable[1:-1]), "Table 1: inner connecting path of a synchronization thread usable")
            require(usable[0] == open_edge[cs[0]] and usable[-1] == open_edge[cs[-1]], "Table 1, first/last path")
    return True


def check_formula(n, clauses, seed=0, choice="random", exhaustive=None, enumerate_paths=False):
    """All checks for one formula. Returns (satisfiable, number of separating shortest paths)."""
    R = Reduction(n, clauses, choice=choice, seed=seed)
    check_structure(R)
    check_shortest_paths(R, enumerate_paths=enumerate_paths)
    r = len(R.links)
    if exhaustive is None:
        exhaustive = r <= 15
    candidates = check_hitting(R) if exhaustive else candidates_by_blocks(R)
    if exhaustive:
        require(sorted(candidates) == sorted(candidates_by_blocks(R)), "block search differs from full search")
    # the short graph: same construction, connecting paths of one edge (same seed, same choices)
    S = Reduction(n, clauses, choice=choice, seed=seed, lengthen=False)
    require([t.crossings for t in S.threads] == [t.crossings for t in R.threads], "short graph differs")
    separating = 0
    for signs in candidates:
        tau = {i: signs[idxs[0]] == "+" for i, idxs in R.block.items()}
        require(satisfies(tau, R.clauses), "a chain path that hits all threads is not satisfying")
        check_separation_details(R, tau)
        sep_long = R.separates(R.chain_path(signs))
        require(sep_long == S.separates(S.chain_path(signs)), "long and short graph disagree")
        require(sep_long, "Lemma 3.8 fails: the chain path of a satisfying assignment is not separating")
        separating += 1
    if exhaustive and r <= 12:
        # connectivity test for every chain path, also for those that miss a thread
        hit_set = set(candidates)
        for signs in itertools.product("+-", repeat=r):
            require(S.separates(S.chain_path(signs)) == (signs in hit_set),
                    "a chain path that misses a thread is separating, or the converse")
    sat = satisfiable(n, clauses)
    require((separating > 0) == sat, "Theorem 3.9 fails")
    n_sat = sum(satisfies({i: bool(b >> (i - 1) & 1) for i in range(1, n + 1)}, clauses) for b in range(2 ** n))
    require(separating == n_sat, "separating shortest paths != satisfying assignments")
    return sat, separating


# -- families of formulas -------------------------------------------------------------------------

def all_clauses(n, distinct):
    variables = range(1, n + 1)
    triples = itertools.combinations(variables, 3) if distinct else itertools.product(variables, repeat=3)
    return [tuple(s * x for s, x in zip(signs, triple))
            for triple in triples for signs in itertools.product((1, -1), repeat=3)]


def random_formula(rng, n, m, distinct):
    clauses = []
    for _ in range(m):
        triple = rng.sample(range(1, n + 1), 3) if distinct else [rng.randint(1, n) for _ in range(3)]
        clauses.append(tuple(x if rng.random() < 0.5 else -x for x in triple))
    return clauses


def run(quick=False):
    rng = random.Random(20261010)
    total = {"formulas": 0, "sat": 0, "unsat": 0}
    started = time.time()

    def do(name, formulas, **kwargs):
        count = sat_count = 0
        for n, clauses, seed in formulas:
            sat, _ = check_formula(n, clauses, seed=seed, **kwargs)
            count += 1
            sat_count += sat
        total["formulas"] += count
        total["sat"] += sat_count
        total["unsat"] += count - sat_count
        print("%-58s %6d formulas  %6d sat  %6d unsat  [%.0f s]"
              % (name, count, sat_count, count - sat_count, time.time() - started), flush=True)

    # one variable, repeated in a clause: the smallest unsatisfiable formulas
    c1 = all_clauses(1, distinct=False)
    do("n=1, m=1..2, all formulas, shortest paths enumerated",
       [(1, list(f), s) for m in (1, 2) for f in itertools.product(c1, repeat=m) for s in (0, 1)],
       enumerate_paths=True)
    # two variables, repetitions allowed
    c2 = all_clauses(2, distinct=False)
    do("n=2, m=1, all formulas, shortest paths enumerated", [(2, [c], s) for c in c2 for s in (0, 1)],
       enumerate_paths=True)
    # three variables, three distinct variables per clause
    c3 = all_clauses(3, distinct=True)
    do("n=3, m=1, distinct variables, shortest paths enumerated", [(3, [c], s) for c in c3 for s in (0, 1, 2)],
       enumerate_paths=True)
    do("n=3, m=8, all eight sign patterns (unsatisfiable)", [(3, c3, s) for s in range(3)])
    do("n=3, m=7, seven of the eight sign patterns",
       [(3, [c for c in c3 if c != skip], 0) for skip in c3])
    if not quick:
        do("n=1, m=3, all formulas", [(1, list(f), 0) for f in itertools.product(c1, repeat=3)])
        do("n=2, m=2, all formulas", [(2, list(f), 0) for f in itertools.product(c2, repeat=2)])
        do("n=3, m=2, distinct variables, all formulas", [(3, list(f), 0) for f in itertools.product(c3, repeat=2)])
        do("n=3, m=3, distinct variables, all multisets of clauses",
           [(3, list(f), 0) for f in itertools.combinations_with_replacement(c3, 3)])
        do("n=2, m=3, 300 random formulas", [(2, [rng.choice(c2) for _ in range(3)], rng.randrange(10 ** 6))
                                              for _ in range(300)])
        do("n=4, m=1..3, distinct variables, 150 random formulas",
           [(4, random_formula(rng, 4, rng.randint(1, 3), True), rng.randrange(10 ** 6)) for _ in range(150)])
        do("n=3..6, m=4..14, repetitions allowed, 80 random formulas",
           [(n, random_formula(rng, n, rng.randint(4, 14), False), rng.randrange(10 ** 6))
            for n in (rng.randint(3, 6) for _ in range(80))], exhaustive=False)
        do("n=3, m=13..18, distinct variables, 10 random formulas",
           [(3, random_formula(rng, 3, rng.randint(13, 18), True), rng.randrange(10 ** 6))
            for _ in range(10)], exhaustive=False)
    print("total: %(formulas)d formulas, %(sat)d satisfiable, %(unsat)d unsatisfiable; no check failed" % total)


if __name__ == "__main__":
    try:
        run(quick="--quick" in sys.argv)
    except Failure as failure:
        print("CHECK FAILED:", failure)
        sys.exit(1)
