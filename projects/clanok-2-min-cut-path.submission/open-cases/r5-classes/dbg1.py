import ccore as C


def mk(N, spec):
    sw, cl = [], []
    for c, E, F in spec:
        sw.append((sum(1 << x for x in E), sum(1 << x for x in F)))
        cl.append(c)
    return C.Inst(N, 0, 1, sw, cl)


inst = mk(7, [(2, [0, 4], [0, 2, 5]), (2, [], [1, 4, 6]), (3, [5], [2, 4, 6]), (0, [0], [0, 5, 6]), (3, [2], [0, 2, 4])])
print("brute", C.brute(inst))
print("exact", C.exact(inst))
print("svp", C.shortest_valid_paths(inst))
print("csearch all", C.csearch(inst, inst.sides, 10 ** 9))
nb = C.normalize_blobs(inst)
print("blob", nb.fmt(), C.brute(nb))
print("prune", C.prune(inst))
st, fx = C.prune(inst)
ci, nm = C.contract(inst, fx)
print("contracted", ci.fmt(), C.brute(ci))
print("p2", C.p2_ok(inst), C.p2_ok(nb))
