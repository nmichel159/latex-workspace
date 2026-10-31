"""rv-r6-chain: instance sources.  Code of other folders is imported read-only and used only to GENERATE instances
(graphs or ZZ instances); everything checked is computed by rvc_lib.py.  The cross-check against gsw.GSW (r4-general)
is the only other use of foreign code, and it is labelled as a cross-check.
"""
import os
import sys
import json
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(os.path.dirname(HERE))          # .../open-cases


def _path(*dirs):
    for d in dirs:
        p = os.path.join(OC, *d.split("/"))
        if p not in sys.path:
            sys.path.append(p)          # appended: own modules (rvc_*) are found first


def tuple_zz(n, le, R, u, v, name):
    return {"name": name, "q": int(n), "le": [[bool(x) for x in row] for row in le],
            "R": [(int(a), int(b)) for a, b in R], "u": int(u), "v": int(v)}


# ---------------------------------------------------------------------------------------------- graphs
def random_graphs(rng, count):
    """verify/equivalence/randgraphs.py (core + ears; planted alternating paths), DC version (k = 2)."""
    _path("verify/equivalence")
    import randgraphs
    out = []
    tries = 0
    while len(out) < count and tries < 50 * count:
        tries += 1
        if tries % 2:
            r = randgraphs.gen_core_ears(rng, k=2)
            if r:
                out.append(("core-ears", r[0], r[1], None))
        else:
            r = randgraphs.gen_planted(rng, k=2)
            if r:
                out.append(("planted", r[0], r[1], (r[2], r[3])))
    return out


# ---------------------------------------------------------------------------------------------- ZZ instances
def random_zz(rng, nm):
    """dc-general/gcert.random_inst and dc-algorithm/mixed.random_instance (as used by r5-core/test_inter.py)."""
    _path("dc-general", "dc-algorithm", "dc-hardness", "r4-general")
    import gcert
    if rng.random() < 0.5:
        I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
        return tuple_zz(I.n, I.le, I.R, I.u, I.v, "gcert")
    import mixed
    z = mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                              p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5]))
    return tuple_zz(z.n, z.le, z.R, z.u, z.v, "mixed")


def r4search(pattern="*.json"):
    out = []
    for f in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", pattern))):
        d = json.load(open(f))
        out.append(tuple_zz(d["n"], d["le"], d["R"], d["u"], d["v"], "r4s:" + d.get("name", os.path.basename(f))))
    return out


def families(kmax=4, Lmax=8):
    """Hub H(2,2) (classes and strict), Y_k, Y'_k, X_L, Z_k, Z^B_k and the other known families of r4-search/known.py,
    and Y^d_k (r5-core/fool.py, converted back to ZZ by r5-core/gcore.to_inst)."""
    _path("r4-general", "dc-general", "dc-algorithm", "dc-hardness")
    out = []
    errs = []
    import hubimp
    for strict in (False, True):
        for (a, b) in ((1, 1), (2, 2)):
            try:
                z, names = hubimp.hubimp(a, b, strict=strict)
                out.append(tuple_zz(z.n, z.le, z.R, z.u, z.v, "H(%d,%d)%s" % (a, b, "po" if strict else "cl")))
            except Exception as e:      # noqa: BLE001
                errs.append("hub %s: %r" % ((a, b, strict), e))
    import yfam
    import xfam
    import zfam
    for k in range(2, kmax + 1):
        for contact in (False, True):
            try:
                I, full, info = yfam.yfam(k, contact=contact)
                out.append(tuple_zz(I.n, I.le, I.R, I.u, I.v, "Y%s_%d" % ("'" if contact else "", k)))
            except Exception as e:      # noqa: BLE001
                errs.append("yfam %d: %r" % (k, e))
    for L in range(2, Lmax + 1):
        try:
            I, full, info = xfam.xfam(L)
            out.append(tuple_zz(I.n, I.le, I.R, I.u, I.v, "X_%d" % L))
        except Exception as e:          # noqa: BLE001
            errs.append("xfam %d: %r" % (L, e))
    for k in range(2, kmax + 1):
        for block in (False, True):
            try:
                r = zfam.zfam(k, block=block)
                I = r[0] if isinstance(r, tuple) else r
                out.append(tuple_zz(I.n, I.le, I.R, I.u, I.v, "Z%s_%d" % ("^B" if block else "", k)))
            except Exception as e:      # noqa: BLE001
                errs.append("zfam %d %s: %r" % (k, block, e))
    try:
        _path("r4-search", "dc-general", "dc-algorithm", "dc-hardness")
        import known
        for fn, args in (("ladder", (3,)), ("ladder", (4,)), ("ladder", (3, True)), ("a14", ()),
                         ("rigid_2ch", (4,)), ("rigid_2ch", (6,)), ("rigid_2ch", (4, True)),
                         ("tic_mates", (4, "tie")), ("tic_mates", (4, "oneway")), ("tic_mates", (6, "tie")),
                         ("tic_mates", (6, "oneway")), ("rigid_mates", (4, "tie")), ("rigid_mates", (4, "oneway"))):
            try:
                name, z, names, sw = getattr(known, fn)(*args)
                out.append(tuple_zz(z.n, z.le, z.R, z.u, z.v, name))
            except Exception as e:      # noqa: BLE001
                errs.append("known.%s%s: %r" % (fn, args, e))
    except Exception as e:              # noqa: BLE001
        errs.append("known: %r" % (e,))
    try:
        _path("r5-core")
        import fool
        import gcore
        for k in range(2, kmax + 1):
            for back in (False, True):
                for contact in (False, True):
                    try:
                        Gd, _ = fool.yd(k, back=back, contact=contact)
                        I = gcore.to_inst(Gd)
                        if isinstance(I, tuple):
                            I = I[0]
                        out.append(tuple_zz(I.n, I.le, I.R, I.u, I.v,
                                            "Y%s^d_%d%s" % ("'" if contact else "", k, " back" if back else "")))
                    except Exception as e:      # noqa: BLE001
                        errs.append("yd %d: %r" % (k, e))
    except Exception as e:              # noqa: BLE001
        errs.append("fool: %r" % (e,))
    return out, errs


def _gen_to_zz(Gd, name):
    import gcore
    I = gcore.to_inst(Gd)
    if isinstance(I, tuple):
        I = I[0]
    return tuple_zz(I.n, I.le, I.R, I.u, I.v, name)


def designs(seed, count, kind):
    """Designs of r5-core §8.4 with many bad pairs: kind 'bad' (badgen.design via test_bad.one), 'rgen' (rigid words,
    test_rgen.make with n in 9..14), converted to ZZ by gcore.to_inst (all read-only)."""
    import random
    _path("r5-core", "r4-general", "dc-general", "dc-algorithm", "dc-hardness")
    rng = random.Random(seed)
    out = []
    if kind == "bad":
        import test_bad
        for it in range(count):
            out.append(_gen_to_zz(test_bad.one(rng, it), "bad-%d-%d" % (seed, it)))
    else:
        import test_rgen
        for it in range(count):
            Gd, W, pp = test_rgen.make(rng, rng.randint(9, 14))
            out.append(_gen_to_zz(Gd, "rgen-%d-%d%s" % (seed, it, "-pp" if pp else "")))
    return out


def saved_designs():
    """r5-core/runs/two-levels-example.json and r5-core/runs/single/*.json (hunt_single.load), as ZZ."""
    _path("r5-core", "r4-general", "dc-general", "dc-algorithm", "dc-hardness")
    import hunt_single
    out = []
    files = [os.path.join(OC, "r5-core", "runs", "two-levels-example.json")] + \
        sorted(glob.glob(os.path.join(OC, "r5-core", "runs", "single", "*.json")))
    for f in files:
        Gd, extra = hunt_single.load(f)
        out.append(_gen_to_zz(Gd, "saved:" + os.path.basename(f)))
    return out


def bp_family(nmax):
    """BP_n of r5-hard.md (bpfam.bp, K_{n,n} of bad pairs on R_{2n}), with and without the bad switches, as ZZ."""
    _path("r5-hard", "r5-core", "r4-general", "dc-general", "dc-algorithm", "dc-hardness")
    import bpfam
    out = []
    for n in range(1, nmax + 1):
        for wb in (True, False):
            Gd = bpfam.bp(n, with_bad=wb)
            out.append(_gen_to_zz(Gd, "BP_%d%s" % (n, "" if wb else " base")))
    return out


def gsw_crosscheck(zd):
    """gsw.GSW of r4-general (read-only), on the same ZZ instance; returns (N, E, F, s, t, M, le) or None."""
    _path("r4-general", "dc-general", "dc-algorithm", "dc-hardness")
    import gcert
    import gsw
    I = gcert.Inst(zd.q, [list(r) for r in zd.le], list(zd.R), zd.u, zd.v)
    G = gsw.GSW(I)
    return G
