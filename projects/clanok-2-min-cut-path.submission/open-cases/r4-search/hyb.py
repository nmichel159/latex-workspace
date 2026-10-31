"""The newest methods of round 4 as portfolio members (agent r4-search; other agents' code imported read-only):
  PROP   forced-exit propagation of r4-general (gsw.prune): refutes the instance (sound 'no') or fixes modes that
         every solution has;
  THR    Theorem R of r4-general: if after the fixing the free switches are pairwise incomparable and P2 holds
         after contraction, the contracted 2CH + P2 instance is equivalent; it is decided by r4-switch's algorithm
         (Theorem 10; in practice alg.decide(1, 1, 4, 8), sound 'yes'; for 'no' we record that a complete polynomial
         method applies);
  HYB    prune, delete the dead sides, run the side-set search with conflict families (gsw.GSW.decide) with a
         ladder of parameters (kd, ks, s, B); sound 'yes' for all parameters;
  NG     Theorem NG of r4-general (ng.ng), budget 2 pins, both sides; sound 'yes'.
'core' = Theorem R does not apply after propagation (comparable free switches, or P2 fails after contraction).
Every 'yes' of HYB is turned into a down-set and re-checked with common.check_downset_solution.
Self-test: python hyb.py SEED COUNT (validation against exact solvers)."""
import os
import sys
from common import OC, zz, gcert, to_gc, check_downset_solution, bits
for _d in ("r4-general", "r4-switch"):
    _p = os.path.join(OC, _d)
    if _p not in sys.path:
        sys.path.append(_p)
import gsw              # noqa: E402  (r4-general, read-only)
import ng as rng_ng     # noqa: E402  (r4-general, read-only)
import alg as ralg      # noqa: E402  (r4-switch, read-only)
import sw as rsw        # noqa: E402  (r4-switch, read-only)

LADDER = [(1, 0, 1, 3), (1, 1, 2, 6), (2, 1, 4, 8)]


def walk_to_downset(z, G, walk):
    """Valid walk of sides -> solution down-set of z (down-closure of the F-picked switches and u)."""
    M = G.M
    D = 0
    for x in range(z.n):
        if z.le[x][z.u]:
            D |= 1 << x
    for sid in walk:
        if sid & 1:
            w = M[sid >> 1]
            for a in range(z.n):
                if z.le[a][w]:
                    D |= 1 << a
    return D


def analyse(z, ladder=LADDER, all_params=False, with_ng=False, with_thr=True):
    I = to_gc(z)
    G = gsw.GSW(I)
    fixed, dead = gsw.prune(G)
    out = {"switches": G.m}
    if dead is None:
        out["prop_refutes"] = True
        out["core"] = False
        return out
    out["prop_refutes"] = False
    out["fixed"] = len(fixed)
    out["dead"] = len(dead)
    inst, free, reason = gsw.reduce_to_2ch(G, fixed)
    out["free"] = len(free)
    out["core"] = inst is None
    out["R_reason"] = reason
    if inst is not None and with_thr:
        out["R_switches"] = len(inst[1])
        out["R_yes"] = bool(ralg.decide(inst, 1, 1, 4, 8))
    H = gsw.pruned_copy(G, dead)
    out["hyb"] = None
    out["hyb_all"] = {}
    for par in ladder:
        r = H.decide(*par, want_walk=True)
        if r[0]:
            walk = r[1][2]
            D = walk_to_downset(z, G, walk)
            assert check_downset_solution(z, D), "HYB walk does not give a solution"
            out["hyb_all"][str(par)] = True
            if out["hyb"] is None:
                out["hyb"] = list(par)
            if not all_params:
                break
        else:
            out["hyb_all"][str(par)] = False
    if with_ng:
        r = rng_ng.ng(I, 2, 0)
        out["ng2"] = bool(r)
    return out


if __name__ == "__main__":
    import random
    import twoch
    import mixed
    from common import sw_to_zz
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rnd = random.Random(seed)
    st = {}

    def inc(k):
        st[k] = st.get(k, 0) + 1
    for it in range(count):
        r = rnd.random()
        if r < 0.4:
            I = gcert.random_inst(rnd, nm=rnd.randint(2, 9), p_order=rnd.choice([0.15, 0.3, 0.5]))
            z = zz.ZZ(I.n, None, I.R, I.u, I.v, le=I.le)
        elif r < 0.75:
            z = mixed.random_instance(rnd, rnd.choice(["low", "up", "mixed"]), nm=rnd.randint(2, 9),
                                      p_order=rnd.choice([0.25, 0.4]), p_tie=rnd.choice([0.0, 0.5, 1.0]))
        else:
            sw = twoch.random_p2_instance(rnd, rnd.randint(3, 5), rnd.randint(2, 7), rnd.uniform(0.1, 0.4),
                                          rnd.uniform(0.1, 0.4))
            z = sw_to_zz(sw)[0]
        if z.n > 24:
            continue
        ex = zz.exact_dfs(z)[0]
        ex2 = gcert.exact(to_gc(z))
        assert ex == ex2
        inc("yes" if ex else "no")
        a = analyse(z, all_params=True, with_ng=True)
        if a["prop_refutes"]:
            inc("PROP refutes")
            if ex:
                inc("PROP-UNSOUND")
            continue
        if a["core"]:
            inc("core-" + ("yes" if ex else "no"))
        if "R_yes" in a:
            if a["R_yes"] and not ex:
                inc("THR-UNSOUND")
            # exact answer of the contracted instance by brute force
            Gx = gsw.GSW(to_gc(z))
            fx, dd = gsw.prune(Gx)
            inst, free, reason = gsw.reduce_to_2ch(Gx, fx)
            if len(free) <= 16:
                b = rsw.brute(inst) is not None
                if b != ex:
                    inc("THR-CONTRACTION-MISMATCH")
                else:
                    inc("THR-contraction-ok")
        for par, ok in a["hyb_all"].items():
            if ok and not ex:
                inc("HYB-UNSOUND")
            if ex:
                inc("HYB%s-%s" % (par, "yes" if ok else "fail"))
        if a.get("ng2") and not ex:
            inc("NG-UNSOUND")
        if ex:
            inc("NG2-" + ("yes" if a.get("ng2") else "fail"))
        # dead sides unused by every solution (small instances)
        G = gsw.GSW(to_gc(z))
        fixed, dead = gsw.prune(G)
        if ex and G.m <= 14:
            ok = all(not (2 * w + ((mask >> w) & 1)) in dead for mask in G.brute() for w in range(G.m))
            inc("dead-ok" if ok else "DEAD-SIDE-USED")
    print("FINAL seed=%d count=%d" % (seed, count), dict(sorted(st.items())), flush=True)
