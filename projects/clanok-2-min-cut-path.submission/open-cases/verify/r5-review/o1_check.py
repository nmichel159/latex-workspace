"""r4-hard.md Lemma 4.1 and Corollary 4.2 with own code: setting S instances for phi_k (clauses A_i = (x_i or a_i),
B_i = (not x_i or b_i), random order), random E-literal per variable, random P2 completion by witness nodes (fresh or
reused with a random reuse rate, added to the E-sides (probability 0.05, 0.5 or 0.95) or the F-sides of both members), dead sides holding witness nodes only.  The proof's
construction is carried out and the resulting assignment is checked: it falsifies exactly one clause and connects
s, t.  Usage: python o1_check.py SEED COUNT K"""
import random
import sys
from collections import Counter


def main():
    seed, count, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    st = Counter()
    for it in range(count):
        # variables: ('x', i), ('a', i), ('b', i); literals (var, sign)
        clauses = []
        for i in range(k):
            clauses.append([(("x", i), True), (("a", i), True)])
            clauses.append([(("x", i), False), (("b", i), True)])
        rng.shuffle(clauses)
        m = len(clauses)
        variables = sorted({lit[0] for cl in clauses for lit in cl})
        Elit = {var: rng.choice((True, False)) for var in variables}   # sign of the E-literal
        # nodes: junctions 0..m; members
        members = []   # dict(var, clause j, type 'E'/'F', E set, F set)
        for j, cl in enumerate(clauses, start=1):
            for var, sign in cl:
                ty = "E" if sign == Elit[var] else "F"
                mem = {"var": var, "j": j, "ty": ty, "E": set(), "F": set()}
                mem[ty] |= {j - 1, j}
                members.append(mem)
        nxt = m + 1
        witness_nodes = []
        reuse = rng.random()
        pE = rng.choice((0.05, 0.5, 0.95))
        for a in range(len(members)):
            for b in range(a + 1, len(members)):
                A, B = members[a], members[b]
                if A["var"] == B["var"]:
                    continue
                if A["E"] & B["E"] or A["F"] & B["F"]:
                    continue
                side = "E" if rng.random() < pE else "F"
                if witness_nodes and rng.random() < reuse:
                    z = rng.choice(witness_nodes)
                else:
                    z = nxt
                    nxt += 1
                    witness_nodes.append(z)
                A[side].add(z)
                B[side].add(z)
        # asserts: P2, dead sides witness-only
        for A in members:
            dead = "F" if A["ty"] == "E" else "E"
            assert all(z > m for z in A[dead])
        for a in range(len(members)):
            for b in range(a + 1, len(members)):
                A, B = members[a], members[b]
                if A["var"] != B["var"]:
                    assert A["E"] & B["E"] or A["F"] & B["F"]
        # proof of Corollary 4.2
        xs = [("x", i) for i in range(k)]
        Epos = {}
        Fpos = {}
        for M in members:
            if M["var"][0] == "x":
                (Epos if M["ty"] == "E" else Fpos)[M["var"]] = M
        byE = sorted(xs, key=lambda v: Epos[v]["j"])
        p = [Epos[byE[0]], Epos[byE[14]], Epos[byE[28]]]
        chosen = {M["var"] for M in p}
        rest = sorted([v for v in xs if v not in chosen], key=lambda v: Fpos[v]["j"])
        q = [Fpos[rest[0]], Fpos[rest[14]], Fpos[rest[28]]]
        special = chosen | {M["var"] for M in q}
        case = None
        for qb in q:
            ps = [pa for pa in p if pa["E"] & qb["E"]]
            if len(ps) >= 2:
                ps.sort(key=lambda M: M["j"])
                case = ("E", ps[0], ps[-1], qb)
                break
        if case is None:
            for pa in p:
                qs = [qb for qb in q if qb["F"] & pa["F"]]
                if len(qs) >= 2:
                    qs.sort(key=lambda M: M["j"])
                    case = ("F", qs[0], qs[-1], pa)
                    break
        if case is None:
            st["lemma41_fail"] += 1
            print("LEMMA 4.1 FAILS")
            continue
        typ, lo, hi, hub = case
        st["case_" + typ] += 1
        between = [j for j in range(lo["j"] + 1, hi["j"])]
        K = None
        for j in between:
            vars_j = {lit[0] for lit in clauses[j - 1]}
            xv = [v for v in vars_j if v[0] == "x"][0]
            if xv not in special:
                K = j
                break
        if K is None:
            st["no_K"] += 1
            print("NO NON-SPECIAL CLAUSE BETWEEN")
            continue
        # assignment: classes of lo, hi, hub in mode typ; K false; all other fresh literals true
        mode = {}
        for M in (lo, hi, hub):
            mode[M["var"]] = typ
        val = {}
        for var, md in mode.items():
            # mode E means the E-literal is true
            val[var] = Elit[var] if md == "E" else (not Elit[var])
        xK = [lit for lit in clauses[K - 1] if lit[0][0] == "x"][0]
        fK = [lit for lit in clauses[K - 1] if lit[0][0] != "x"][0]
        assert xK[0] not in val
        val[xK[0]] = not xK[1]
        val[fK[0]] = not fK[1]
        for cl in clauses:
            for var, sign in cl:
                if var[0] != "x" and var not in val:
                    val[var] = sign
        for v in xs:
            if v not in val:
                val[v] = rng.choice((True, False))
        false_clauses = [j for j, cl in enumerate(clauses, start=1)
                         if not any(val[var] == sign for var, sign in cl)]
        # connectivity: picked side of a member: its E-side if its class is in mode E (E-literal true)
        par = list(range(nxt))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        for M in members:
            var = M["var"]
            md = "E" if val[var] == Elit[var] else "F"
            side = sorted(M[md])
            for z in side[1:]:
                par[find(side[0])] = find(z)
        conn = find(0) == find(m)
        if false_clauses == [K] and conn:
            st["unfaithful_shown"] += 1
        else:
            st["construction_fail"] += 1
            print("CONSTRUCTION FAILS", false_clauses, K, conn)
    print("seed %d count %d k %d:" % (seed, count, k), dict(sorted(st.items())))


if __name__ == "__main__":
    main()
