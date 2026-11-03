"""Second implementation (Python): numbers of plane maps without a colouring, for comparison with allmaps.js."""
import sys, time, json
from planemap import generate, edge_constraints, vertex_constraints, solve

MAXM = int(sys.argv[1]) if len(sys.argv) > 1 else 7
levels = generate(MAXM)
tests = [("E[1,1]", "e", [1, 1]), ("E[1,1,1]", "e", [1, 1, 1]), ("E[1,1,2]", "e", [1, 1, 2]), ("E[1,2,2]", "e", [1, 2, 2]),
         ("E[1,2]", "e", [1, 2]), ("E[2,2]", "e", [2, 2]), ("E[1,3]", "e", [1, 3]),
         ("V[1,1,1]", "v", [1, 1, 1]), ("V[1,1,2]", "v", [1, 1, 2]), ("V[1,2,2]", "v", [1, 2, 2]), ("V[2,2,2]", "v", [2, 2, 2]),
         ("V[2,2]", "v", [2, 2]), ("V[1,3]", "v", [1, 3])]
out = {}
t0 = time.time()
for m in range(1, MAXM + 1):
    for g in levels[m].values():
        for name, kind, defects in tests:
            if kind == "e":
                for variant in ("P", "W"):
                    if solve(g.m, edge_constraints(g, variant), defects) is None:
                        out.setdefault(name + " " + variant, {}).setdefault(str(m), 0)
                        out[name + " " + variant][str(m)] += 1
            else:
                if solve(g.nv, vertex_constraints(g), defects) is None:
                    out.setdefault(name, {}).setdefault(str(m), 0)
                    out[name][str(m)] += 1
print("counts", {m: len(levels[m]) for m in levels})
for k in out:
    print("  ", k, json.dumps(out[k]).replace(" ", ""))
print("time", round(time.time() - t0, 1))
