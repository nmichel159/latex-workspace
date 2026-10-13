"""Theorem 13(c) of theory-dc.md: the 3-SAT reduction to ZZ, built here from the text.
Checks: the generated relation is a partial order with least u and greatest v; R joins strictly comparable pairs;
every u-v path of (Q, R) is a zigzag of the stated form; ZZ answer = satisfiability; P2 fails;
for the smallest formulas the realised graph (Theorem 13(b) construction) has cp = c iff satisfiable.
Usage: python sat_check.py SEED COUNT [realise_count] [max_clauses]"""
import sys, random, itertools, time
from collections import Counter
from eqcore import adj_masks, bit_list, leq, lt, check_P2, zz_dfs, realise, Flow, pimc_flow_dfs, bfs_dist


def build(nv, clauses):
    names = ["u", "d", "e0"] + ["a%d" % i for i in range(1, nv + 2)]
    for i in range(1, nv + 1):
        names += ["T%d" % i, "F%d" % i]
    names += ["c%d" % j for j in range(1, len(clauses) + 2)]
    for j, cl in enumerate(clauses, 1):
        for k in range(1, len(cl) + 1):
            names.append("P%d_%d" % (j, k))
    names.append("v")
    ix = {s: i for i, s in enumerate(names)}
    q = len(names)
    rel = set()

    def lt_(a, b):
        rel.add((ix[a], ix[b]))

    for s in names:
        if s != "u":
            lt_("u", s)
        if s != "v":
            lt_(s, "v")
    lt_("e0", "d")
    lt_("e0", "a1")
    for i in range(1, nv + 1):
        for X in ("T%d" % i, "F%d" % i):
            lt_(X, "a%d" % i)
            lt_(X, "a%d" % (i + 1))
    lt_("c1", "a%d" % (nv + 1))
    for j, cl in enumerate(clauses, 1):
        for k, lit in enumerate(cl, 1):
            P = "P%d_%d" % (j, k)
            lt_("c%d" % j, P)
            lt_("c%d" % (j + 1), P)
            i = abs(lit)
            lt_(P, ("F%d" % i) if lit > 0 else ("T%d" % i))
    # reflexive-transitive closure
    up = [{x} for x in range(q)]
    for a, b in rel:
        up[a].add(b)
    changed = True
    while changed:
        changed = False
        for x in range(q):
            new = set(up[x])
            for y in up[x]:
                new |= up[y]
            if new != up[x]:
                up[x] = new
                changed = True
    down = [0] * q
    for x in range(q):
        for y in up[x]:
            down[y] |= 1 << x
    R = [("u", "d"), ("e0", "d"), ("e0", "a1")]
    for i in range(1, nv + 1):
        for X in ("T%d" % i, "F%d" % i):
            R += [(X, "a%d" % i), (X, "a%d" % (i + 1))]
    R.append(("c1", "a%d" % (nv + 1)))
    for j, cl in enumerate(clauses, 1):
        for k in range(1, len(cl) + 1):
            P = "P%d_%d" % (j, k)
            R += [("c%d" % j, P), ("c%d" % (j + 1), P)]
    R.append(("c%d" % (len(clauses) + 1), "v"))
    R = [(ix[a], ix[b]) for a, b in R]
    return names, ix, q, down, R


def sat(nv, clauses):
    for bits in itertools.product([False, True], repeat=nv):
        if all(any((bits[abs(l) - 1] if l > 0 else not bits[abs(l) - 1]) for l in cl) for cl in clauses):
            return True
    return False


def all_paths(q, Radj, u, v):
    res = []

    def rec(path, onp):
        x = path[-1]
        for y in bit_list(Radj[x] & ~onp):
            if y == v:
                res.append(path + [v])
            else:
                rec(path + [y], onp | (1 << y))
    rec([u], 1 << u)
    return res


def main():
    seed = int(sys.argv[1])
    count = int(sys.argv[2])
    rcount = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = random.Random(seed)
    st = Counter()
    viol = []
    t0 = time.time()
    for it in range(count):
        nv = rng.randint(1, 4)
        m = rng.randint(1, int(sys.argv[4]) if len(sys.argv) > 4 else 5)
        clauses = []
        for _ in range(m):
            w = rng.randint(1, 3)
            vs = rng.sample(range(1, nv + 1), min(w, nv))
            clauses.append([x if rng.random() < 0.5 else -x for x in vs])
        names, ix, q, down, R = build(nv, clauses)
        u, v = ix["u"], ix["v"]
        # partial order: antisymmetric
        for x in range(q):
            for y in range(x + 1, q):
                if leq(down, x, y) and leq(down, y, x):
                    viol.append(("not antisymmetric", clauses, names[x], names[y]))
        if any(not leq(down, u, x) or not leq(down, x, v) for x in range(q)):
            viol.append(("u not least or v not greatest", clauses))
        for a, b in R:
            if not lt(down, a, b):
                viol.append(("R pair not a < b", clauses, names[a], names[b]))
        Radj = adj_masks(q, R)
        npaths = 2 ** nv
        for cl in clauses:
            npaths *= len(cl)
        enumerate_paths = npaths <= 3000
        paths = all_paths(q, Radj, u, v) if enumerate_paths else []
        if enumerate_paths and len(paths) != npaths:
            viol.append(("number of u-v paths != 2^n * prod |C_j|", clauses, len(paths), npaths))
        cons = 0
        for P in paths:
            form = [names[x] for x in P]
            exp = ["u", "d", "e0", "a1"]
            for i in range(1, nv + 1):
                exp += ["?X%d" % i, "a%d" % (i + 1)]
            exp += ["c1"]
            for j in range(1, len(clauses) + 1):
                exp += ["?P%d" % j, "c%d" % (j + 1)]
            exp += ["v"]
            ok = len(form) == len(exp) and all(
                (e == f) or (e.startswith("?X") and f in ("T" + e[2:], "F" + e[2:])) or
                (e.startswith("?P") and f.startswith("P" + e[2:] + "_")) for e, f in zip(exp, form))
            if not ok:
                viol.append(("path of unexpected form", clauses, form))
            for i in range(len(P) - 1):
                a, b = P[i], P[i + 1]
                if (i % 2 == 0 and not lt(down, a, b)) or (i % 2 == 1 and not lt(down, b, a)):
                    viol.append(("path not a zigzag", clauses, form))
                    break
            vals, peaks = P[0::2], P[1::2]
            bad = [(names[a], names[b]) for a in vals for b in peaks if leq(down, b, a)]
            for a, b in bad:
                if not (a[0] in "TF" and b[0] == "P"):
                    viol.append(("valley >= peak not a conflict relation", clauses, a, b))
            if not bad:
                cons += 1
        z, _ = zz_dfs(q, down, Radj, u, v)
        s = sat(nv, clauses)
        if z != s or (enumerate_paths and (cons > 0) != s):
            viol.append(("ZZ != SAT", clauses, z, cons, s))
        st["formulas"] += 1
        st["formulas with all paths enumerated"] += enumerate_paths
        st["satisfiable" if s else "unsatisfiable"] += 1
        st["P2 fails" if check_P2(q, down, Radj) else "P2 holds"] += 1
        st["zigzags enumerated"] += len(paths)
    # realisations of the smallest formulas
    for it in range(rcount):
        nv = 1
        m = rng.randint(1, 2)
        clauses = [[rng.choice([1, -1])] for _ in range(m)]
        names, ix, q, down, R = build(nv, clauses)
        u, v = ix["u"], ix["v"]
        n, edges, N, info = realise(q, down, R, u, v)
        F = Flow(n, edges)
        c = F.conn(u, v)
        if c != N:
            viol.append(("realised c != N", clauses))
        if bfs_dist(adj_masks(n, edges), u)[v] != 2:
            viol.append(("realised d != 2", clauses))
        pans, _, nodes = pimc_flow_dfs(n, edges, u, v, c=c)
        s = sat(nv, clauses)
        if pans != s:
            viol.append(("realised PIMC != SAT", clauses, pans, s))
        st["realised formulas"] += 1
        st["realised max n"] = max(st["realised max n"], n)
    for k in sorted(st):
        print("%-40s %d" % (k, st[k]))
    print("violations:", len(viol))
    for x in viol[:20]:
        print("  ", x)
    print("time %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
