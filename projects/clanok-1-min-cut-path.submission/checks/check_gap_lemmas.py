"""Checks of the two lemmas behind "no PTAS" (Section 7.1), on the executable model of Algorithm 1.

Notation: for a u-v path P of the graph G of the reduction, eta(P) is the number of threads that
share no edge with P; eta* is the minimum of eta(P) over the chain paths; Lambda is the number of
edges of a chain path.

  Lower bound      cp(u,v) >= Lambda + eta*; more precisely |P| + eta(P) >= Lambda + eta* for every
                   u-v path P of G, and |S| >= |P| + eta(P) for every cut-path S that contains P
  Charging         for every chain path P: (clauses not satisfied by the assignment read off the
                   initialization links) <= B * eta(P), B = the largest number of occurrences of a
                   variable
  Sizes            Lambda = 10n + 33m + 1 in general, 39m + 1 when every variable occurs five times

The graph is built with connecting paths of one edge (lengthen=False); such an edge stands for a
connecting path with Lambda edges and has length Lambda here. This changes neither the cuts nor,
with these lengths, the number of edges of a path.

cp(u,v) is computed exactly as the minimum of |P| + c_{G - P}(u,v) over the u-v paths P: over all
chain paths, and over all other paths by a depth-first search that drops a partial path once its
length reaches the best value found plus SLACK (a cut has at least 0 edges, so nothing is lost; the
slack only adds paths on which the inequality |P| + eta(P) >= Lambda + eta* is checked).

Run:  python check_gap_lemmas.py            (about 2 minutes)
      python check_gap_lemmas.py --long     (adds the unsatisfiable formula on two variables, r = 16)
"""

import itertools
import random
import sys
from collections import deque

from reduction import Reduction, edge


SLACK = 8  # the search also visits paths up to SLACK edges longer than the best value, for the inequality


class Failure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


class Model:
    def __init__(self, n, clauses, seed):
        self.n, self.clauses = n, [tuple(c) for c in clauses]
        self.red = red = Reduction(n, clauses, choice="random", seed=seed, lengthen=False)
        self.Lambda = red.Lambda
        self.u, self.v = red.u, red.v
        self.r = len(red.links)
        self.thread_edges = [frozenset(t.edges()) for t in red.threads]
        self.connecting = {}
        self.crossing = {}
        for index, t in enumerate(red.threads):
            for path in t.connecting:
                self.connecting[edge(path[0], path[1])] = index
            for e in t.crossing_edges():
                self.crossing[e] = index
        self.adj = {x: sorted(ys) for x, ys in red.adj.items()}
        self.B = max(1, max(len(lits) for lits in red.M.values()))

    def length(self, edges):
        return sum(self.Lambda if e in self.connecting else 1 for e in edges)

    def eta(self, edges):
        return sum(1 for te in self.thread_edges if not (te & edges))

    def eta_by_signs(self, signs):
        """eta of a chain path from the lists passed to Thread, without the graph."""
        return sum(1 for t in self.red.threads if not any(signs[idx] == s for idx, s in t.spec))

    def unsatisfied(self, signs):
        tau = {i: signs[self.red.I[i]] == "+" for i in range(1, self.n + 1)}
        return sum(1 for c in self.clauses if not any(tau[abs(lit)] == (lit > 0) for lit in c))

    def min_unsatisfied(self):
        best = len(self.clauses)
        for bits in range(2 ** self.n):
            tau = {i: bool(bits >> (i - 1) & 1) for i in range(1, self.n + 1)}
            best = min(best, sum(1 for c in self.clauses
                                 if not any(tau[abs(lit)] == (lit > 0) for lit in c)))
        return best

    def cut_value(self, removed):
        """Maximum number of edge-disjoint u-v paths in G minus `removed` (unit capacities)."""
        cap = {}
        for x, ys in self.adj.items():
            for y in ys:
                if edge(x, y) not in removed:
                    cap[(x, y)] = 1
        flow = 0
        while True:
            parent = {self.u: None}
            queue = deque([self.u])
            while queue and self.v not in parent:
                x = queue.popleft()
                for y in self.adj[x]:
                    if y not in parent and cap.get((x, y), 0) > 0:
                        parent[y] = x
                        queue.append(y)
            if self.v not in parent:
                return flow
            y = self.v
            while parent[y] is not None:
                x = parent[y]
                cap[(x, y)] -= 1
                cap[(y, x)] = cap.get((y, x), 0) + 1
                y = x
            flow += 1


def check_instance(n, clauses, seed, exact, all_one_connecting):
    model = Model(n, clauses, seed)
    red = model.red
    m = len(clauses)
    occurrences = [len(red.M[i]) for i in range(1, n + 1)]
    require(model.Lambda == 10 * n + 33 * m + 1, f"Lambda: {n}, {clauses}")
    if all(o == 5 for o in occurrences):
        require(model.Lambda == 39 * m + 1, f"Lambda with five occurrences: {n}, {clauses}")

    # chain paths: eta, eta*, charging
    eta_star = None
    chain = []
    exhaustive = model.r <= 16
    rng = random.Random(seed)
    sign_vectors = (itertools.product("+-", repeat=model.r) if exhaustive
                    else (tuple(rng.choice("+-") for _ in range(model.r)) for _ in range(20000)))
    for signs in sign_vectors:
        e = model.eta_by_signs(signs)
        require(model.unsatisfied(signs) <= model.B * e,
                f"charging: {n}, {clauses}, signs {''.join(signs)}")
        if exhaustive:
            chain.append((signs, e))
            eta_star = e if eta_star is None else min(eta_star, e)
    if not exhaustive:
        return {"charging_only": True}
    q = model.min_unsatisfied()
    require(model.B * eta_star >= q, f"eta* >= q / B: {n}, {clauses}")
    require((eta_star == 0) == (q == 0), f"eta* = 0 iff satisfiable: {n}, {clauses}")
    result = {"eta_star": eta_star, "q": q, "B": model.B, "Lambda": model.Lambda}
    if not exact:
        return result

    # exact cp: chain paths first
    best = None
    for signs, e in chain:
        path = frozenset(red.chain_path(signs))
        require(model.eta(path) == e, "eta of a chain path computed in two ways")
        require(model.length(path) == model.Lambda, "length of a chain path")
        if model.r > 13 and best is not None and model.Lambda + e >= best:
            continue  # long run only: the cut of G - P has at least eta(P) edges (checked when r <= 13)
        cut = model.cut_value(path)
        require(cut >= e, "cut of G - P below the number of missed threads")
        value = model.Lambda + cut
        best = value if best is None else min(best, value)

    # all other u-v paths, by depth-first search with the bound "length < best"
    counters = {"other_paths": 0, "one_connecting": 0}
    state = {"best": best}
    visited = {model.u}
    used = []

    def search(x, weight, connecting_count, bounded):
        if x == model.v:
            if connecting_count == 0:
                return
            path = frozenset(used)
            eta = model.eta(path)
            require(weight + eta >= model.Lambda + eta_star,
                    f"|P| + eta(P) >= Lambda + eta*: {n}, {clauses}, seed {seed}, path {sorted(path)}")
            counters["other_paths"] += 1
            if connecting_count == 1:
                counters["one_connecting"] += 1
            if weight < state["best"]:
                cut = model.cut_value(path)
                require(cut >= eta, "cut of G - P below the number of missed threads")
                state["best"] = min(state["best"], weight + cut)
            return
        for y in model.adj[x]:
            if y in visited:
                continue
            e = edge(x, y)
            is_connecting = e in model.connecting
            w = weight + (model.Lambda if is_connecting else 1)
            c = connecting_count + (1 if is_connecting else 0)
            if bounded and w >= state["best"] + SLACK:
                continue
            if not bounded and c > 1:
                continue
            visited.add(y)
            used.append(e)
            search(y, w, c, bounded)
            used.pop()
            visited.remove(y)

    sys.setrecursionlimit(100000)
    search(model.u, 0, 0, True)
    cp = state["best"]
    require(cp >= model.Lambda + eta_star, f"cp >= Lambda + eta*: {n}, {clauses}, seed {seed}")
    require((cp == model.Lambda) == (q == 0), f"cp = Lambda iff satisfiable: {n}, {clauses}")
    result["cp"] = cp
    result["bounded_paths"] = counters["other_paths"]

    if all_one_connecting:
        # every u-v path with exactly one connecting path, without the bound
        counters["other_paths"] = counters["one_connecting"] = 0
        state["best"] = -1  # no path is evaluated for its cut: only |P| + eta(P) is checked
        search(model.u, 0, 0, False)
        result["one_connecting"] = counters["one_connecting"]
    return result


def literals(n):
    return [s * i for i in range(1, n + 1) for s in (1, -1)]


def main():
    long_run = "--long" in sys.argv
    rng = random.Random(20261010)
    jobs = []  # (n, clauses, exact, all paths with one connecting path)

    # one variable: all formulas with one or two clauses (up to the order of the literals in a clause)
    one = sorted(set(tuple(sorted(c)) for c in itertools.product(literals(1), repeat=3)))
    for c in one:
        jobs.append((1, [c], True, True))
    for c1, c2 in itertools.combinations_with_replacement(one, 2):
        jobs.append((1, [c1, c2], True, True))
    # one variable, three clauses: the unsatisfiable ones and a few others
    jobs.append((1, [(1, 1, 1), (-1, -1, -1), (1, 1, -1)], True, False))
    jobs.append((1, [(1, 1, 1), (-1, -1, -1), (-1, -1, -1)], True, False))
    jobs.append((1, [(1, 1, 1), (1, 1, 1), (1, 1, 1)], True, False))
    # two variables
    two = list(itertools.product(literals(2), repeat=3))
    for _ in range(8):
        jobs.append((2, [rng.choice(two)], True, True))
    for _ in range(8):
        jobs.append((2, [rng.choice(two), rng.choice(two)], True, False))
    jobs.append((2, [(1, 1, 1), (-1, -1, -1), (2, 2, 1)], True, False))
    jobs.append((2, [(1, 1, 2), (1, 1, -2), (-1, -1, -1)], True, False))
    jobs.append((2, [(1, 2, 2), (-1, 2, 2), (-2, -2, -2)], True, False))
    if long_run:
        jobs.append((2, [(1, 1, 2), (1, 1, -2), (-1, -1, 2), (-1, -1, -2)], True, False))
        # two independent contradictions: every chain path misses at least two threads
        jobs.append((2, [(1, 1, 1), (-1, -1, -1), (2, 2, 2), (-2, -2, -2)], True, False))
    # charging only: larger random formulas, formulas with five occurrences of every variable
    for _ in range(12):
        n = rng.randint(3, 6)
        m = rng.randint(3, 8)
        clauses = [tuple(rng.choice(literals(n)) for _ in range(3)) for _ in range(m)]
        if all(any(abs(lit) == i for c in clauses for lit in c) for i in range(1, n + 1)):
            jobs.append((n, clauses, False, False))
    for _ in range(6):
        # three variables, five clauses, every clause contains each variable once: 3CNF-5 shape
        clauses = [tuple(rng.choice((1, -1)) * i for i in (1, 2, 3)) for _ in range(5)]
        jobs.append((3, clauses, False, False))
    all_eight = [tuple(s * i for s, i in zip(signs, (1, 2, 3))) for signs in itertools.product((1, -1), repeat=3)]
    jobs.append((3, all_eight[:5], False, False))

    exact = satisfiable = strict = paths = one_connecting = charging = 0
    gaps = {}
    for index, (n, clauses, want_exact, want_all) in enumerate(jobs):
        res = check_instance(n, clauses, seed=index, exact=want_exact, all_one_connecting=want_all)
        charging += 1
        if "cp" in res:
            exact += 1
            satisfiable += res["q"] == 0
            paths += res["bounded_paths"]
            one_connecting += res.get("one_connecting", 0)
            key = (res["q"], res["eta_star"], res["cp"] - res["Lambda"])
            gaps[key] = gaps.get(key, 0) + 1
            strict += res["cp"] > res["Lambda"] + res["eta_star"]

    print(f"formulas: {len(jobs)}; charging lemma checked on the chain paths of all of them")
    print(f"exact cp on {exact} formulas ({satisfiable} satisfiable); non-chain u-v paths within the bound: {paths}; "
          f"all u-v paths with one connecting path: {one_connecting}")
    print("(least number of unsatisfied clauses, eta*, cp - Lambda): number of formulas")
    for key in sorted(gaps):
        print(f"  {key}: {gaps[key]}")
    print(f"formulas with cp > Lambda + eta*: {strict}")
    print("No check failed.")


if __name__ == "__main__":
    try:
        main()
    except Failure as failure:
        print("FAILED:", failure)
        sys.exit(1)
