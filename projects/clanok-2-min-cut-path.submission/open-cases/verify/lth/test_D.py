"""Lemma D of dc-hardness.md and the dead-side remark of Theorem H, Remark (2) (agent verify-LTH).

Random backbone I0 (2CH, no P2 needed); connector nodes are new nodes added to exactly two sides X, Y of different
switches. A connector is *guarded* if every s-X path of I0 uses Y' and every s-Y path of I0 uses X' (paths = sequences
of sides of I0, all modes, consecutive sides sharing a node of I0). Checks, for every mode vector:
(D) with guarded connectors only, I connects s, t iff I0 does;
(D-) control: with unguarded connectors the equivalence fails sometimes (the hypothesis is not vacuous);
(T) sides of I all of whose nodes are connectors may be given the node t without changing any answer.
Usage: python test_D.py <seed> <count>"""
import sys
import random

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *


def side_reach(sides_I0, s, removed):
    """Side ids reachable by s-paths in I0 avoiding the side id `removed`."""
    ids = [i for i in range(len(sides_I0)) if i != removed and sides_I0[i]]
    seen = set(i for i in ids if sides_I0[i] >> s & 1)
    stack = list(seen)
    while stack:
        i = stack.pop()
        for k in ids:
            if k not in seen and sides_I0[k] & sides_I0[i]:
                seen.add(k); stack.append(k)
    return seen


def guarded(sides_I0, s, X, Y):
    # every s-X path uses Y' <=> X not reachable when Y' is removed (X != Y' since different switches)
    return X not in side_reach(sides_I0, s, Y ^ 1) and Y not in side_reach(sides_I0, s, X ^ 1)


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "guarded_conn": 0, "viol_D": 0, "viol_T": 0, "control_breaks": 0, "control_inst": 0,
          "dead_sides": 0}
    for it in range(count):
        N0 = rng.randint(3, 6); n = rng.randint(2, 7)
        I0 = rand_2ch(rng, N0, n, dens=rng.choice([0.15, 0.25, 0.4]), p_empty=0.3, p2=False)
        N0, s, t, sw0 = I0
        sides0 = [x for pair in sw0 for x in pair]
        pairs = [(X, Y) for X in range(2 * n) for Y in range(2 * n) if X >> 1 != Y >> 1 and X < Y]
        good = [(X, Y) for (X, Y) in pairs if guarded(sides0, s, X, Y)]
        badp = [(X, Y) for (X, Y) in pairs if not guarded(sides0, s, X, Y)]
        for mode, plist in (("guarded", good), ("control", badp)):
            if not plist:
                continue
            conns = [rng.choice(plist) for _ in range(rng.randint(1, 6))]
            sides = list(sides0)
            N = N0
            for (X, Y) in conns:
                sides[X] |= 1 << N; sides[Y] |= 1 << N
                N += 1
            I = (N, s, t, [(sides[2 * w], sides[2 * w + 1]) for w in range(n)])
            # dead sides: non-empty in I, empty in I0
            dead = [i for i in range(2 * n) if sides[i] and not sides0[i]]
            sidesT = list(sides)
            for i in dead:
                sidesT[i] |= 1 << t
            IT = (N, s, t, [(sidesT[2 * w], sidesT[2 * w + 1]) for w in range(n)])
            differs = False
            for code in range(1 << n):
                modes = [(code >> w) & 1 for w in range(n)]
                a0 = connects(I0, modes)
                a1 = connects(I, modes)
                if mode == "guarded":
                    if a0 != a1:
                        st["viol_D"] += 1
                        print("LEMMA D FAILS", I0, conns, modes)
                    if connects(IT, modes) != a0:
                        st["viol_T"] += 1
                        print("DEAD-SIDE REMARK FAILS", I0, conns, dead, modes)
                elif a0 != a1:
                    differs = True
            if mode == "guarded":
                st["inst"] += 1; st["guarded_conn"] += len(conns); st["dead_sides"] += len(dead)
            else:
                st["control_inst"] += 1; st["control_breaks"] += differs
    print(st)
    print("violations:", st["viol_D"] + st["viol_T"])
