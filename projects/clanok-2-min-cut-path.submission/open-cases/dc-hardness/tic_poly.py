"""Polynomial algorithm for TIC (Theorem T of dc-hardness.md) and its check against brute force.

TIC instance (tic.py): K, spans E[w], F[w] (junction intervals (a, b) or None); P2: for w != v the E-spans or the
F-spans share a junction.  Question: one span per switch covering all edges 1..K.

Algorithm.  A *chain* is a sequence of spans I_1, ..., I_r with strictly increasing left and right ends, 0 in I_1,
K in I_r, consecutive spans sharing a junction, and I_a, I_{a+2} disjoint (a minimal cover has this form).  The
*group* of the a-th span is (its type, a mod 2).  For a guess phi = (phi_g) of one junction (or None) per group, a
chain is *phi-admissible* if (i) the partner span of every member is empty or contains phi_g of the member's group
(phi_g = None allows only empty partners), and (ii) no two members that contain some phi_g are partners.
Claim: a solution exists iff some phi has a phi-admissible chain.  The search below is a BFS over states
(previous span, current span, parity, set of members so far that contain a phi junction); a minimal chain has at
most two members through each junction, so the last component has at most 8 spans and the state space is
O(K^4 n^10) over all guesses: polynomial.  (The implementation is written for clarity, not speed.)
Usage: python tic_poly.py SEED COUNT"""
import sys
import random
import itertools
from collections import deque
import tic


def sides_of(E, F):
    out = []  # (switch, type, span)
    for w in range(len(E)):
        if E[w] is not None:
            out.append((w, "E", E[w]))
        if F[w] is not None:
            out.append((w, "F", F[w]))
    return out


def partner_span(E, F, side):
    w, T, sp = side
    return F[w] if T == "E" else E[w]


def contains(sp, j):
    return sp is not None and sp[0] <= j <= sp[1]


def admissible_chain(K, E, F, phi):
    """BFS for a phi-admissible chain; phi: dict group -> junction or None.  Returns the chain or None."""
    S = sides_of(E, F)
    phis = [j for j in phi.values() if j is not None]

    def ok_i(idx, parity):
        w, T, sp = S[idx]
        par = partner_span(E, F, S[idx])
        if par is None:
            return True
        g = phi[(T, parity)]
        return g is not None and contains(par, g)

    def meets_phi(idx):
        sp = S[idx][2]
        return any(contains(sp, j) for j in phis)

    start = [i for i, (w, T, sp) in enumerate(S) if sp[0] == 0 and ok_i(i, 1)]
    seen = set()
    dq = deque()
    for i in start:
        mset = frozenset([i]) if meets_phi(i) else frozenset()
        st = (None, i, 1, mset)
        seen.add(st)
        dq.append((st, [i]))
    while dq:
        (prev, cur, par, mset), path = dq.popleft()
        if S[cur][2][1] == K:
            return [S[i] for i in path]
        a, b = S[cur][2]
        npar = 1 - par
        for j, (w, T, sp) in enumerate(S):
            c, d = sp
            if not (a < c <= b and d > b):
                continue
            if prev is not None and S[prev][2][1] >= c:
                continue  # I_{a-1} and I_{a+1} must be disjoint
            if not ok_i(j, npar):
                continue
            mset2 = mset
            if meets_phi(j):
                if any(S[k][0] == w for k in mset):
                    continue  # partner (or same switch) among phi-members
                mset2 = mset | {j}
            st = (cur, j, npar, mset2)
            if st in seen:
                continue
            seen.add(st)
            dq.append((st, path + [j]))
    return None


def poly_solve(K, E, F):
    groups = [("E", 0), ("E", 1), ("F", 0), ("F", 1)]
    choices = [None] + list(range(K + 1))
    for combo in itertools.product(choices, repeat=4):
        phi = dict(zip(groups, combo))
        ch = admissible_chain(K, E, F, phi)
        if ch is not None:
            return True, phi, ch
    return False, None, None


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {}
    bad = []
    for it in range(count):
        K = rng.randint(1, 7)
        n = rng.randint(1, 7)
        K, E, F = tic.random_tic(rng, K, n, longp=rng.choice([0.0, 0.2, 0.5]))
        # occasionally drop a side
        if rng.random() < 0.1:
            w = rng.randrange(n)
            if rng.random() < 0.5:
                E[w] = None
            else:
                F[w] = None
            if not tic.p2_ok(E, F):
                continue
        ex = tic.exact(K, E, F) is not None
        po = poly_solve(K, E, F)[0]
        st[(ex, po)] = st.get((ex, po), 0) + 1
        if ex != po:
            bad.append((K, E, F))
    for L in range(1, 8):
        K, E, F = tic.rigid(L)
        ex = tic.exact(K, E, F) is not None
        po = poly_solve(K, E, F)[0]
        st[("rigid", ex, po)] = st.get(("rigid", ex, po), 0) + 1
    print("(exact, poly):", st)
    for b in bad[:5]:
        print("MISMATCH", b)
