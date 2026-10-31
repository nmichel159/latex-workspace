"""Ladder family (dc-algorithm.md Section 11.6).

K(k): elements u, b_1..b_k, a_1..a_k, v; order u < b_j < a_i < v for all i, j (two levels, complete between them);
real edges: the zigzag u a_1 b_1 a_2 b_2 ... a_k b_k v, plus a_i v for all i and u b_j for all j (top witness v for
every two a's, bottom witness u for every two b's).
KW(k): the same with private hubs instead: W_b (u < W_b < all b) adjacent to every b_j and W_a (all a < W_a < v)
adjacent to every a_i, and no edges a_i v, u b_j.
Checks: order, P2, the set of solution down-sets, generator numbers, the k-guess, the strict guesses
D = {x : x < a} and D = Q - {x : x > b}, AC/PC on the no-variants (one zigzag edge deleted, P2 re-checked).
Usage: python ladder.py KMAX
"""
import sys
import zz
import mixed as mx
import pcfast


def ladder(k, hubs=False):
    # indices: u = 0, [W_b], b_1..b_k, a_1..a_k, [W_a], v
    idx = 0
    u = idx
    idx += 1
    Wb = None
    if hubs:
        Wb = idx
        idx += 1
    B = list(range(idx, idx + k))
    idx += k
    A = list(range(idx, idx + k))
    idx += k
    Wa = None
    if hubs:
        Wa = idx
        idx += 1
    v = idx
    n = idx + 1
    lt = [[False] * n for _ in range(n)]

    def less(x, y):
        lt[x][y] = True
    for x in range(1, n):
        less(u, x)
    for x in range(n - 1):
        less(x, v)
    for b in B:
        for a in A:
            less(b, a)
        if hubs:
            less(Wb, b)
    if hubs:
        for a in A:
            less(a, Wa)
            less(Wb, a)
        for b in B:
            less(b, Wa)
        less(Wb, Wa)
    lt = zz.closure(n, {(x, y) for x in range(n) for y in range(n) if lt[x][y]})
    path = [u]
    for i in range(k):
        path += [A[i], B[i]]
    path.append(v)
    R = {(min(path[i], path[i + 1]), max(path[i], path[i + 1])) for i in range(len(path) - 1)}
    R = {(x, y) if lt[x][y] else (y, x) for x, y in R}
    if hubs:
        R |= {(a, Wa) for a in A} | {(Wb, b) for b in B}
    else:
        R |= {(a, v) for a in A} | {(u, b) for b in B}
    return zz.ZZ(n, lt, sorted(R), u, v), path, A, B


def strict_guess(z, I):
    """D = {x : x < a} or D = Q - {x : x > b} for one element a or b."""
    lt = z.lt
    for a in range(z.n):
        D = sum(1 << x for x in range(z.n) if lt[x][a])
        if (D >> z.u) & 1 and not (D >> z.v) & 1 and zz.zigzag_in(z, D, I.adj) is not None:
            return True
    for b in range(z.n):
        D = sum(1 << x for x in range(z.n) if not lt[b][x])
        if (D >> z.u) & 1 and not (D >> z.v) & 1 and zz.zigzag_in(z, D, I.adj) is not None:
            return True
    return False


def report(k, hubs):
    z, path, A, B = ladder(k, hubs)
    I = mx.Info(z)
    p2 = mx.p2_holds(z, I)
    sols = mx.solutions(z, I)
    gl = [mx.g_low(I, D) for D, _ in sols]
    gu = [mx.g_up(I, D) for D, _ in sols]
    kmax = min(k, 3)
    low_ok = [mx.guess_low(z, j, I) is not None for j in range(kmax + 1)]
    up_ok = [mx.guess_up(z, j, I) is not None for j in range(kmax + 1)]
    sg = strict_guess(z, I)
    # no-variants: delete one zigzag edge
    nov = []
    for i in range(len(path) - 1):
        e = (path[i], path[i + 1]) if z.lt[path[i]][path[i + 1]] else (path[i + 1], path[i])
        R2 = [f for f in z.R if f != e]
        z2 = zz.ZZ(z.n, z.lt, R2, z.u, z.v)
        I2 = mx.Info(z2)
        ex = bool(mx.solutions(z2, I2))
        nov.append((i, mx.p2_holds(z2, I2), ex, zz.ac_answer(z2), pcfast.pc_answer(z2) if z.n <= 16 else None))
    print(f"K({k}){' hubs' if hubs else ''}: q = {z.n}, |R| = {len(z.R)}, P2 {p2}, solutions {len(sols)}, "
          f"g_low {gl}, g_up {gu}, j-guess low {low_ok}, up {up_ok}, strict guess {sg}", flush=True)
    for i, p2b, ex, ac, pc in nov:
        print(f"   edge {i} deleted: P2 {p2b}, exact {ex}, AC {ac}, PC {pc}", flush=True)


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for k in range(2, kmax + 1):
        report(k, False)
        report(k, True)
