"""Check of Lemma 4.1 and Corollary 4.2 (r4-hard.md, Section 4) on random instances of setting S.

Setting S: switch model with classes for a CNF formula; junction nodes 0..m (s = 0, t = m); one class per variable;
one member per literal occurrence, main side {j-1, j} of type E (E-literal) or F; P2 completed by witness nodes
(nodes > m) added to sides, never junctions to dead sides.

For phi_k = AND_i (x_i or a_i)(not x_i or b_i), random clause order, random E-literal per variable and random P2
completion, the script runs the construction of the proof of Corollary 4.2 and checks that the assignment it builds
falsifies exactly one clause and connects s and t.  A second mode checks faithfulness exhaustively on small random
formulas (all assignments) and counts unfaithful instances.

Usage: python o1check.py SEED COUNT K [small COUNT2]
"""
import itertools
import random
import sys


class UF:
    def __init__(self):
        self.p = {}

    def f(self, x):
        p = self.p
        p.setdefault(x, x)
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def u(self, a, b):
        a, b = self.f(a), self.f(b)
        if a != b:
            self.p[a] = b


def encode(clauses, elit, rng, p_reuse):
    """clauses: list of lists of (var, sign); elit[var] = sign of the E-literal.  Returns members list of dicts
    {cls, typ, E:set, F:set, clause j} and the junction count m.  P2 completed at random."""
    m = len(clauses)
    mem = []
    for j, cl in enumerate(clauses, 1):
        for var, sign in cl:
            typ = "E" if sign == elit[var] else "F"
            d = dict(cls=var, typ=typ, j=j, E=set(), F=set(), sign=sign)
            d[typ] |= {j - 1, j}
            mem.append(d)
    nxt = [m + 1]
    witness_nodes = {"E": [], "F": []}
    pairs = [(a, b) for a in range(len(mem)) for b in range(a + 1, len(mem)) if mem[a]["cls"] != mem[b]["cls"]]
    rng.shuffle(pairs)
    for a, b in pairs:
        A, B = mem[a], mem[b]
        if A["E"] & B["E"] or A["F"] & B["F"]:
            continue
        t = rng.choice("EF")
        if rng.random() < p_reuse and witness_nodes[t]:
            # reuse a witness node already in one of the two sides, else a random existing one
            cand = [z for z in (A[t] | B[t]) if z > m]
            z = rng.choice(cand) if cand else rng.choice(witness_nodes[t])
        else:
            z = nxt[0]
            nxt[0] += 1
            witness_nodes[t].append(z)
        A[t].add(z)
        B[t].add(z)
    for a, b in pairs:
        assert mem[a]["E"] & mem[b]["E"] or mem[a]["F"] & mem[b]["F"]
    for d in mem:  # dead sides hold witness nodes only
        dead = "F" if d["typ"] == "E" else "E"
        assert all(z > m for z in d[dead])
    return mem, m


def connected(mem, m, emode):
    """emode[var] True iff the class is in mode E (E-literal true)."""
    uf = UF()
    for d in mem:
        side = d["E"] if emode[d["cls"]] else d["F"]
        side = sorted(side)
        for z in side[1:]:
            uf.u(side[0], z)
    return uf.f(0) == uf.f(m)


def phi_k(k, rng):
    cl = []
    for i in range(k):
        cl.append([("x%d" % i, 1), ("a%d" % i, 1)])
        cl.append([("x%d" % i, -1), ("b%d" % i, 1)])
    rng.shuffle(cl)
    return cl


def run_cor42(seed, count, k):
    rng = random.Random(seed)
    ok = 0
    caseE = caseF = 0
    for it in range(count):
        clauses = phi_k(k, rng)
        vars_ = sorted({v for c in clauses for v, s in c})
        elit = {v: rng.choice([1, -1]) for v in vars_}
        mem, m = encode(clauses, elit, rng, p_reuse=rng.random())
        xs = ["x%d" % i for i in range(k)]
        epos, fpos, emem, fmem = {}, {}, {}, {}
        for d in mem:
            if d["cls"] in xs:
                if d["typ"] == "E":
                    epos[d["cls"]], emem[d["cls"]] = d["j"], d
                else:
                    fpos[d["cls"]], fmem[d["cls"]] = d["j"], d
        se = sorted(xs, key=lambda x: epos[x])
        Ev = [se[0], se[14], se[28]]
        rest = sorted([x for x in xs if x not in Ev], key=lambda x: fpos[x])
        Fv = [rest[0], rest[14], rest[28]]
        P = [emem[x] for x in Ev]
        Qm = [fmem[x] for x in Fv]
        special = set()
        for x in Ev + Fv:
            special |= {epos[x], fpos[x]}
        conf = None
        for qb in Qm:
            ps = [p for p in P if p["E"] & qb["E"]]
            if len(ps) >= 2:
                conf = ("E", ps[0], ps[1], qb)
                break
        if conf is None:
            for pa in P:
                qs = [q for q in Qm if q["F"] & pa["F"]]
                if len(qs) >= 2:
                    conf = ("F", qs[0], qs[1], pa)
                    break
        assert conf is not None, "Lemma 4.1 violated"
        kind, m1, m2, hub = conf
        lo, hi = sorted([m1["j"], m2["j"]])
        assert hi - lo >= 14
        K = next(j for j in range(lo + 1, hi) if j not in special)
        emode = {v: rng.random() < 0.5 for v in vars_}
        for d in (m1, m2, hub):
            emode[d["cls"]] = (kind == "E")
        # falsify clause K, satisfy every other clause by its fresh literal
        clK = clauses[K - 1]
        for j, cl in enumerate(clauses, 1):
            for var, sign in cl:
                if var.startswith("x"):
                    continue
                want_true = (j != K)
                emode[var] = (sign == elit[var]) if want_true else (sign != elit[var])
        xvar, xsign = [(v, s) for v, s in clK if v.startswith("x")][0]
        assert xvar not in Ev + Fv
        emode[xvar] = (xsign != elit[xvar])  # literal false
        val = {v: (emode[v] if elit[v] == 1 else not emode[v]) for v in vars_}
        false_cl = [j for j, cl in enumerate(clauses, 1) if not any(val[v] == (s == 1) for v, s in cl)]
        assert false_cl == [K], false_cl
        assert connected(mem, m, emode), "not connected"
        ok += 1
        caseE += kind == "E"
        caseF += kind == "F"
    print("cor42 seed", seed, "k", k, "instances", count, "construction succeeded", ok, "case E", caseE, "case F", caseF)


def run_small(seed, count):
    """Faithfulness on small random formulas, all assignments."""
    rng = random.Random(seed)
    unf = 0
    tot = 0
    for it in range(count):
        nv = rng.randint(3, 6)
        m = rng.randint(3, 8)
        clauses = []
        for _ in range(m):
            sz = rng.randint(1, 3)
            vs = rng.sample(range(nv), min(sz, nv))
            clauses.append([("y%d" % v, rng.choice([1, -1])) for v in vs])
        vars_ = sorted({v for c in clauses for v, s in c})
        elit = {v: rng.choice([1, -1]) for v in vars_}
        mem, mm = encode(clauses, elit, rng, p_reuse=rng.random())
        bad = False
        for bits in itertools.product([False, True], repeat=len(vars_)):
            emode = dict(zip(vars_, bits))
            val = {v: (emode[v] if elit[v] == 1 else not emode[v]) for v in vars_}
            sat = all(any(val[v] == (s == 1) for v, s in cl) for cl in clauses)
            con = connected(mem, mm, emode)
            assert con or not sat  # satisfying assignments always connect
            if con and not sat:
                bad = True
        tot += 1
        unf += bad
    print("small seed", seed, "formulas", tot, "unfaithful completions", unf)


if __name__ == "__main__":
    seed, count, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    run_cor42(seed, count, k)
    if len(sys.argv) > 5 and sys.argv[4] == "small":
        run_small(seed, int(sys.argv[5]))
