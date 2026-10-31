"""Independent checks of the smallest switch-model instance found by shrink_rigid.py (dc-algorithm.md 11.6):
ZZ form, P2, all solution down-sets, generator numbers, the k-guess, the strict guesses, Theorem H search with t = 1
(dc-hardness/helly2ch.py, read-only import), and AC / PC on its no-variants (one node removed from one side, keeping
P2).  Usage: python check_ac18.py 'JSON instance'"""
import os
import sys
import json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dc-hardness"))
import swlib  # noqa: E402
import helly2ch  # noqa: E402
from twoch import p2_ok  # noqa: E402
import zz  # noqa: E402
import mixed as mx  # noqa: E402
import pcfast  # noqa: E402
import ladder  # noqa: E402
import hunt_antichain as ha  # noqa: E402

inst = json.loads(sys.argv[1])
N, E, F, s, t = inst
print("nodes", N, "s", s, "t", t)
for i in range(len(E)):
    print(f"  switch {i}: E = {swlib.bits_of(E[i])}, F = {swlib.bits_of(F[i])}")
z, names = swlib.to_zz(inst)
I = mx.Info(z)
print("ZZ: q =", z.n, "|R| =", len(z.R), "names", names)
print("R:", [(names[a], names[b]) for a, b in z.R])
print("P2 (ZZ):", mx.p2_holds(z, I), " P2 (2CH):", p2_ok(E, F))
sols = mx.solutions(z, I)
print("solution down-sets:", len(sols), "exact_dfs:", zz.exact_dfs(z)[0])
for D, p in sols:
    print("   D middle =", [names[x] for x in range(z.n) if (D >> x) & 1 and names[x][0] == "sw"],
          "g_low", mx.g_low(I, D), "g_up", mx.g_up(I, D), "path", [names[x] for x in p])
print("2CH mode counts (min E, min F):", ha.mode_counts(inst))
print("k-guess low:", [mx.guess_low(z, k, I) is not None for k in range(4)],
      "up:", [mx.guess_up(z, k, I) is not None for k in range(4)])
print("strict guess:", ladder.strict_guess(z, I))
kinds = mx.witness_kinds(z, I)
print("omega(U) =", mx.clique_number(z.n, mx.lower_only_graph(z, I, kinds)),
      "omega(Lambda) =", mx.clique_number(z.n, mx.upper_only_graph(z, I, kinds)))
try:
    print("Theorem H search, t = 1:", helly2ch.helly_solve(tuple(inst)))
except Exception as ex:
    print("helly2ch failed:", repr(ex))
# no-variants
cnt = dict(total=0, p2=0, no=0, ac_fp=0, pc_fp=0)
for i in range(len(E)):
    for typ in (0, 1):
        S = E if typ == 0 else F
        for x in swlib.bits_of(S[i]):
            E2, F2 = E[:], F[:]
            if typ == 0:
                E2[i] &= ~(1 << x)
            else:
                F2[i] &= ~(1 << x)
            cnt["total"] += 1
            if not p2_ok(E2, F2):
                continue
            cnt["p2"] += 1
            inst2 = [N, E2, F2, s, t]
            z2, _ = swlib.to_zz(inst2)
            if zz.exact_dfs(z2)[0]:
                continue
            cnt["no"] += 1
            if zz.ac_answer(z2):
                cnt["ac_fp"] += 1
                if pcfast.pc_answer(z2):
                    cnt["pc_fp"] += 1
                    print("PC FALSE POSITIVE", json.dumps(inst2))
print("no-variants (one node removed from one side):", cnt)
