"""R_L and Theorem H, Remark (2) (agent verify-LTH).

(a) Helly property of the three forms of R_L: 2CH form, form with t added to every flip side, interval form.
(b) t = 1 search of Theorem H on the 2CH form of R_L. For L <= Lfull the search is run as implemented (all guesses
over node classes); for larger L the guesses are restricted to the flip-side nodes w_pq, z_pq (the only nodes that
lie in a partner); the restricted search can only answer yes when the full one does.
Usage: python rigid_H.py <Lmax helly> <Lfull> <Lmax restricted>"""
import sys
import time
import itertools

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *
from families import *


def restricted_h1(inst, names, L):
    """t = 1 search with Phi_g ranging over {none} and the nodes w_pq, z_pq (bitmask guesses)."""
    N, s, t, sw = inst
    flipnodes = [i for i, nm in enumerate(names) if isinstance(nm, tuple) and nm[0] in ("w", "z")]
    cands = [0] + [1 << x for x in flipnodes]
    # reuse h_search by temporarily restricting: emulate by a local copy of the loop body
    side = {}
    for w, (E, F) in enumerate(sw):
        if E:
            side[2 * w] = E
        if F:
            side[2 * w + 1] = F
    sids = sorted(side)
    nbr = {i: [k for k in sids if side[k] & side[i]] for i in sids}
    starts = [i for i in sids if side[i] >> s & 1]
    from collections import deque
    for Phi in itertools.product(cands, repeat=4):
        PhiU = Phi[0] | Phi[1] | Phi[2] | Phi[3]
        phinodes = bits(PhiU)

        def adm(i, par):
            p = side.get(i ^ 1, 0)
            return (not p) or bool(p & Phi[(i & 1) * 2 + par])

        def ok_store(stored, i):
            if (i ^ 1) in stored:
                return False
            ns = stored | {i}
            return all(sum(1 for j in ns if side[j] >> x & 1) <= 2 for x in phinodes)

        q = deque(); seen = set()
        for i in starts:
            if adm(i, 1) and (not side[i] & PhiU or ok_store(frozenset(), i)):
                stt = (i, 1, frozenset([i]) if side[i] & PhiU else frozenset())
                seen.add(stt); q.append(stt)
        while q:
            cur, par, stored = q.popleft()
            if side[cur] >> t & 1:
                return True, Phi
            for nx in nbr[cur]:
                npar = par ^ 1
                if not adm(nx, npar):
                    continue
                ns = stored
                if side[nx] & PhiU and nx not in stored:
                    if not ok_store(stored, nx):
                        continue
                    ns = stored | {nx}
                stt = (nx, npar, ns)
                if stt not in seen:
                    seen.add(stt); q.append(stt)
    return False, None


if __name__ == "__main__":
    Lh, Lfull, Lr = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    print("(a) Helly property (E-sides, F-sides) and uniqueness of the solution")
    for L in range(2, Lh + 1):
        row = []
        for form in ("2ch", "t_in_flips"):
            inst, names = rigid_2ch(L, t_in_flips=(form == "t_in_flips"))
            Es = [x[0] for x in inst[3]]; Fs = [x[1] for x in inst[3]]
            ok, sols = brute_2ch(inst, all_solutions=True)
            row.append("%s: helly=%s p2=%s unique=%s" % (form, is_helly(Es) and is_helly(Fs), p2_2ch(inst),
                                                         sols == [alternating_modes(L)]))
        K, swt = rigid_tic(L)
        inst = tic_to_2ch(K, swt)
        Es = [x[0] for x in inst[3]]; Fs = [x[1] for x in inst[3]]
        row.append("interval: helly=%s" % (is_helly(Es) and is_helly(Fs)))
        print("L=%d  " % L + " | ".join(row), flush=True)
    print("(b) t = 1 search of Theorem H on the 2CH form of R_L")
    for L in range(2, Lfull + 1):
        t0 = time.time()
        inst, names = rigid_2ch(L)
        print("L=%d full search: %s (%.1fs)" % (L, h_search(inst, 1), time.time() - t0), flush=True)
    for L in range(2, Lr + 1):
        t0 = time.time()
        inst, names = rigid_2ch(L)
        r, Phi = restricted_h1(inst, names, L)
        lab = None
        if Phi:
            lab = [[names[x] for x in bits(m)] for m in Phi]
        print("L=%d restricted search: %s %s (%.1fs)" % (L, r, lab, time.time() - t0), flush=True)
    for L in range(2, min(Lr, 8) + 1):
        t0 = time.time()
        inst, names = rigid_2ch(L, t_in_flips=True)
        print("L=%d t-in-flips form, full t=1 search: %s (%.1fs)" % (L, h_search(inst, 1), time.time() - t0),
              flush=True)
