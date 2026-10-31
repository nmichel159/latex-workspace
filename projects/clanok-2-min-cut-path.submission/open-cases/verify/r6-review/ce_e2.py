"""Counterexamples to r5-core.md Theorem 5.2 (E2) as stated, and checks of the repairs.

CE2: 2CH (no order, no middle edges); b_1 has E_{b1} & F_{b1} != 0 (a node n in both); path a b1 c1..c4 b2.
CE3: as CE2 without the node n; one extra switch v < b2 with F_v meeting X_a and E_{b1}.
CE4: as CE3 but v, v2 < b1, b2, F_v meeting X_a and F_v2, F_v2 meeting E_{b1} (a chain inside the contraction).
Every instance: P2, yes-instance, the planted path is the unique shortest valid path, positions of b1, b2 differ by 5.
Writes runs/ce-e2.json (switch form and ZZ form) and prints the outcome of the (E2) description and of the repairs.
"""
import json

from glib import GInst, bits, p2_violations, brute, all_shortest, connects, anchored_e, NE, contract_map, cmask, to_zz
from test_tca import members, minimal_E, maximal_F, fstar_A, picks


def build(kind, nc=4):
    # switches: a = 0, b1 = 1, c_i = 2..nc+1, b2 = nc+2, extra v (, v2)
    a, b1 = 0, 1
    cs = list(range(2, 2 + nc))
    b2 = 2 + nc
    m = b2 + 1 + (1 if kind == "CE3" else 2 if kind == "CE4" else 0)
    E = [0] * m
    F = [0] * m
    names = {}
    cnt = [0]

    def node(nm):
        z = cnt[0]
        cnt[0] += 1
        names[nm] = z
        return z

    def put(z, w, ty):
        if ty == 0:
            E[w] |= 1 << z
        else:
            F[w] |= 1 << z
    s = node("s")
    t = node("t")
    path = [(a, 0), (b1, 1)] + [(c, 0) for c in cs] + [(b2, 1)]
    put(s, a, 0)
    put(t, b2, 1)
    for i in range(len(path) - 1):
        z = node("y%d" % (i + 1))
        put(z, *path[i])
        put(z, *path[i + 1])
    # P2 among the path switches
    z = node("alpha1"); put(z, a, 1); put(z, b1, 1)            # a-b1: F_a & F_b1
    z = node("alpha2"); put(z, a, 1); put(z, b2, 1)            # a-b2: F_a & F_b2
    for i, c in enumerate(cs):
        z = node("beta%d" % i); put(z, a, 1); put(z, c, 1)     # a-c_i: partners meet
        z = node("phi%d" % i); put(z, b1, 1); put(z, c, 1)     # b1-c_i: F & F
        z = node("chi%d" % i); put(z, c, 0); put(z, b2, 0)     # c_i-b2: E & E (E_b2 is dead: t only in F_b2)
    for i, j in [(i, j) for i in range(nc) for j in range(i + 2, nc)]:
        z = node("psi%d_%d" % (i, j)); put(z, cs[i], 1); put(z, cs[j], 1)
    z = node("gamma"); put(z, b1, 0); put(z, b2, 0)            # b1-b2: E & E
    rel = [[0] * m for _ in range(m)]
    if kind == "CE2":
        z = node("n"); put(z, b1, 0); put(z, b1, 1)            # E_b1 & F_b1 != 0
    elif kind == "CE3":
        v = b2 + 1
        rel[v][b2] = 1                                          # v < b2
        z = node("q"); put(z, v, 1); put(z, a, 0)              # F_v meets X_a
        z = node("p"); put(z, v, 1); put(z, b1, 0)             # F_v meets E_b1
        for w in [a, b1] + cs:                                  # P2 of v through E_v (E_v is dead: v < b2)
            z = node("ev%d" % w); put(z, v, 0); put(z, w, 0)
    elif kind == "CE4":
        v, v2 = b2 + 1, b2 + 2
        rel[v][b1] = rel[v][b2] = 1                             # v < b1, b2 (E_v dead)
        rel[v2][b1] = rel[v2][b2] = 1                           # v2 < b1, b2
        z = node("q"); put(z, v, 1); put(z, a, 0)              # F_v meets X_a
        z = node("r"); put(z, v, 1); put(z, v2, 1)             # F_v meets F_v2 (also P2 of v, v2)
        z = node("p"); put(z, v2, 1); put(z, b1, 0)            # F_v2 meets E_b1
        for vv in (v, v2):                                      # P2 of v, v2 with the others through E-sides
            for w in [a, b2] + cs:
                z = node("e%d_%d" % (vv, w)); put(z, vv, 0); put(z, w, 0)
    G = GInst(cnt[0], E, F, rel, s, t)
    P = tuple(2 * w + ty for (w, ty) in path)
    return G, P, names, (a, b1, cs, b2)


def run(kind):
    G, P, names, (a, b1, cs, b2) = build(kind)
    rec = {"kind": kind, "m": G.m, "N": G.N}
    rec["p2_violations"] = p2_violations(G)
    sols = brute(G)
    rec["yes"] = bool(sols)
    rec["n_solutions"] = len(sols)
    sp = all_shortest(G)
    rec["shortest_paths"] = sp
    rec["planted_is_unique_shortest"] = (sp == [P])
    WE, WF, pos = members(G, P)
    A, B = minimal_E(G, WE), maximal_F(G, WF)
    rec["A"], rec["B"] = sorted(bits(A)), sorted(bits(B))
    rec["pos_b1_b2"] = (pos[b1], pos[b2])
    B0 = (1 << b1) | (1 << b2)
    dB = G.dnc(B0)
    root = contract_map(G, [G.F[v] for v in bits(dB) if G.F[v]])
    c1, c2 = cmask(G, root, G.E[b1]), cmask(G, root, G.E[b2])
    U = sum(1 << y for y in range(G.m) if G.E[y] and (cmask(G, root, G.E[y]) & (c1 | c2)))
    Phi = fstar_A(G, P, A, b1) | fstar_A(G, P, A, b2)
    D = anchored_e(G, B0, 0, U, Phi)
    rec["E2_U"] = sorted(bits(U))
    rec["E2_Phi_fstar"] = sorted(bits(Phi))
    rec["E2_D"] = None if D is None else sorted(bits(D))
    rec["E2_D_picks_P"] = D is not None and picks(G, D, P)
    rec["E2_D_connects"] = D is not None and connects(G, D)
    Da = anchored_e(G, B0, 0, U, A & U)
    rec["repair_a_Phi"] = sorted(bits(A & U))
    rec["repair_a_connects"] = Da is not None and picks(G, Da, P) and connects(G, Da)
    Ub = NE(G, G.E[b1]) | NE(G, G.E[b2])
    for bb in (b1, b2):
        for v in range(G.m):
            if G.lt(v, bb) and (G.F[v] & G.E[bb]):
                Ub |= NE(G, G.F[v])
    Db = anchored_e(G, B0, 0, Ub, Phi)
    rec["repair_b_U"] = sorted(bits(Ub))
    rec["repair_b_connects"] = Db is not None and picks(G, Db, P) and connects(G, Db)
    # one E-anchor more (A_0 = {a}) also repairs it: ADESC enumerates E-anchors
    Dc = anchored_e(G, B0, 1 << a, U, Phi)
    rec["with_A0_a_connects"] = Dc is not None and connects(G, Dc)
    rec["inst"] = G.to_json()
    rec["zz"] = to_zz(G)
    rec["names"] = names
    rec["path"] = list(P)
    return rec


if __name__ == "__main__":
    out = []
    for kind in ("CE2", "CE3", "CE4"):
        r = run(kind)
        out.append(r)
        print(json.dumps({k: v for k, v in r.items() if k not in ("inst", "zz", "names")}))
    with open("runs/ce-e2.json", "w") as fh:
        json.dump(out, fh, indent=1)
