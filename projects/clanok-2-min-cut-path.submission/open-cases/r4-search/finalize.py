"""Re-check a found instance from scratch and store it under a descriptive name with full verdicts.
Checks: ZZ axioms (preorder, u least, v greatest, R strictly increasing), P2, exact answer by three solvers
(zz.exact_dfs, gcert.exact, all down-sets when q <= 40), number of solution down-sets, the portfolio at levels 2 and 3
(stop_early=False; H2 for switch-model instances if requested), description.
Usage: python finalize.py SRC.json DST_NAME [h2]"""
import sys
import json
from common import zz, gcert, load, to_json, save, to_gc, zz_to_sw, HERE
from portfolio import portfolio
from describe import describe
import os


def axioms(z):
    n, le = z.n, z.le
    for a in range(n):
        assert le[a][a]
        for b in range(n):
            if le[a][b]:
                for c in range(n):
                    if le[b][c]:
                        assert le[a][c], "not transitive"
    assert all(le[z.u][x] for x in range(n)) and all(le[x][z.v] for x in range(n))
    assert not le[z.v][z.u]
    for a, b in z.R:
        assert le[a][b] and not le[b][a]
    assert (z.u, z.v) not in z.R


def finalize(src, dst, h2=False):
    z, sw, names = load(src)
    axioms(z)
    out = {"p2": not z.p2_bad()}
    e1 = zz.exact_dfs(z)[0]
    e2 = gcert.exact(to_gc(z))
    assert e1 == e2
    out["exact"] = e1
    if z.n <= 40:
        sols = [D for D in zz.downsets(z) if zz.zigzag_in(z, D) is not None]
        assert bool(sols) == e1
        out["solution_downsets"] = len(sols)
    if sw is None:
        r = zz_to_sw(z)
        sw = r[0] if r else None
    v2 = portfolio(z, level=2, sw=sw, exact_ans=e1, stop_early=False)
    v3 = portfolio(z, level=3, sw=sw, exact_ans=e1, stop_early=False, h2=h2)
    out["level2"] = v2
    out["level3"] = v3
    desc = describe(z, names, 4)
    d = to_json(z, name=dst, names=names, sw=sw, verdict=out, notes=desc)
    path = os.path.join(HERE, "instances", dst + ".json")
    save(path, d)
    print(desc)
    print("level2 hard:", v2["hard"], v2["yes"] or v2["no"])
    print("level3 hard:", v3["hard"], v3["yes"] or v3["no"])
    return out


if __name__ == "__main__":
    finalize(sys.argv[1], sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == "h2")
