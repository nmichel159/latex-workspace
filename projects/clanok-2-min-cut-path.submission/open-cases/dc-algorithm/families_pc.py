"""PC of the path-position CSP on structured families (agent DC-algorithm).

A. Z_k, Z'_k (theory-dc.md Section 3, built by theory-dc-scripts/antichain*.py, imported read-only), k = 2..5:
   the yes-instance, and the no-variants obtained by deleting one real edge of the unique witness path (ZZ form).
B. G(k) of experiments.md (experiments/repaired_family.py, read-only), k = 2..5, converted graph -> ZZ.
C. Rigid family R_L (dc-hardness.md Section 2), L = 2..7: yes-instance; no-variants: t moved into another set, one
   y-node deleted, and the "double wire" (a second rigid wire from the end of the first one back to t that uses the
   flipped sets in reverse order).
D. Theorem 13(b) round trip: random ZZ + P2 instance -> DC graph G(Pi) -> ZZ (graph_to_zz) -> exact, AC, PC.
E. Control without P2: Theorem B instances (Multicolored Clique, dc-algorithm/mcc.py) without a clique.
Usage: python families_pc.py SECTIONS   (e.g. ABCDE)"""
import os
import sys
import random
import itertools
import time

sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "theory-dc-scripts"))
import zz  # noqa: E402
import pcfast  # noqa: E402
import pi  # noqa: E402  (theory-dc-scripts, read-only)
import hunt2  # noqa: E402


def report(name, z, extra=""):
    t = time.time()
    ex = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z)
    pc = pcfast.pc_answer(z) if ac else False
    p2 = not z.p2_bad()
    flag = "  <-- PC FALSE POSITIVE" if (pc and not ex) else ""
    flag += "  <-- WRONG (PC no on yes)" if (ex and not pc) else ""
    print("%-34s n=%3d |R|=%3d P2=%-5s exact=%-5s AC=%-5s PC=%-5s %5.1fs %s%s"
          % (name, z.n, len(z.R), p2, ex, ac, pc, time.time() - t, extra, flag), flush=True)
    return ex, ac, pc, p2


def delete_edge(z, e):
    R = [f for f in z.R if f != e]
    return zz.ZZ(z.n, None, R, z.u, z.v, le=z.le)


# ------------------------------------------------------------------ graph -> ZZ
def graph_to_zz(n, edges, u, v):
    """ZZ instance of a graph (theory-dc.md Theorem 13(a) without the ear contraction): Q = {x : c(u,x) >= 3} (plus u),
    x <= y iff every minimum u-v cut containing y contains x (vertices in no minimum cut are equivalent to v),
    R = edges of G[Q] joining non-equivalent vertices.  Paths inside minimum cuts lie in Q (theory-dc.md Corollary 3)
    and the traces of minimum cuts on Q are the down-sets of the restricted preorder."""
    W = [[0] * n for _ in range(n)]
    for a, b in edges:
        W[a][b] += 1
        W[b][a] += 1
    Q = [u] + [x for x in range(n) if x != u and pi.maxflow(W, u, x)[0] >= 3]
    c, F = pi.maxflow(W, u, v)
    reach = pi.residual_reach(W, F)
    C = {y: reach[u] | reach[y] for y in Q}
    top = {y: bool((C[y] >> v) & 1) for y in Q}
    idx = {x: i for i, x in enumerate(Q)}
    q = len(Q)
    le = [[False] * q for _ in range(q)]
    for x in Q:
        for y in Q:
            if top[y]:
                le[idx[x]][idx[y]] = True
            elif top[x]:
                le[idx[x]][idx[y]] = False
            else:
                le[idx[x]][idx[y]] = bool((C[y] >> x) & 1)
    R = []
    for a, b in edges:
        if a in idx and b in idx:
            i, j = idx[a], idx[b]
            if le[i][j] and le[j][i]:
                continue
            assert le[i][j] or le[j][i], "edge between incomparable vertices"
            R.append((i, j))
    return zz.ZZ(q, None, R, idx[u], idx[v], le=le), c


def realise_zz(z):
    """Theorem 13(b) of theory-dc.md: weight one on every comparable pair a < b (real edge if in R, else an ear),
    an ear u-a (a != u) and an ear b-v (b != v) for every such pair; equivalent elements joined by M ears.
    Returns (n, edges, u, v) of the simple graph (ears = degree-two vertices)."""
    n = z.n
    W = [[0] * n for _ in range(n)]
    Rs = {(min(a, b), max(a, b)) for a, b in z.R}
    pairs = [(a, b) for a in range(n) for b in range(n) if z.lt[a][b]]
    M = len(pairs) + 1
    for a, b in pairs:
        W[a][b] += 1
        W[b][a] += 1
        if a != z.u:
            W[z.u][a] += 1
            W[a][z.u] += 1
        if b != z.v:
            W[b][z.v] += 1
            W[z.v][b] += 1
    for a in range(n):
        for b in range(a + 1, n):
            if z.le[a][b] and z.le[b][a]:
                W[a][b] += M
                W[b][a] += M
    inst = pi.Inst(n, sorted(Rs), W, z.u, z.v)
    N, E = inst.realise()
    return N, E, z.u, z.v


# ------------------------------------------------------------------ sections
def section_A():
    import antichain
    import antichain2
    for name, mod in (("Z", antichain), ("Z'", antichain2)):
        for k in range(2, 6):
            inst, path = mod.build(k)
            z = zz.from_pi(inst)
            report("%s_%d" % (name, k), z)
            # witness path edges in ZZ orientation
            pe = set()
            for a, b in zip(path, path[1:]):
                pe.add((a, b) if z.lt[a][b] else (b, a))
            for e in sorted(pe):
                if e in z.R:
                    report("%s_%d minus %s" % (name, k, e), delete_edge(z, e))


def section_B():
    sys.path.append(os.path.join(HERE, "..", "experiments"))
    import repaired_family
    for k in range(2, 6):
        g, u, v = repaired_family.repaired(k)
        edges = [tuple(e) for e in g.edges]
        z, c = graph_to_zz(g.n, edges, u, v)
        ex, ac, pc, p2 = report("G(%d) graph n=%d c=%d" % (k, g.n, c), z)
        for e in list(z.R):
            report("G(%d) minus %s" % (k, e), delete_edge(z, e))


def section_C():
    for L in range(2, 8):
        inst = hunt2.rigid(L)
        N, E, F, s, t = inst
        report("R_%d" % L, zz.from_sw(*hunt2.ch_to_sw(inst)))
        # t moved
        for i in range(L):
            for side in "EF":
                E2, F2 = list(E), list(F)
                for j in range(L):
                    E2[j] &= ~(1 << t)
                    F2[j] &= ~(1 << t)
                if side == "E":
                    E2[i] |= 1 << t
                else:
                    F2[i] |= 1 << t
                if (side == "E") == (i % 2 == 0) and i == L - 1:
                    continue      # original position
                report("R_%d t in %s_%d" % (L, side, i + 1), zz.from_sw(*hunt2.ch_to_sw((N, E2, F2, s, t))))
        # one node deleted
        for x in range(N):
            if x in (s, t):
                continue
            E2 = [m & ~(1 << x) for m in E]
            F2 = [m & ~(1 << x) for m in F]
            if not pcfast_p2(E2, F2):
                continue
            report("R_%d minus node %d" % (L, x), zz.from_sw(*hunt2.ch_to_sw((N, E2, F2, s, t))))
        # double wire: first wire s -> m on the path sets, second wire m -> t on the flipped sets in reverse order
        E2, F2 = list(E), list(F)
        m = N
        N2 = N + 1
        for j in range(L):
            E2[j] &= ~(1 << t)
            F2[j] &= ~(1 << t)
        last_path_is_E = (L % 2 == 1)
        if last_path_is_E:
            E2[L - 1] |= 1 << m
        else:
            F2[L - 1] |= 1 << m
        # flipped set of switch k is F if k odd (1-based) else E
        def flip_add(k, x):
            if k % 2 == 1:
                F2[k - 1] |= 1 << x
            else:
                E2[k - 1] |= 1 << x
        flip_add(L, m)
        for k in range(L, 1, -1):
            y = N2
            N2 += 1
            flip_add(k, y)
            flip_add(k - 1, y)
        flip_add(1, t)
        report("R_%d double wire" % L, zz.from_sw(*hunt2.ch_to_sw((N2, E2, F2, s, t))))


def pcfast_p2(E, F):
    n = len(E)
    return all((E[i] & E[l]) or (F[i] & F[l]) for i in range(n) for l in range(i + 1, n))


def section_D(count=40, seed=7):
    rng = random.Random(seed)
    done = 0
    while done < count:
        n = rng.randint(5, 8)
        z = zz.random_zz(rng, n, rng.choice([0.2, 0.3]), rng.choice([0.2, 0.3]))
        if sum(1 for a in range(n) for b in range(n) if z.lt[a][b]) < 3:
            continue
        N, E, u, v = realise_zz(z)
        z2, c = graph_to_zz(N, E, u, v)
        ex1 = zz.exact_dfs(z)[0]
        pc1 = pcfast.pc_answer(z) if zz.ac_answer(z) else False
        ex2, ac2, pc2, p2 = report("13(b) round trip n=%d graph %d" % (n, N), z2,
                                   "orig exact=%s PC=%s" % (ex1, pc1))
        if ex1 != ex2:
            print("   MISMATCH of exact answers")
        done += 1


def section_E(seed=3, count=12):
    import mcc
    rng = random.Random(seed)
    done = 0
    tries = 0
    while done < count and tries < 10000:
        tries += 1
        k = rng.choice([3, 4])
        sizes = [rng.randint(1, 3) for _ in range(k)]
        verts = [(i, r) for i in range(k) for r in range(1, sizes[i] + 1)]
        p = rng.choice([0.5, 0.6, 0.7, 0.8])
        edges = {frozenset((a, b)) for a, b in itertools.combinations(verts, 2) if a[0] != b[0] and rng.random() < p}
        has = any(all(frozenset(((i, ch[i]), (j, ch[j]))) in edges for i in range(k) for j in range(i + 1, k))
                  for ch in [dict(enumerate(c)) for c in itertools.product(*[range(1, s + 1) for s in sizes])])
        if has:
            continue
        z, Lz = mcc.build(k, sizes, edges)
        t = time.time()
        ex = zz.exact_dfs(z)[0]
        ac = zz.ac_answer(z, Lz)
        pc = pcfast.pc_answer(z, Lz) if ac else False
        print("MCC k=%d sizes=%s |E|=%d n=%d L=%d exact=%s AC=%s PC(L=path length)=%s %.1fs%s"
              % (k, sizes, len(edges), z.n, Lz, ex, ac, pc, time.time() - t,
                 "  <-- PC false positive (no P2)" if pc and not ex else ""), flush=True)
        done += 1


if __name__ == "__main__":
    secs = sys.argv[1] if len(sys.argv) > 1 else "ABCDE"
    for s in secs:
        print("=== section", s, flush=True)
        globals()["section_" + s]()
