"""Theorem H of dc-hardness.md: the piercing-set algorithm for 2CH + P2 with t = 1 (one node per group).

Search: for every guess phi = (phi_g) over the four groups g = (type, parity) (a node or None), a BFS over states
(current side, parity, frozenset of stored sides) where a side may be used at parity p only if its partner side is
empty or contains phi_(type, p), sides meeting some phi node are stored, at most two stored sides per phi node, and
no two stored sides belong to one switch.  Answer 'yes' iff some guess reaches a side containing t.
Always sound (a 'yes' comes with a valid mode vector); complete when some solution has a shortest side sequence whose
group partner families each have a common node (the Helly case).
Checks: soundness and success rate on random 2CH + P2 instances; R_L (not Helly, fails for larger L) and R_L with t
added to every flip side (Helly, succeeds).
Usage: python helly2ch.py SEED COUNT"""
import sys
import random
import itertools
from collections import deque
from twoch import connected, p2_ok, random_p2_instance
from swlib import exact_2ch, bits_of
from rigid_pc import rigid_named


def sides_list(inst):
    N, E, F, s, t = inst
    S = []
    for w in range(len(E)):
        if E[w]:
            S.append((w, 0, E[w]))
        if F[w]:
            S.append((w, 1, F[w]))
    return S


def partner(inst, side):
    N, E, F, s, t = inst
    w, T, m = side
    return F[w] if T == 0 else E[w]


def search(inst, phi):
    N, E, F, s, t = inst
    S = sides_list(inst)
    phimask = 0
    for v in phi.values():
        if v is not None:
            phimask |= 1 << v

    def ok(i, par):
        p = partner(inst, S[i])
        if not p:
            return True
        g = phi[(S[i][1], par)]
        return g is not None and (p >> g) & 1

    def add(i, stored):
        m = S[i][2]
        if not (m & phimask):
            return stored
        if any(S[k][0] == S[i][0] and k != i for k in stored):
            return None
        new = stored | {i}
        for v in bits_of(phimask):
            if sum(1 for k in new if (S[k][2] >> v) & 1) > 2:
                return None
        return new

    seen = set()
    dq = deque()
    for i, (w, T, m) in enumerate(S):
        if (m >> s) & 1 and ok(i, 1):
            st0 = add(i, frozenset())
            if st0 is None:
                continue
            st = (i, 1, st0)
            seen.add(st)
            dq.append(st)
    while dq:
        i, par, stored = dq.popleft()
        if (S[i][2] >> t) & 1:
            return True
        npar = 1 - par
        for j in range(len(S)):
            if not (S[i][2] & S[j][2]):
                continue
            if not ok(j, npar):
                continue
            st2 = add(j, stored)
            if st2 is None:
                continue
            st = (j, npar, st2)
            if st in seen:
                continue
            seen.add(st)
            dq.append(st)
    return False


def helly_solve(inst):
    N = inst[0]
    groups = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for combo in itertools.product([None] + list(range(N)), repeat=4):
        if search(inst, dict(zip(groups, combo))):
            return True
    return False


def add_t_to_flips(L):
    N, E, F, s, t = rigid_named(L)
    E, F = list(E), list(F)
    for k in range(1, L + 1):
        if k % 2 == 1:
            F[k - 1] |= 1 << t   # flip side of odd k is F
        else:
            E[k - 1] |= 1 << t
    return (N, E, F, s, t)


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {}
    for it in range(count):
        inst = random_p2_instance(rng, rng.randint(3, 5), rng.randint(2, 6), rng.uniform(0.1, 0.35), rng.uniform(0.1, 0.35))
        if inst[0] > 8:
            continue
        ex = exact_2ch(inst) is not None
        he = helly_solve(inst)
        st[(ex, he)] = st.get((ex, he), 0) + 1
        if he and not ex:
            print("UNSOUND", inst, flush=True)
    print("(exact, t=1 algorithm):", st, flush=True)
    for L in range(2, 6):
        inst = rigid_named(L)
        inst2 = add_t_to_flips(L)
        print("R_%d: exact %s, t=1 %s | with t in flip sides: P2 %s, exact %s, unique %s, t=1 %s" % (
            L, exact_2ch(inst) is not None, helly_solve(inst), p2_ok(inst2[1], inst2[2]),
            exact_2ch(inst2) is not None, len([m for m in range(1 << L) if connected(
                inst2[0], [inst2[2][i] if (m >> i) & 1 else inst2[1][i] for i in range(L)], inst2[3], inst2[4])]) == 1,
            helly_solve(inst2)), flush=True)
