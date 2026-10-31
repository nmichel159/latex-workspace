import ccore as C
import branchfam as BF
for k in range(2, 6):
    I = BF.ybranch(k)
    sols = C.all_solutions(I)
    spine = [I.cl[I.names.index(("x", j))] for j in range(1, 2 * k + 1)]
    modes = set(tuple(m[c] for c in spine) for m in sols)
    st, fx = C.relaxed_prune(I)
    print(k, "spine modes over solutions:", modes, "relaxed_prune:", st, len(fx), "of", I.k)
