"""Portfolio of the known polynomial methods for ZZ + P2 (agent r4-search).

Witness methods (say "yes" only with a solution; sound for every instance):
  G{K}      the K-guess on both sides (dc-algorithm.md Theorems F, F+, Fomega): D_A = Q - up(A + {v}) and
            D^B = down(B + {u}) over sets A, B of at most K middle classes.
  LAT2      lattice guesses with at most two parameters: unions and intersections of at most two basic down-sets
            down(a), {x < a}, Q - up(a), {x : not a < x} (a any element); contains the strict guesses of
            dc-algorithm/ladder.py and the 2-guess.
  H1        Theorem H search with t = 1 (dc-hardness/helly2ch.helly_solve), switch-model instances only.
  GC{K}     certificate search of dc-general.md Theorem GC with |pin set| <= K, all modes (gcert.certificate).
  H2        (level 3, switch model, optional) Theorem H with t = 2 through GC with piercers in B and T only,
            at most 4 below and 4 above (gcert.general_search).
Relaxations (say "no" only with a refutation):
  AC, PC    arc / strong path consistency of the path-position CSP with L = largest odd number <= q (zz.py, pcfast.py)
  SPC       singleton path consistency (dc-algorithm/variants.spc)
  SPPC      PC of the simple-path CSP for every odd L <= q (dc-algorithm/variants.pc_simple); refutes iff it refutes
            every L
Complete-class certificates (a failed witness method then proves "no"):
  width <= K (the K-guess enumerates all down-sets), 2 min(omega(U), omega(Lambda)) <= K (Theorem Fomega),
  switch model with Helly side families (Theorem H, t = 1).
An instance is portfolio-hard if it is a yes-instance on which no witness method finds a solution, or a no-instance
that no relaxation refutes; 'hard_strict' additionally requires (for no-instances) that no complete-class
certificate applies.
"""
import itertools
import time
from common import zz, gcert, bits, to_gc, zz_to_sw, check_downset_solution, width
import pcfast       # noqa: E402 (read-only import, dc-algorithm)
import variants     # noqa: E402 (read-only import, dc-algorithm)
import mixed        # noqa: E402 (read-only import, dc-algorithm)
import helly2ch     # noqa: E402 (read-only import, dc-hardness)
import h1fast       # JS port of helly2ch.helly_solve (validated in h1fast.py)


class Masks:
    def __init__(self, z):
        n, le = z.n, z.le
        self.z = z
        self.n = n
        self.full = (1 << n) - 1
        self.down = [sum(1 << a for a in range(n) if le[a][b]) for b in range(n)]
        self.up = [sum(1 << b for b in range(n) if le[a][b]) for a in range(n)]
        self.cls = [self.down[x] & self.up[x] for x in range(n)]
        self.hi = [0] * n
        self.lo = [0] * n
        for a, b in z.R:
            self.hi[a] |= 1 << b
            self.lo[b] |= 1 << a
        self.u, self.v = z.u, z.v
        self.B = self.cls[z.u]
        self.T = self.cls[z.v]
        seen = 0
        self.reps = []
        for x in range(n):
            if not (seen >> x) & 1:
                self.reps.append(x)
                seen |= self.cls[x]
        self.mid = [x for x in self.reps if not (self.B >> x) & 1 and not (self.T >> x) & 1]

    def valid(self, D):
        return (D >> self.u) & 1 and not (D >> self.v) & 1

    def connects(self, D):
        """u, v connected in G_D (D a down-set)."""
        hi, lo, v = self.hi, self.lo, self.v
        reach = 1 << self.u
        frontier = reach
        while frontier:
            new = 0
            m = frontier
            while m:
                low = m & -m
                x = low.bit_length() - 1
                m ^= low
                if (D >> x) & 1:
                    new |= hi[x] & ~D
                else:
                    new |= lo[x] & D
            new &= ~reach
            if (new >> v) & 1:
                return True
            reach |= new
            frontier = new
        return False


def guess(M, K):
    """K-guess on both sides; returns a solution down-set or None."""
    upv = M.up[M.v]
    for r in range(K + 1):
        for A in itertools.combinations(M.mid, r):
            U = upv
            for a in A:
                U |= M.up[a]
            D = M.full & ~U
            if M.valid(D) and M.connects(D):
                return D
            D = M.down[M.u]
            for a in A:
                D |= M.down[a]
            if M.valid(D) and M.connects(D):
                return D
    return None


def lattice2(M):
    """unions / intersections of at most two basic down-sets."""
    basics = set()
    for a in range(M.n):
        basics.add(M.down[a])
        basics.add(M.down[a] & ~M.cls[a])
        basics.add(M.full & ~M.up[a])
        basics.add(M.full & ~(M.up[a] & ~M.cls[a]))
    basics = sorted(basics)
    cand = set(b for b in basics if M.valid(b))
    for i in range(len(basics)):
        bi = basics[i]
        for j in range(i + 1, len(basics)):
            bj = basics[j]
            x = bi | bj
            if M.valid(x):
                cand.add(x)
            x = bi & bj
            if M.valid(x):
                cand.add(x)
    for D in cand:
        if M.connects(D):
            return D
    return None


def omega_bound(z):
    I = mixed.Info(z)
    kinds = mixed.witness_kinds(z, I)
    U = mixed.lower_only_graph(z, I, kinds)
    Lg = mixed.upper_only_graph(z, I, kinds)
    return mixed.clique_number(z.n, U), mixed.clique_number(z.n, Lg)


def helly_family(sets):
    """Helly property of a family of node sets (bit masks) by Berge's criterion: for every three nodes a, b, c the
    members containing at least two of them have a common node.  (Equivalent to: every pairwise intersecting
    subfamily has a common node.)"""
    sets = [s for s in sets if s]
    allnodes = 0
    for s in sets:
        allnodes |= s
    nodes = bits(allnodes)
    for a, b, c in itertools.combinations(nodes, 3):
        common = allnodes
        any_member = False
        for s in sets:
            k = ((s >> a) & 1) + ((s >> b) & 1) + ((s >> c) & 1)
            if k >= 2:
                common &= s
                any_member = True
        if any_member and not common:
            return False
    return True


def h2_search(I, sw_nodes_B, sw_nodes_T, maxpins=4, deadline=None):
    """Theorem H with t = 2 via GC general mode with piercers only in B (at most maxpins) and in T (at most maxpins).
    Returns a walk or None.  Expensive."""
    Bl = [x for x in sw_nodes_B if I.hi[x]]
    Tl = [x for x in sw_nodes_T if I.lo[x]]
    for rb in range(maxpins + 1):
        for PB in itertools.combinations(Bl, rb):
            pm = sum(1 << x for x in PB)
            for rt in range(maxpins + 1):
                for PT in itertools.combinations(Tl, rt):
                    if deadline is not None and time.time() > deadline:
                        raise TimeoutError
                    pp = sum(1 << x for x in PT)
                    w = gcert.general_search(I, 0, pm, 0, pp, 2, return_walk=True)
                    if w:
                        return w
    return None


def portfolio(z, level=2, sw=None, exact_ans=None, stop_early=True, skip=(), timing=False, h2=False,
              spc=True, sppc=True, gc=True, fast_h1=True):
    """Run the portfolio.  Returns a dict (see module doc).  level = K, the bound of the guesses and of GC.
    sw: the 2CH form if z is a switch-model instance (computed by zz_to_sw if None).
    exact_ans: the exact answer if known (else computed by zz.exact_dfs).
    stop_early: stop the witness cascade at the first success, the relaxation cascade at the first refutation."""
    K = level
    res = {"q": z.n, "R": len(z.R), "level": K, "yes": {}, "no": {}, "complete": [], "time": {}}
    t0 = time.time()
    if exact_ans is None:
        exact_ans = zz.exact_dfs(z)[0]
    res["exact"] = bool(exact_ans)
    res["p2"] = not z.p2_bad()
    M = Masks(z)
    if sw is None:
        r = zz_to_sw(z)
        sw = r[0] if r is not None else None
    res["switch_model"] = sw is not None

    def timed(name, f):
        t = time.time()
        out = f()
        res["time"][name] = round(time.time() - t, 3)
        return out

    if exact_ans:
        # witness cascade
        def record(name, D):
            ok = D is not None
            if ok and isinstance(D, int):
                assert check_downset_solution(z, D), name
            res["yes"][name] = ok
            return ok
        found = False
        if "G" not in skip:
            found = record("G%d" % K, timed("G", lambda: guess(M, K))) or found
        if not (found and stop_early) and "LAT2" not in skip:
            found = record("LAT2", timed("LAT2", lambda: lattice2(M))) or found
        if not (found and stop_early) and sw is not None and "H1" not in skip:
            r = timed("H1", lambda: h1fast.h1(sw) if fast_h1 else helly2ch.helly_solve(sw))
            res["yes"]["H1"] = bool(r)
            found = found or bool(r)
        if not (found and stop_early) and gc and "GC" not in skip:
            I = to_gc(z)
            c = timed("GC", lambda: gcert.certificate(I, K))
            res["yes"]["GC%d" % K] = c is not None
            if c is not None:
                res["gc_cert"] = [c[0], c[1], [list(x) if isinstance(x, tuple) else x for x in c[2]]]
            found = found or c is not None
        if not (found and stop_early) and h2 and sw is not None:
            I = to_gc(z)
            Bn = bits(M.B)
            Tn = bits(M.T)
            w = timed("H2", lambda: h2_search(I, Bn, Tn))
            res["yes"]["H2"] = w is not None
            found = found or w is not None
        res["hard"] = not found
        res["hard_strict"] = not found
    else:
        refuted = False
        L = z.n if z.n % 2 == 1 else z.n - 1
        if "AC" not in skip:
            r = timed("AC", lambda: zz.ac_answer(z))
            res["no"]["AC"] = not r
            refuted = not r
        if not (refuted and stop_early) and "PC" not in skip:
            r = timed("PC", lambda: pcfast.pc_answer(z))
            res["no"]["PC"] = not r
            refuted = refuted or not r
        if not (refuted and stop_early) and spc and "SPC" not in skip:
            r = timed("SPC", lambda: variants.spc(z))
            res["no"]["SPC"] = not r
            refuted = refuted or not r
        if not (refuted and stop_early) and sppc and "SPPC" not in skip:
            def sp():
                for LL in range(1, L + 1, 2):
                    if variants.pc_simple(z, LL):
                        return False
                return True
            r = timed("SPPC", sp)
            res["no"]["SPPC"] = r
            refuted = refuted or r
        res["hard"] = not refuted
        # complete-class certificates
        w = width(z)
        res["width"] = w
        if w <= K:
            res["complete"].append("width<=%d" % K)
        try:
            oU, oL = omega_bound(z)
            res["omega"] = [oU, oL]
            if 2 * min(oU, oL) <= K:
                res["complete"].append("Fomega")
        except Exception as e:  # noqa: BLE001
            res["omega"] = str(e)
        if sw is not None:
            N, E, F, s, t = sw
            if helly_family(E) and helly_family(F):
                res["complete"].append("Helly")
        res["hard_strict"] = res["hard"] and not res["complete"]
    res["time"]["total"] = round(time.time() - t0, 3)
    return res


def summary(res):
    s = "q=%d |R|=%d exact=%s P2=%s sw=%s" % (res["q"], res["R"], res["exact"], res["p2"], res["switch_model"])
    s += " yes:" + ",".join("%s=%d" % (k, v) for k, v in res["yes"].items())
    s += " no:" + ",".join("%s=%d" % (k, v) for k, v in res["no"].items())
    if res["complete"]:
        s += " complete:" + ",".join(res["complete"])
    s += " HARD" if res["hard"] else ""
    s += " (%.1fs)" % res["time"]["total"]
    return s
