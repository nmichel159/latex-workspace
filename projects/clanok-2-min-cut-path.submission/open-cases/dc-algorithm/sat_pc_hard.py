"""Control: is PC of the path-position CSP refuted on hard unsatisfiable formulas encoded by the 3-SAT reduction of
theory-dc.md Theorem 13(c) (no P2)?  Formulas: all 8 clauses on 3 variables; pigeonhole PHP(3,2).
Usage: python sat_pc_hard.py"""
import sys, os, time, itertools
sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zz

def sat(nv, cls):
    return any(all(any((l > 0) == a[abs(l) - 1] for l in c) for c in cls)
               for a in itertools.product([False, True], repeat=nv))

forms = {
    "all8": (3, [[s1 * 1, s2 * 2, s3 * 3] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]),
    # PHP(3,2): p_{i,h} = variable 2*(i-1)+h, i=1..3, h=1..2
    "php32": (6, [[1, 2], [3, 4], [5, 6]] + [[-(2 * (i - 1) + h), -(2 * (j - 1) + h)]
                                              for h in (1, 2) for i in range(1, 4) for j in range(i + 1, 4)]),
    "sat-control": (3, [[1, 2, 3], [-1, 2], [-2, 3], [1, -3]]),
}
for name, (nv, cls) in forms.items():
    z, names = zz.from_sat(nv, cls)
    L = 2 * nv + 2 * len(cls) + 5
    t0 = time.time()
    ex = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z, L)
    pc = zz.pc_numpy(z, L) if ac else False
    print(name, "n =", z.n, "|R| =", len(z.R), "L =", L, "satisfiable:", sat(nv, cls), "zz:", ex, "AC:", ac,
          "PC:", pc, "time %.1fs" % (time.time() - t0), flush=True)
