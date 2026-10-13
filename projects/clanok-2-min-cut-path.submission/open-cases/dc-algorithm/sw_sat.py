"""Proposition E (dc-algorithm.md): 3-SAT -> switch model SW (no P2), and an attempt to add P2 while keeping the
answer.

Encoding (bottoms carry the variable part, tops the clause part):
  bottoms beta_1 = u, ..., beta_{n+1} and route bottoms; tops tau_1, ..., tau_{m+1} = v; fixed edge beta_{n+1} tau_1.
  One switch per occurrence (literal l in clause j): Nt = {tau_j, tau_{j+1}} (a valley there satisfies clause j).
  Variable i: route T_i from beta_i to beta_{i+1} through the switches of the occurrences of NOT x_i (as peaks),
  route F_i through those of x_i; consecutive switches of a route share a private bottom; an empty route gets a
  dummy switch.  A switch used by the route of the value of x_i cannot serve its clause.

p2_greedy: for every pair of switches without a common neighbour, try (in random order) a shared existing bottom,
a shared existing top, a new private bottom, a new private top, and keep the first that leaves the answer 'no'.
Usage: python sw_sat.py check SEED COUNT  |  python sw_sat.py p2 SEED TRIES FORMULA"""
import os
import sys
import random
import itertools

sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zz  # noqa: E402
import sw2  # noqa: E402


def encode(nv, clauses):
    m = len(clauses)
    nb = 0
    beta = []
    for i in range(nv + 1):
        beta.append(nb)
        nb += 1
    nt = 0
    tau = []
    for j in range(m + 1):
        tau.append(nt)
        nt += 1
    # u must be bottom 0 and v top 0: beta[0] = 0 already; v = tau[m] -> swap tops 0 and m
    def tmap(t):
        return m if t == 0 else (0 if t == m else t)
    Nb, Nt, label = [], [], []
    occ = {}
    for j, cl in enumerate(clauses):
        for lit in cl:
            s = len(Nb)
            Nb.append(set())
            Nt.append({tmap(tau[j]), tmap(tau[j + 1])})
            label.append(("occ", j, lit))
            occ.setdefault(lit, []).append(s)
    for i in range(1, nv + 1):
        for lit in (-i, i):          # route T_i uses occurrences of -i, route F_i those of +i
            sws = occ.get(lit, [])
            if not sws:
                s = len(Nb)
                Nb.append(set())
                Nt.append(set())
                label.append(("dummy", i, lit))
                sws = [s]
            prev = beta[i - 1]
            for k, s in enumerate(sws):
                if k == len(sws) - 1:
                    nxt = beta[i]
                else:
                    nxt = nb
                    nb += 1
                Nb[s] |= {prev, nxt}
                prev = nxt
    F = [(beta[nv], tmap(tau[0]))]
    return [nb, nt, F, [frozenset(x) for x in Nb], [frozenset(x) for x in Nt]], label


def answer(inst):
    z = zz.from_sw(*inst)
    return zz.exact_dfs(z)[0]


def satisfiable(nv, clauses):
    return any(all(any((l > 0) == a[abs(l) - 1] for l in c) for c in clauses)
               for a in itertools.product([False, True], repeat=nv))


def p2_greedy(rng, inst):
    nb, nt, F, Nb, Nt = inst
    Nb, Nt = [set(x) for x in Nb], [set(x) for x in Nt]
    k = len(Nb)
    pairs = [(a, b) for a in range(k) for b in range(a + 1, k)]
    rng.shuffle(pairs)
    for a, b in pairs:
        if Nb[a] & Nb[b] or Nt[a] & Nt[b]:
            continue
        opts = []
        for x in range(nb):
            opts.append(("b", x))
        for t in range(nt):
            opts.append(("t", t))
        opts.append(("nb", None))
        opts.append(("nt", None))
        rng.shuffle(opts)
        ok = False
        for kind, x in opts:
            nb2, nt2 = nb, nt
            Nb2, Nt2 = [set(y) for y in Nb], [set(y) for y in Nt]
            if kind == "b":
                Nb2[a].add(x); Nb2[b].add(x)
            elif kind == "t":
                Nt2[a].add(x); Nt2[b].add(x)
            elif kind == "nb":
                Nb2[a].add(nb); Nb2[b].add(nb); nb2 += 1
            else:
                Nt2[a].add(nt); Nt2[b].add(nt); nt2 += 1
            cand = [nb2, nt2, F, [frozenset(y) for y in Nb2], [frozenset(y) for y in Nt2]]
            if not answer(cand):
                nb, nt, Nb, Nt = nb2, nt2, Nb2, Nt2
                ok = True
                break
        if not ok:
            return None, (a, b)
    return [nb, nt, F, [frozenset(y) for y in Nb], [frozenset(y) for y in Nt]], None


FORMULAS = {
    "all8": (3, [[s1 * 1, s2 * 2, s3 * 3] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]),
    "all4": (2, [[s1 * 1, s2 * 2] for s1 in (1, -1) for s2 in (1, -1)]),
    "x-notx": (1, [[1], [-1]]),
    "php32": (6, [[1, 2], [3, 4], [5, 6]] + [[-(2 * (i - 1) + h), -(2 * (j - 1) + h)]
                                             for h in (1, 2) for i in range(1, 4) for j in range(i + 1, 4)]),
}

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "check":
        seed, count = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        st = {}
        for it in range(count):
            nv = rng.randint(1, 3)
            m = rng.randint(1, 5)
            cls = [[rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3))] for _ in range(m)]
            cls = [sorted(set(c)) for c in cls]
            inst, _ = encode(nv, cls)
            a = answer(inst)
            s = satisfiable(nv, cls)
            st[(s, a)] = st.get((s, a), 0) + 1
        print("(satisfiable, SW answer):", st)
    else:
        seed, tries, name = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        nv, cls = FORMULAS[name]
        inst, label = encode(nv, cls)
        print(name, "switches", len(inst[3]), "SW answer", answer(inst), "satisfiable", satisfiable(nv, cls))
        rng = random.Random(seed)
        stuck = {}
        for t in range(tries):
            res, bad = p2_greedy(rng, inst)
            if res is not None:
                z = zz.from_sw(*res)
                print("P2 completion keeping 'no' found: n =", z.n, "P2", sw2.p2(res[3], res[4]),
                      "AC", zz.ac_answer(z), "PC", zz.pc_numpy(z) if zz.ac_answer(z) else False)
                print(sw2.fmt(tuple(res)))
                break
            key = tuple(sorted((label[bad[0]], label[bad[1]])))
            stuck[key] = stuck.get(key, 0) + 1
        else:
            print("no completion in", tries, "tries; pairs where the greedy got stuck:")
            for k, c in sorted(stuck.items(), key=lambda kv: -kv[1])[:10]:
                print("  ", k, c)


def isolated_options(inst):
    """For every pair of switches without a common neighbour: the single-link options (shared existing bottom or
    top, new private bottom or top) that keep the answer 'no' when added alone.  Adding links is monotone (it can
    only turn 'no' into 'yes'), so a pair with no such option cannot be given P2 by any supergraph of the instance
    on the same switches."""
    nb, nt, F, Nb, Nt = inst
    k = len(Nb)
    res = {}
    for a in range(k):
        for b in range(a + 1, k):
            if Nb[a] & Nb[b] or Nt[a] & Nt[b]:
                continue
            good = []
            for kind, x in [("b", x) for x in range(nb)] + [("t", t) for t in range(nt)] + [("nb", None), ("nt", None)]:
                nb2, nt2 = nb, nt
                Nb2, Nt2 = [set(y) for y in Nb], [set(y) for y in Nt]
                if kind == "b":
                    Nb2[a].add(x); Nb2[b].add(x)
                elif kind == "t":
                    Nt2[a].add(x); Nt2[b].add(x)
                elif kind == "nb":
                    Nb2[a].add(nb); Nb2[b].add(nb); nb2 += 1
                else:
                    Nt2[a].add(nt); Nt2[b].add(nt); nt2 += 1
                if not answer([nb2, nt2, F, [frozenset(y) for y in Nb2], [frozenset(y) for y in Nt2]]):
                    good.append((kind, x))
            res[(a, b)] = good
    return res
