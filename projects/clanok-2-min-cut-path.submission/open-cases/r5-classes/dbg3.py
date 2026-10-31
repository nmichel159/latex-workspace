import sys
import ccore as C
import branchfam as BF
import cdecide as D
for k in range(2, 6):
    for nf in (1, 2):
        I = BF.ybranch_fake(k, contact=2, nfake=nf)
        sols = C.all_solutions(I) if I.k <= 20 else []
        spine = [I.cl[I.names.index(("x", j))] for j in range(1, 2 * k + 1)]
        modes = set(tuple(m[c] for c in spine) for m in sols)
        st1, fx1 = C.prune(I)
        st2, fx2 = C.relaxed_prune(I)
        L, paths = C.shortest_valid_paths(I)
        g = D.guided_cost(I, paths[0], 2, 1, 1)
        print(k, nf, "P2", C.p2_ok(I), "classes", I.k, "sols", len(sols), "spine modes", modes,
              "prune", st1, len(fx1), "relaxed", st2, len(fx2), "|P|", L, "npaths", len(paths), "guided", g, flush=True)
