"""NP-hardness without DC (sketch check): 3-SAT -> zigzag-path problem on a poset (Section 5 of theory-dc.md),
realised by absreal.realise; checks equivalence with satisfiability on random small formulas by exhaustive
minimum-cut enumeration of the realised instance."""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi
from absreal import closure, realise

def build(nvars, clauses):
    """vertices: u, d, e0, a_1..a_{n+1}, T_i, F_i, c_1..c_{m+1}, P_{j,k}, v.
    zigzag: u < d > e0 < a_1 > {T_1|F_1} < a_2 > ... > {T_n|F_n} < a_{n+1} > c_1 < P_{1,k} > c_2 < ... > c_{m+1} < v.
    conflicts: F_i > P_{j,k} if literal k of clause j is x_i; T_i > P_{j,k} if it is not x_i."""
    names = []
    def new(nm):
        names.append(nm); return len(names) - 1
    u = new("u"); d = new("d"); e0 = new("e0")
    a = [None] + [new("a%d" % i) for i in range(1, nvars + 2)]
    T = [None] + [new("T%d" % i) for i in range(1, nvars + 1)]
    F = [None] + [new("F%d" % i) for i in range(1, nvars + 1)]
    m = len(clauses)
    c = [None] + [new("c%d" % j) for j in range(1, m + 2)]
    P = {}
    for j, cl in enumerate(clauses, 1):
        for k, lit in enumerate(cl):
            P[(j, k)] = new("P%d_%d" % (j, k))
    v = new("v")
    less = set(); R = set()
    def up(lo, hi, real=True):
        less.add((lo, hi))
        if real:
            R.add((lo, hi))
    up(u, d); up(e0, d); up(e0, a[1])
    for i in range(1, nvars + 1):
        for X in (T[i], F[i]):
            up(X, a[i]); up(X, a[i + 1])
    up(c[1], a[nvars + 1])
    for (j, k), p in P.items():
        up(c[j], p); up(c[j + 1], p)
    up(c[m + 1], v)
    for (j, k), p in P.items():
        lit = clauses[j - 1][k]
        i = abs(lit)
        if lit > 0:
            up(p, F[i], real=False)
        else:
            up(p, T[i], real=False)
    n = len(names)
    for x in range(n):
        if x != u:
            less.add((u, x))
        if x != v:
            less.add((x, v))
    return n, less, R, u, v, names

def sat(nvars, clauses):
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any((bits[abs(l) - 1] if l > 0 else not bits[abs(l) - 1]) for l in cl) for cl in clauses):
            return True
    return False

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    agree = disagree = 0
    for it in range(count):
        nv = rng.randint(1, 3); m = rng.randint(1, 4)
        clauses = [[rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3))] for _ in range(m)]
        n, less, R, u, v, names = build(nv, clauses)
        lt = closure(n, less)
        inst = realise(n, lt, R, u, v)
        res = pi.answer(inst, limit=10 ** 6)
        if res["yes"] == sat(nv, clauses):
            agree += 1
        else:
            disagree += 1
            print("MISMATCH", nv, clauses, res["yes"])
    print("formulas: %d agree, %d disagree" % (agree, disagree))
