"""rv-r6-chain: end-to-end runs of the chain  graph of DC -> ZZ + P2 -> general switch form -> Theorem 8.2 / IDESC.

usage:
  python rvc_run.py graphs SEED COUNT [PAIRS_PER_GRAPH]      random DC graphs (verify/equivalence/randgraphs.py)
  python rvc_run.py zzrand SEED COUNT NMMIN NMMAX            random ZZ + P2 instances realised as graphs (Thm 13(b))
  python rvc_run.py families KMAX LMAX                       hub H(2,2), Y_k, Y'_k, X_L, Z_k, Z^B_k, known families, Y^d_k
  python rvc_run.py r4search [GLOB]                          r4-search/instances/*.json
  options (env): RVC_WORKERS (default 6), RVC_PATHS (shortest paths per instance, default 12),
                 RVC_SMALL (blind single-term search when m <= this, default 9)

For every pair (u, v) with d = 2, c >= 3 of a graph in DC:
  brute force on the graph (subset table when n <= 20; Lemma 6 walk search always), Theorem 13(a) (own), P2,
  own ZZ solver, own switch form + gsw.GSW cross-check, switch-form answers (shortest valid path; down-set
  enumeration when m <= 18), the proof of Theorem 8.2 on up to RVC_PATHS shortest valid paths (every claim checked),
  the final intersection lifted back to a vertex set of G and checked to be a minimum cut containing a u-v path,
  random down-sets lifted and compared (connectivity in switch form = path in the cut of G), and a blind search over
  single terms with reduced parameters (sound; recorded, not required).
Every record is one JSON line in runs/<tag>.jsonl; the summary goes to stdout (redirect to runs/<tag>.txt).
"""
import os
import sys
import json
import time
import random
import traceback
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rvc_lib as L      # noqa: E402
import rvc_src as S      # noqa: E402

NPATHS = int(os.environ.get("RVC_PATHS", "12"))
BUDGET = int(os.environ.get("RVC_BUDGET", "200000"))
QREAL = int(os.environ.get("RVC_QREAL", "60"))
L.HALF = os.environ.get("RVC_HALF", "0") == "1"
L.PREFER_DAMAGE = os.environ.get("RVC_DAMAGE", "0") == "1"
ZBUDGET = int(os.environ.get("RVC_ZBUDGET", "3000000"))
FULLM = int(os.environ.get("RVC_FULLM", "6"))
SMALL = int(os.environ.get("RVC_SMALL", "9"))


def sig(N, E, F, s, t, m):
    out = []
    for z in range(N):
        inc = tuple(sorted([(w, 0) for w in range(m) if (E[w] >> z) & 1] + [(w, 1) for w in range(m) if (F[w] >> z) & 1]))
        if inc or z in (s, t):
            out.append((inc, z == s, z == t))
    return sorted(out)


def chain_pair(G, u, v, name, rng, orig=None):
    rec = {"name": name, "n": G.n, "e": len(G.edges), "u": u, "v": v, "err": []}
    err = rec["err"]
    d = G.dist_from(u)[v]
    cap = G.unit_cap()
    c, _ = L.maxflow(G.n, cap, u, v)
    rec["d"], rec["c"] = d, c
    if d != 2 or c < 3:
        rec["skip"] = "not open case"
        return rec
    # ---------------------------------------------------------------- brute force on the graph
    t0 = time.time()
    bp = None
    try:
        cb, bp, states = L.brute_paths(G, u, v, budget=BUDGET)
        rec["bp_states"] = states
        if cb != c:
            err.append("flow value mismatch")
    except RuntimeError:
        rec["bp"] = "budget"
    bs = None
    if G.n <= 20:
        cs, bs, nmin = L.brute_subsets(G, u, v)
        rec["nmincuts"] = nmin
        if cs != c:
            err.append("subset c %d != flow c %d" % (cs, c))
    bc = None
    if bs is None:
        try:
            cc, bc, nmc = L.brute_core(G, u, v, kmax=int(os.environ.get("RVC_COREMAX", "24")))
            rec["ncoretraces"] = nmc
            if cc != c:
                err.append("core-table c %d != flow c %d" % (cc, c))
        except ValueError as e:
            rec["bc"] = str(e)
    got = [(nm, x) for nm, x in (("subsets", bs), ("core", bc), ("paths", bp)) if x is not None]
    if len(set(x for _, x in got)) > 1:
        err.append("MISMATCH between brute forces %s" % (got,))
    rec["brute_methods"] = [nm for nm, _ in got]
    brute = got[0][1] if got else None
    rec["brute"] = brute
    rec["t_brute"] = round(time.time() - t0, 3)
    # ---------------------------------------------------------------- Theorem 13(a)
    g2z = L.GraphToZZ(G, u, v)
    z = g2z.zz
    rec["q"], rec["R"], rec["ears"] = z.q, len(z.R), len(g2z.ears)
    if g2z.c != c:
        err.append("c_H %d != c_G %d" % (g2z.c, c))
    if not z.check_preorder():
        err.append("ZZ preorder invalid")
    p2b = z.p2_bad()
    rec["p2_zz"] = not p2b
    if p2b:
        err.append("P2 FAILS in ZZ: %s" % (p2b[:3],))
    try:
        zans = z.exact(budget=ZBUDGET)
    except RuntimeError:
        zans = None
    rec["zz"] = zans
    if brute is not None and zans is not None and zans != brute:
        err.append("MISMATCH zz %s brute %s" % (zans, brute))
    if orig is not None:
        same = (z.q == orig.q)
        if same:
            Q = g2z.Q
            same = all(z.le[i][j] == orig.le[Q[i]][Q[j]] for i in range(z.q) for j in range(z.q)) and \
                sorted(tuple(sorted((Q[a], Q[b]))) for a, b in z.R) == sorted(tuple(sorted(e)) for e in orig.R)
        rec["roundtrip"] = same
        oans = orig.exact()
        rec["zz_orig"] = oans
        if oans != (brute if brute is not None else zans):
            err.append("MISMATCH original ZZ %s graph %s" % (oans, brute))
    return chain_sf(z, zans, brute, rec, err, rng, g2z, c)


def bad_pairs(sf, pd):
    """Bad pairs of r5-core.md §6.4 on the path: y < x, x in N_F - A, y in N_E - B."""
    cnt = 0
    for x in L.bits(pd.NFset & ~pd.A):
        cnt += L.popcount(sf.sdown[x] & pd.NEset & ~pd.B)
    return cnt


def zz_connects(z, Dq):
    """ZZ level: is u connected to v in G_D (R-edges with exactly one end in the down-set Dq)?"""
    adj = {}
    for a, b in z.R:
        if ((Dq >> a) & 1) != ((Dq >> b) & 1):
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
    seen = {z.u}
    st = [z.u]
    while st:
        x = st.pop()
        if x == z.v:
            return True
        for y in adj.get(x, []):
            if y not in seen:
                seen.add(y)
                st.append(y)
    return False


def chain_zz_only(z, name, rng):
    """For ZZ instances too large to realise as graphs: the chain from the ZZ instance on."""
    rec = {"name": name, "q": z.q, "R": len(z.R), "err": [], "zz_only": True}
    err = rec["err"]
    if not z.check_preorder():
        err.append("ZZ preorder invalid")
    p2b = z.p2_bad()
    rec["p2_zz"] = not p2b
    if p2b:
        rec["skip"] = "no P2"
        return rec
    try:
        zans = z.exact(budget=ZBUDGET)
    except RuntimeError:
        zans = None
        rec["zz"] = "budget"
    else:
        rec["zz"] = zans
    return chain_sf(z, zans, None, rec, err, rng, None, None)


def chain_sf(z, zans, brute, rec, err, rng, g2z, c):
    # ---------------------------------------------------------------- switch form
    try:
        sf = L.SF(z)
    except ValueError as e:
        rec["sf"] = str(e)
        return rec
    rec["m"], rec["N"] = sf.m, sf.N
    p2s = sf.p2_bad()
    rec["p2_sf"] = not p2s
    if p2s:
        err.append("P2 FAILS in switch form: %s" % (p2s[:3],))
    try:
        GW = S.gsw_crosscheck(z)
        same = (GW.M == sf.mid and GW.m == sf.m and
                [[bool(x) for x in r] for r in GW.le] == sf.le and
                sig(GW.N, GW.E, GW.F, GW.s, GW.t, GW.m) == sig(sf.N, sf.E, sf.F, sf.s, sf.t, sf.m))
        rec["gsw_same"] = same
        if not same:
            err.append("gsw.GSW differs from own conversion")
        if sf.m <= 14:
            ga = bool(GW.brute())
            rec["gsw_brute"] = ga
            if zans is not None and ga != zans:
                err.append("MISMATCH gsw.brute %s zz %s" % (ga, zans))
    except Exception as e:        # noqa: BLE001
        err.append("gsw crosscheck exception %r" % (e,))
    Lsh = sf.shortest()
    sans = Lsh is not None
    rec["sf_L"] = Lsh
    rec["sf"] = sans
    if zans is not None and sans != zans:
        err.append("MISMATCH switch form %s zz %s" % (sans, zans))
    if sf.m <= 18:
        try:
            sb = sf.brute()
            rec["sf_brute"] = sb
            if sb != sans:
                err.append("MISMATCH sf.brute %s sf.shortest %s" % (sb, sans))
        except RuntimeError:
            pass
    final = brute if brute is not None else (zans if zans is not None else sans)
    rec["answer"] = final
    rec["answer_from"] = "graph" if brute is not None else ("zz" if zans is not None else "switch form")
    # ---------------------------------------------------------------- Theorem 8.2 on shortest valid paths
    def certify(D, what):
        """D (down-set of switches): ZZ level (u, v connected in G_D') and, if the graph is known, its lift to G is a
        minimum cut; returns (ZZ-level connectivity, graph-level path-in-cut or None)."""
        if not sf.is_down(D):
            err.append("%s: not a down-set" % what)
        Dq = sf.lift_down(D)
        zc = zz_connects(z, Dq)
        gc = None
        if g2z is not None:
            A = g2z.lift(Dq)
            cs, gc = g2z.cut_check(A)
            if cs != c:
                err.append("%s: lifted cut %d != c %d" % (what, cs, c))
            if gc != zc:
                err.append("MISMATCH %s: ZZ connects %s, graph cut has path %s" % (what, zc, gc))
        return zc, gc

    info = {}
    if sans and Lsh == 0:
        rec["s_eq_t"] = True
        zc, gc = certify(0, "s = t")
        if gc:
            rec["cert_graph"] = True
        if not zc:
            err.append("s = t but D = {} does not connect at ZZ level")
        rec["idesc"] = True
    elif sans:
        paths = sf.all_shortest(Lsh, limit=NPATHS)
        rec["paths"] = len(paths)
        if not paths:
            err.append("no shortest path enumerated")
        ok_any = False
        for P in paths:
            perr = []
            D, terms, pd = L.theorem82(sf, P, perr, info)
            info["Amax"] = max(info.get("Amax", 0), L.popcount(pd.A))
            info["bad"] = max(info.get("bad", 0), bad_pairs(sf, pd))
            if perr:
                err.extend(["P%s: %s" % ([(w, "EF"[ty]) for w, ty in P], x) for x in perr[:4]])
            if D is None:
                continue
            zc, gc = certify(D, "final D")
            if zc and gc is not False:
                ok_any = True
                if gc:
                    rec["cert_graph"] = True
            else:
                err.append("final D of Theorem 8.2 does not certify (ZZ %s, graph %s)" % (zc, gc))
        rec["idesc"] = ok_any
        rec["info"] = info
    else:
        rec["idesc"] = False       # IDESC is sound: no down-set connects, so no test can succeed
    if rec.get("idesc") != final:
        err.append("MISMATCH idesc %s answer %s" % (rec.get("idesc"), final))
    # ---------------------------------------------------------------- random down-sets: semantics of the conversion
    sem = 0
    for it in range(25):
        p = rng.choice([0.1, 0.3, 0.5, 0.7])
        Sg = sum(1 << i for i in range(sf.m) if rng.random() < p)
        D = sf.downclose(Sg)
        con = sf.connects(D)
        zc, gc = certify(D, "random down-set")
        if con != zc:
            err.append("MISMATCH semantics: switch form %s, ZZ %s" % (con, zc))
            break
        sem += 1
    rec["sem"] = sem
    # ---------------------------------------------------------------- blind single-term search, reduced parameters
    if sf.m <= FULLM:
        t1 = time.time()
        okf, nterms = L.idesc_full(sf, want=True)
        rec["idesc_full"] = okf
        rec["idesc_full_terms"] = nterms
        rec["t_idesc_full"] = round(time.time() - t1, 2)
        if okf != final:
            err.append("MISMATCH blind IDESC(k,k,N,9k) %s answer %s" % (okf, final))
    if sf.m <= SMALL:
        ok, wit = L.idesc_small(sf, 1, 2, 1)
        rec["single"] = ok
        if ok and not final:
            err.append("UNSOUND: single term connects on a no-instance")
    return rec


def run_graph_items(items):
    """items: list of (name, n, edges, pairs or None, seed)."""
    out = []
    for name, n, edges, pairs, seed in items:
        rng = random.Random(seed)
        try:
            G = L.Graph(n, edges)
            if any(x < 0 for x in G.dist_from(0)):
                out.append({"name": name, "skip": "disconnected"})
                continue
            ok, bad = L.dc_test(G)
            if not ok:
                out.append({"name": name, "skip": "not DC", "bad": bad})
                continue
            if pairs is None:
                cand = []
                cap = G.unit_cap()
                for a in range(n):
                    da = G.dist_from(a)
                    for b in range(a + 1, n):
                        if da[b] == 2 and L.maxflow(n, cap, a, b, limit=3)[0] >= 3:
                            cand.append((a, b))
                rng.shuffle(cand)
                pairs = cand[:int(os.environ.get("RVC_PAIRS", "4"))]
            for (a, b) in pairs:
                for (uu, vv) in ((a, b), (b, a)) if (rng.random() < 0.3 and not name.startswith("small")) else ((a, b),):
                    try:
                        out.append(chain_pair(G, uu, vv, "%s (%d,%d)" % (name, uu, vv), rng))
                    except Exception as e:      # noqa: BLE001
                        out.append({"name": name, "err": ["EXCEPTION %r" % (e,), traceback.format_exc()[-800:]]})
        except Exception as e:                  # noqa: BLE001
            out.append({"name": name, "err": ["EXCEPTION %r" % (e,), traceback.format_exc()[-800:]]})
    return out


def run_zz_items(items):
    """items: list of (zz dict, seed): realise (Theorem 13(b), M = 1), check DC, run the chain from the graph."""
    out = []
    for zd, seed in items:
        rng = random.Random(seed)
        name = zd["name"]
        try:
            z = L.ZZ(zd["q"], zd["le"], zd["R"], zd["u"], zd["v"])
            if not z.check_preorder():
                out.append({"name": name, "skip": "bad preorder"})
                continue
            p2 = not z.p2_bad()
            if z.q > QREAL:
                out.append(chain_zz_only(z, name, rng))
                continue
            n, edges = L.realise(z, M=1)
            G = L.Graph(n, edges)
            ok, bad = L.dc_test(G)
            if ok != p2:
                out.append({"name": name, "err": ["Fact 1 fails: DC %s, P2 %s" % (ok, p2)]})
                continue
            if not ok:
                out.append({"name": name, "skip": "no P2 (not DC)"})
                continue
            r = chain_pair(G, z.u, z.v, name, rng, orig=z)
            out.append(r)
        except Exception as e:                  # noqa: BLE001
            out.append({"name": name, "err": ["EXCEPTION %r" % (e,), traceback.format_exc()[-800:]]})
    return out


def summarise(recs, tag, t0):
    st = Counter()
    worst = Counter()
    for r in recs:
        if r.get("skip"):
            st["skipped: " + r["skip"]] += 1
            continue
        if r.get("err"):
            st["RECORDS WITH ERRORS"] += 1
        st["pairs"] += 1
        if r.get("answer") is True:
            st["yes"] += 1
        elif r.get("answer") is False:
            st["no"] += 1
        if r.get("bp") == "budget":
            st["brute_paths over budget"] += 1
        bm = r.get("brute_methods", [])
        st["brute methods: " + "+".join(bm) if bm else "NO GRAPH BRUTE FORCE"] += 1
        if r.get("roundtrip") is False:
            st["roundtrip differs (13(a) of 13(b))"] += 1
        if r.get("gsw_same"):
            st["gsw.GSW identical"] += 1
        if r.get("s_eq_t"):
            st["s = t"] += 1
        st["paths checked (Thm 8.2)"] += r.get("paths", 0)
        st["random down-sets lifted"] += r.get("sem", 0)
        if "idesc_full" in r:
            st["blind IDESC(k,k,N,9k) run (m <= FULLM)"] += 1
            if r["idesc_full"]:
                st["blind IDESC(k,k,N,9k) accepts"] += 1
        if "single" in r:
            st["blind single-term search run"] += 1
            if r["single"]:
                st["blind single-term search accepts"] += 1
        inf = r.get("info") or {}
        if r.get("cert_graph"):
            st["yes certified in G (lifted D: min cut with u-v path)"] += 1
        if r.get("answer") is False and not r.get("brute_methods"):
            st["no-instances without graph brute force"] += 1
        if r.get("zz_only"):
            st["ZZ level only (too large to realise)"] += 1
        if r.get("p2_zz") and r.get("p2_sf"):
            st["P2 in ZZ and in switch form"] += 1
        for kk in ("levels", "tools", "flips", "anchors", "damage", "heavy", "span", "Amax", "bad"):
            if kk in inf:
                worst[kk] = max(worst[kk], inf[kk])
        for kk in ("m", "q", "n", "c", "sf_L"):
            if isinstance(r.get(kk), int):
                worst[kk] = max(worst[kk], r[kk])
        if inf.get("levels", 0) >= 2:
            st["paths/instances with >= 2 levels"] += 1
    print("== %s (%.0fs)" % (tag, time.time() - t0))
    for kk in sorted(st):
        print("  %-45s %s" % (kk, st[kk]))
    print("  maxima:", dict(worst))
    errs = [r for r in recs if r.get("err")]
    for r in errs[:30]:
        print("  ERR", r.get("name"), r["err"][:6])
    print("  total records with errors: %d" % len(errs))


def main():
    mode = sys.argv[1]
    workers = int(os.environ.get("RVC_WORKERS", "6"))
    t0 = time.time()
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    jobs = []
    if mode == "graphs":
        seed, count = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        gs = S.random_graphs(rng, count)
        for i, (kind, n, edges, pair) in enumerate(gs):
            jobs.append(("graph", ("%s-%d-%d" % (kind, seed, i), n, edges, [pair] if pair else None, seed * 100003 + i)))
        tag = "graphs-%d-%d" % (seed, count)
    elif mode == "zzrand":
        seed, count, a, b = (int(x) for x in sys.argv[2:6])
        rng = random.Random(seed)
        for i in range(count):
            zd = S.random_zz(rng, rng.randint(a, b))
            zd["name"] += "-%d-%d" % (seed, i)
            jobs.append(("zz", (zd, seed * 100003 + i)))
        tag = "zzrand-%d-%d-%d-%d" % (seed, count, a, b)
    elif mode == "families":
        kmax, lmax = int(sys.argv[2]), int(sys.argv[3])
        insts, ferrs = S.families(kmax, lmax)
        for e in ferrs:
            print("  family generator skipped:", e)
        for i, zd in enumerate(insts):
            jobs.append(("zz", (zd, 7000 + i)))
        tag = "families-%d-%d" % (kmax, lmax)
    elif mode == "small":
        # every connected graph with at most 8 vertices (networkx atlas for n <= 7, verify/equivalence/graphs8.g6
        # for n = 8), every ordered pair with d = 2, c >= 3 (the DC test is done per graph)
        import networkx as nx
        gl = [g for g in nx.graph_atlas_g() if g.number_of_nodes() >= 3]
        g8 = os.path.join(os.path.dirname(HERE), "equivalence", "graphs8.g6")
        gl += list(nx.read_graph6(g8))
        batch = []
        for i, g in enumerate(gl):
            if not nx.is_connected(g):
                continue
            n = g.number_of_nodes()
            g = nx.convert_node_labels_to_integers(g)
            edges = list(g.edges())
            Gt = L.Graph(n, edges)
            cap = Gt.unit_cap()
            pairs = []
            for a in range(n):
                da = Gt.dist_from(a)
                for b in range(n):
                    if a != b and da[b] == 2 and L.maxflow(n, cap, a, b, limit=3)[0] >= 3:
                        pairs.append((a, b))
            if pairs:
                batch.append(("small-%d-n%d" % (i, n), n, edges, pairs, 5000 + i))
            if len(batch) >= 40:
                jobs.append(("graphs", batch))
                batch = []
        if batch:
            jobs.append(("graphs", batch))
        tag = "small-n8"
    elif mode in ("bad", "rgen"):
        seed, count = int(sys.argv[2]), int(sys.argv[3])
        for i, zd in enumerate(S.designs(seed, count, mode)):
            jobs.append(("zz", (zd, seed * 100003 + i)))
        tag = "%s-%d-%d" % (mode, seed, count)
    elif mode == "bp":
        for i, zd in enumerate(S.bp_family(int(sys.argv[2]))):
            jobs.append(("zz", (zd, 8500 + i)))
        tag = "bp-%s" % sys.argv[2]
    elif mode == "saved":
        for i, zd in enumerate(S.saved_designs()):
            jobs.append(("zz", (zd, 8000 + i)))
        tag = "saved"
    elif mode == "r4search":
        pat = sys.argv[2] if len(sys.argv) > 2 else "*.json"
        for i, zd in enumerate(S.r4search(pat)):
            jobs.append(("zz", (zd, 9000 + i)))
        tag = "r4search-" + pat.replace("*", "X").replace(".json", "")
    else:
        raise SystemExit(__doc__)
    if L.HALF:
        tag += "-half"
    if L.PREFER_DAMAGE:
        tag += "-dmg"
    tag += os.environ.get("RVC_TAGSUFFIX", "")
    print("%s: %d jobs, %d workers" % (tag, len(jobs), workers), flush=True)
    recs = []
    outf = open(os.path.join(HERE, "runs", tag + ".jsonl"), "w")

    def handle(res):
        for r in res:
            recs.append(r)
            outf.write(json.dumps(r, default=str) + "\n")
        outf.flush()

    if workers <= 1:
        for kind, it in jobs:
            if kind == "graphs":
                handle(run_graph_items(it))
            else:
                handle(run_graph_items([it]) if kind == "graph" else run_zz_items([it]))
    else:
        from multiprocessing import Pool
        with Pool(workers) as pool:
            futs = []
            for kind, it in jobs:
                if kind == "graphs":
                    futs.append(pool.apply_async(run_graph_items, (it,)))
                    continue
                fn = run_graph_items if kind == "graph" else run_zz_items
                futs.append(pool.apply_async(fn, ([it],)))
            for i, f in enumerate(futs):
                handle(f.get())
                if (i + 1) % 50 == 0:
                    print("  %d/%d jobs (%.0fs)" % (i + 1, len(jobs), time.time() - t0), flush=True)
    outf.close()
    summarise(recs, tag, t0)


if __name__ == "__main__":
    main()
