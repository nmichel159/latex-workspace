"""dc-hardness.md Section 2, "PC on broken rigid families" (row PC1), with own code (agent verify-round3).
cut(L, k): R_L without the node y_k (k = 1..L-1); tflip(L, k): t moved from h_L into Fl_k (k = 1..L-1).
2CH -> ZZ by the own conversion of rl_thmF.py (b_x, t_x per node, e_w per switch). For each instance: P2, exact answer
(2CH brute force over mode vectors and ZZ DFS), relaxation (both sides of every switch), AC and PC at L = largest odd
<= q. By Lemma G a refutation at this L implies a refutation at every smaller odd L.
Usage: python broken_rigid.py Lmin Lmax"""
import itertools
import sys
import time

from rl_thmF import rigid_2ch, twoch_to_zz


def connects(N, s, t, sides):
    adj = {}
    seen = {s}
    stack = [s]
    while stack:
        x = stack.pop()
        if x == t:
            return True
        for S in sides:
            if x in S:
                for y in S:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
    return False


def brute(N, s, t, sw):
    for modes in itertools.product((0, 1), repeat=len(sw)):
        if connects(N, s, t, [sw[w][m] for w, m in enumerate(modes)]):
            return True
    return False


def p2(sw):
    return all((sw[a][0] & sw[b][0]) or (sw[a][1] & sw[b][1]) for a in range(len(sw)) for b in range(a + 1, len(sw)))


if __name__ == "__main__":
    Lmin, Lmax = int(sys.argv[1]), int(sys.argv[2])
    tot = {"inst": 0, "no": 0, "relax_yes": 0, "ac_yes": 0, "pc_yes": 0, "p2": 0, "dfs_mismatch": 0}
    for L in range(Lmin, Lmax + 1):
        N, s, t, sw = rigid_2ch(L)
        sw = [(set(E), set(F)) for (E, F) in sw]
        # node indices: rigid_2ch puts 's' = 0, 't' = 1, then ('y', k) for k = 1..L-1 at index 1 + k
        for kind in ("cut", "tflip"):
            for k in range(1, L):
                sw2 = [(set(E), set(F)) for (E, F) in sw]
                if kind == "cut":
                    y = 1 + k
                    for (E, F) in sw2:
                        E.discard(y); F.discard(y)
                else:
                    for (E, F) in sw2:
                        E.discard(t); F.discard(t)
                    # Fl_k is the F-side for odd k (h_k = E), the E-side for even k
                    (sw2[k - 1][1] if k % 2 == 1 else sw2[k - 1][0]).add(t)
                t0 = time.time()
                ans = brute(N, s, t, sw2)
                rel = connects(N, s, t, [S for pair in sw2 for S in pair])
                I = twoch_to_zz(N, s, t, sw2)
                I.check()
                z = I.solve_dfs() is not None
                Lc = I.q if I.q % 2 == 1 else I.q - 1
                a = I.ac(Lc)[0]
                p = I.pc(Lc) if a else False
                tot["inst"] += 1; tot["no"] += not ans; tot["relax_yes"] += rel; tot["ac_yes"] += a
                tot["pc_yes"] += p; tot["p2"] += p2(sw2) and I.p2(); tot["dfs_mismatch"] += (z != ans)
                print("%s(%d,%d): q=%d |R|=%d P2=%s answer=%s dfs=%s relax=%s AC=%s PC=%s (%.0fs)" % (
                    kind, L, k, I.q, len(I.R), p2(sw2) and I.p2(), ans, z, rel, a, p, time.time() - t0), flush=True)
    print("TOTAL", tot)
