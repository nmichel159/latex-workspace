"""Gadget search, part A: which P2 repairs can a 3-SAT encoding take at all? (agent r4-search)

Proposition W (report, Section 5.1).  Let I be a ZZ no-instance and {x, y} an incomparable pair.  The *strongest
lower witness* of {x, y} is a new element w with down-set {z : z < x and z < y} + {w}, up-set (up x) + (up y), real
edges w-x, w-y; the strongest upper witness is dual.  A *conservative extension* J of I adds elements, order relations
and real edges but no order relation between two elements of I.  If adding the strongest lower witness creates a
consistent zigzag and adding the strongest upper witness does too, then every conservative extension of I in which
x, y have a witness (P2 for the pair) is a yes-instance.  Such a pair is called *blocked*.
So an encoding with a blocked pair has no P2 completion by witnesses (of any kind: bottom, top or middle, shared or
private, switched off by order relations to new elements); only new comparabilities between its own elements can help.

Encodings of a CNF formula tested:
  E1  zz.from_sat (theory-dc.md Theorem 13(c)): variable routes T_i / F_i, clause options P_jk, order P_jk < conflict
  E2  dc-algorithm/sw_sat.encode (pure switch model; the encoding of dc-hardness.md Section 3)
  E3  2CH with classes: clause nodes m_0 = s, ..., m_k = t in series; one switch per literal occurrence with its
      clause edge {m_(j-1), m_j} as E-side (positive literal) or F-side (negative literal), the other side empty;
      all occurrences of a variable form one class (tied)
For each formula: pairs without a witness, blocked pairs, and the pairs that only one direction repairs.
Usage: python gadgets.py SEED COUNT   (all4 and COUNT random unsatisfiable formulas)"""
import sys
import random
import itertools
import json
from common import zz, make_zz, HERE
import sw_sat
import families as dcg_families   # dc-general/families.py (to_inst with member preorder)
from common import gcert


def satisfiable(nv, clauses):
    return any(all(any((l > 0) == a[abs(l) - 1] for l in c) for c in clauses)
               for a in itertools.product([False, True], repeat=nv))


def from_gc(I):
    return make_zz(I.n, I.le, I.R, I.u, I.v)


def enc_e1(nv, clauses):
    z, names = zz.from_sat(nv, clauses)
    return z, names


def enc_e2(nv, clauses):
    inst, label = sw_sat.encode(nv, clauses)
    z = zz.from_sw(*inst)
    return z, None


def enc_e3(nv, clauses):
    k = len(clauses)
    # nodes: 0 = s = m_0, 1 = t = m_k, 2.. = m_1..m_{k-1}
    def m(j):
        if j == 0:
            return 0
        if j == k:
            return 1
        return 1 + j
    N = k + 1
    E, F, var = [], [], []
    for j, cl in enumerate(clauses, 1):
        for lit in cl:
            if lit > 0:
                E.append([m(j - 1), m(j)])
                F.append([])
            else:
                E.append([])
                F.append([m(j - 1), m(j)])
            var.append(abs(lit))
    nm = len(E)
    mle = [[var[a] == var[b] for b in range(nm)] for a in range(nm)]
    I, names = dcg_families.to_inst(N, E, F, mle, 0, 1)
    return from_gc(I), names


def strongest(z, x, y, kind):
    """z plus the strongest lower ('low') or upper ('up') witness of x, y; new element index n."""
    n, le = z.n, z.le
    lt = z.lt
    N = n + 1
    le2 = [row[:] + [False] for row in le] + [[False] * N]
    w = n
    le2[w][w] = True
    if kind == "low":
        for a in range(n):
            if lt[a][x] and lt[a][y]:
                le2[a][w] = True
            if le[x][a] or le[y][a]:
                le2[w][a] = True
        R = list(z.R) + [(w, x), (w, y)]
    else:
        for a in range(n):
            if lt[x][a] and lt[y][a]:
                le2[w][a] = True
            if le[a][x] or le[a][y]:
                le2[a][w] = True
        R = list(z.R) + [(x, w), (y, w)]
    # conservative: no new relation among old elements (le restricted to old is unchanged by construction);
    # transitivity check
    for a in range(N):
        for b in range(N):
            if le2[a][b]:
                for c in range(N):
                    if le2[b][c] and not le2[a][c]:
                        raise AssertionError("not transitive")
    return make_zz(N, le2, R, z.u, z.v)


def analyse(z):
    bad = z.p2_bad()
    blocked, only_low, only_up, both = [], [], [], []
    for x, y in bad:
        lo = zz.exact_dfs(strongest(z, x, y, "low"))[0]
        up = zz.exact_dfs(strongest(z, x, y, "up"))[0]
        if lo and up:
            blocked.append((x, y))
        elif lo:
            only_up.append((x, y))
        elif up:
            only_low.append((x, y))
        else:
            both.append((x, y))
    return bad, blocked, only_low, only_up, both


def random_unsat(rng, nv, m, width):
    while True:
        cls = []
        for _ in range(m):
            vs = rng.sample(range(1, nv + 1), min(width, nv))
            cls.append([v if rng.random() < 0.5 else -v for v in vs])
        if not satisfiable(nv, cls):
            return cls


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    formulas = [("all4", 2, [[1, 2], [1, -2], [-1, 2], [-1, -2]]),
                ("x-notx", 1, [[1], [-1]])]
    for i in range(count):
        nv = rng.randint(2, 4)
        width = rng.choice([2, 3]) if nv >= 3 else 2
        m = rng.randint(4, 8)
        formulas.append(("rand%d" % i, nv, random_unsat(rng, nv, m, width)))
    out = open("%s/runs/gadgets-A-%d.jsonl" % (HERE, seed), "w")
    tot = {}
    for name, nv, cls in formulas:
        rec = {"name": name, "nv": nv, "clauses": cls}
        for ename, enc in (("E1", enc_e1), ("E2", enc_e2), ("E3", enc_e3)):
            z, names = enc(nv, cls)
            assert not zz.exact_dfs(z)[0], (name, ename)
            bad, blocked, ol, ou, both = analyse(z)
            rec[ename] = {"q": z.n, "no_witness": len(bad), "blocked": len(blocked), "only_low": len(ol),
                          "only_up": len(ou), "both_ok": len(both)}
            if names:
                rec[ename]["blocked_pairs"] = [[str(names[a]), str(names[b])] for a, b in blocked[:40]]
            key = ename + ("-blocked" if blocked else "-unblocked")
            tot[key] = tot.get(key, 0) + 1
        print(name, cls, {e: {k: v for k, v in rec[e].items() if k != "blocked_pairs"} for e in ("E1", "E2", "E3")},
              flush=True)
        out.write(json.dumps(rec) + "\n")
        out.flush()
    print("FINAL seed=%d formulas=%d %s" % (seed, len(formulas), tot), flush=True)
