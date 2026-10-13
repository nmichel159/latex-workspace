"""Theorem L(a) of dc-hardness.md: concentration lemma and window search on 2CH + P2 with a layout (verify-LTH).

Instances: positions 0..P-1, k nodes per position (node = pos * k + j), every side inside a window of l + 1
positions (reach <= l); P2 repaired by adding a node to two sides only when the reach stays <= l.
Checks: (1) concentration: if some w, v with non-empty E-sides have |x_w - x_v| > 2l, all non-empty F-sides lie in
[y_w - 2l, y_w + 3l]; otherwise all non-empty E-sides lie in an interval of 3l + 1 positions (and symmetrically);
(2) on every solution and every shortest sequence, at most |W| + 1 sides of the concentrated type occur;
(3) the window search (sets S of at most |W| + 1 switches in the concentrated mode, the rest in the other mode)
agrees with brute force. Usage: python test_La.py <seed> <count>
"""
import sys
import random
import itertools

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *


def gen(rng, P, k, l, n, p_empty=0.1):
    N = P * k
    pos = [x // k for x in range(N)]

    def rside():
        p0 = rng.randint(0, P - 1)
        p1 = min(P - 1, p0 + rng.randint(0, l))
        cand = [x for x in range(N) if p0 <= pos[x] <= p1]
        m = 0
        while not m:
            for x in cand:
                if rng.random() < 0.5:
                    m |= 1 << x
        return m

    sw = []
    for _ in range(n):
        pair = [0 if rng.random() < p_empty else rside() for _ in range(2)]
        if not pair[0] and not pair[1]:
            pair[0] = rside()
        sw.append(pair)

    def reach_ok(m):
        ps = [pos[x] for x in bits(m)]
        return max(ps) - min(ps) <= l

    for _ in range(5000):
        bad = p2_violations(sw)
        if not bad:
            break
        a, b = rng.choice(bad)
        opts = [(m, x) for m in (0, 1) for x in range(N)
                if sw[a][m] and sw[b][m] and reach_ok(sw[a][m] | 1 << x) and reach_ok(sw[b][m] | 1 << x)]
        if opts:
            m, x = rng.choice(opts)
            sw[a][m] |= 1 << x; sw[b][m] |= 1 << x
        else:
            w = rng.choice((a, b)); m = rng.randint(0, 1)
            sw[w][m] = rside()
    else:
        return None
    if not p2_violations(sw):
        s = rng.randrange(N); t = rng.randrange(N)
        if s == t:
            t = (s + 1) % N
        return (N, s, t, [tuple(x) for x in sw]), pos
    return None


def concentration(inst, pos, l):
    """Returns (type, window positions) as in the proof, or raises AssertionError if the lemma fails."""
    N, s, t, sw = inst
    result = None
    for typ in (0, 1):
        other = 1 - typ
        xs = {w: min(pos[x] for x in bits(sw[w][typ])) for w in range(len(sw)) if sw[w][typ]}
        far = [(w, v) for w in xs for v in xs if xs[w] - xs[v] > 2 * l]
        for (w, v) in far:          # every far pair, both orders of the types
            for z in (w, v):
                yz = min(pos[x] for x in bits(sw[z][other]))
                lo, hi = yz - 2 * l, yz + 3 * l
                for r in range(len(sw)):
                    if sw[r][other]:
                        assert all(lo <= pos[x] <= hi for x in bits(sw[r][other])), ("window", inst, typ)
                if typ == 0 and result is None:
                    result = (other, (lo, hi))
    if result is not None:
        return result
    xs = {w: min(pos[x] for x in bits(sw[w][0])) for w in range(len(sw)) if sw[w][0]}
    if not xs:
        return 0, (0, -1)
    lo = min(xs.values()); hi = lo + 3 * l
    assert max(xs.values()) - lo <= 2 * l
    for w in range(len(sw)):
        if sw[w][0]:
            assert all(lo <= pos[x] <= hi for x in bits(sw[w][0])), ("E-window", inst)
    return 0, (lo, hi)


def window_search(inst, typ, Wsize):
    N, s, t, sw = inst
    n = len(sw)
    for size in range(0, min(n, Wsize + 1) + 1):
        for S in itertools.combinations(range(n), size):
            modes = [1 - typ] * n
            for w in S:
                modes[w] = typ
            if connects(inst, modes):
                return True
    return False


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "yes": 0, "viol": 0, "maxcount_ratio": 0.0, "nontrivial_window": 0}
    for it in range(count):
        P = rng.randint(4, 12); k = rng.randint(1, 2); l = rng.randint(1, 3); n = rng.randint(3, 10)
        g = gen(rng, P, k, l, n)
        if g is None:
            continue
        inst, pos = g
        st["inst"] += 1
        try:
            typ, (lo, hi) = concentration(inst, pos, l)
        except AssertionError as e:
            st["viol"] += 1
            print("CONCENTRATION FAILS", e)
            continue
        W = [x for x in range(inst[0]) if lo <= pos[x] <= hi]
        if len(W) + 1 < n:
            st["nontrivial_window"] += 1
        ok, sols = brute_2ch(inst, all_solutions=True)
        st["yes"] += ok
        for modes in sols[:50]:
            for seq in shortest_sequences(inst, modes, limit=50):
                cnt = sum(1 for i in seq if (i & 1) == typ)
                if cnt > len(W) + 1:
                    st["viol"] += 1
                    print("COUNT FAILS", inst, seq, typ, W)
        ws = window_search(inst, typ, len(W))
        if ws != ok:
            st["viol"] += 1
            print("WINDOW SEARCH FAILS", inst, ok, ws)
    print(st)
    print("violations:", st["viol"])
