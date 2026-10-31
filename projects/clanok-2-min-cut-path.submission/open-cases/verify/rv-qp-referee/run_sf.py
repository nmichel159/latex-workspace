"""Referee qp-referee: Sections 3-6 of qp-proof.md on ZZ instances and on switch-form instances.

modes
  zz <r> [part] [parts]   every ZZ instance with r middle elements (own enumeration: all preorders on
                           {u} + r elements + {v} with u <= x <= v and u < v, every R of strictly comparable pairs
                           without {u, v}), P2 instances only; Lemma 3.2, 3.3 (per down-set), 3.4, 4.2-4.5,
                           Theorem 5.3 on every shortest valid path, exact IDESC (Definition 6.1) vs brute force.
                           With parts > 1 only the preorders with index = part mod parts.
  zzr <seed> <count> <rlo> <rhi>  random ZZ instances (own generator), same checks (IDESC exact if m <= 7)
  rsw <seed> <count> <mlo> <mhi>  verify/rv-r6-core/gen8.random_sw (generator only), same checks on the switch form
  rigid <seed> <count> <nlo> <nhi> verify/rv-r6-core/gen8.rigid_design (planted path), Section 4, Theorem 5.3
  deep <seed> <count> <L> <k>     verify/rv-r6-core/gen8.deep_design, Section 4, Theorem 5.3 (levels recorded)
"""
import os
import sys
import json
import time
import random
import traceback
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qpr_lib as L

OC = os.path.dirname(os.path.dirname(HERE))


def foreign_gen8():
    p = os.path.join(OC, "verify", "rv-r6-core")
    if p not in sys.path:
        sys.path.append(p)
    import gen8
    return gen8


def from_sw(I):
    le = [sum(1 << j for j in range(I.m) if I.le[i][j]) for i in range(I.m)]
    mid = {(z, w): p for (z, w, p) in I.me}
    return L.SF(I.m, le, I.E, I.F, I.s, I.t, mid, I.nn)


# ------------------------------------------------------------------------------------------- own ZZ enumeration
def preorders_mid(r):
    """all preorders on r labelled elements, as lists of up-masks"""
    pairs = [(a, b) for a in range(r) for b in range(r) if a != b]
    out = []
    for code in range(1 << len(pairs)):
        le = [1 << a for a in range(r)]
        for i, (a, b) in enumerate(pairs):
            if (code >> i) & 1:
                le[a] |= 1 << b
        ok = True
        for a in range(r):
            for b in L.bits(le[a]):
                if le[b] & ~le[a]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(le)
    return out


def full_preorders(r):
    """preorders on u = 0, middle 1..r, v = r + 1, with u <= x <= v, u < v"""
    q = r + 2
    u, v = 0, r + 1
    out = []
    for lm in preorders_mid(r):
        for Tu in range(1 << r):
            for Tv in range(1 << r):
                if Tu & Tv:
                    continue
                le = [0] * q
                le[u] = (1 << q) - 1
                le[v] = 1 << v
                for a in range(r):
                    m = (1 << v)
                    for b in L.bits(lm[a]):
                        m |= 1 << (b + 1)
                    if (Tu >> a) & 1:
                        m |= 1 << u
                    le[a + 1] = m
                for a in range(r):
                    if (Tv >> a) & 1:
                        le[v] |= 1 << (a + 1)
                ok = True
                for a in range(q):
                    for b in L.bits(le[a]):
                        if le[b] & ~le[a]:
                            ok = False
                            break
                    if not ok:
                        break
                if ok and not (le[v] >> u) & 1:
                    out.append(le)
    # remove duplicates
    seen = set()
    res = []
    for le in out:
        key = tuple(le)
        if key not in seen:
            seen.add(key)
            res.append(le)
    return res


def strict_pairs(le, q, u, v):
    out = []
    for a in range(q):
        for b in range(q):
            if a != b and (le[a] >> b) & 1 and not (le[b] >> a) & 1 and {a, b} != {u, v}:
                out.append((a, b))
    return out


# ------------------------------------------------------------------------------------------- checks
def check_sf(sf, stats, brute=True, paths=None, idesc=True, maxm_idesc=7):
    sf.check_def17()
    L.need(sf.p2(), "instance without P2")
    L.check_lemma45(sf, stats)
    allD = sf.downsets() if brute else None
    yes = sf.answer() if brute else None
    if brute and sf.s != sf.t:
        Ps = L.shortest_valid_paths(sf) if paths is None else paths
        if Ps is None:
            stats["path search over budget"] = stats.get("path search over budget", 0) + 1
            Ps = []
        else:
            L.need(bool(Ps) == yes, "L3.4(c): valid path exists iff yes-instance")
    else:
        Ps = paths or []
    for P in Ps:
        L.need(L.is_valid(sf, P), "path not valid")
        po = L.PathObj(sf, P)
        if allD is not None:
            L.check_lemma34(sf, P, po, allD)
        L.check_section4(sf, P, po, stats)
        L.theorem53(sf, P, stats)
        stats["paths checked"] = stats.get("paths checked", 0) + 1
    if brute and idesc and sf.m <= maxm_idesc:
        r = L.idesc_exact(sf, maxm=maxm_idesc)
        L.need(r == yes, "IDESC exact differs from brute force")
        stats["IDESC exact run"] = stats.get("IDESC exact run", 0) + 1
    if yes is not None:
        stats["yes" if yes else "no"] = stats.get("yes" if yes else "no", 0) + 1
    stats["max m"] = max(stats.get("max m", 0), sf.m)


def check_zz(zz, stats):
    zz.check_def16()
    sf, cinfo = L.zz_to_sf(zz)
    same = L.check_lemma32_33(zz, sf, cinfo)
    L.need(same, "L3.3: answers differ")
    check_sf(sf, stats)


def run_zz_exhaustive(r, part, parts, stats, errs):
    q = r + 2
    u, v = 0, r + 1
    pre = full_preorders(r)
    stats["preorders"] = len(pre)
    for pi, le in enumerate(pre):
        if pi % parts != part:
            continue
        sp = strict_pairs(le, q, u, v)
        for code in range(1 << len(sp)):
            R = [sp[i] for i in range(len(sp)) if (code >> i) & 1]
            zz = L.ZZ(q, le, R, u, v)
            if not zz.p2():
                stats["no P2 (skipped)"] = stats.get("no P2 (skipped)", 0) + 1
                continue
            stats["instances"] = stats.get("instances", 0) + 1
            try:
                check_zz(zz, stats)
            except L.Fail as e:
                errs.append({"le": le, "R": R, "err": str(e)})
            except Exception as e:
                errs.append({"le": le, "R": R, "err": "EXC " + repr(e), "tb": traceback.format_exc()})


def random_zz(rng, r):
    q = r + 2
    u, v = 0, r + 1
    # random preorder: random DAG on a random permutation plus ties
    perm = list(range(r))
    rng.shuffle(perm)
    pe = rng.choice([0.2, 0.35, 0.5])
    le = [1 << a for a in range(r)]
    for i in range(r):
        for j in range(i + 1, r):
            if rng.random() < pe:
                le[perm[i]] |= 1 << perm[j]
    for a in range(r):
        if rng.random() < 0.15:
            b = rng.randrange(r)
            le[a] |= 1 << b
            le[b] |= 1 << a
    changed = True
    while changed:
        changed = False
        for a in range(r):
            for b in L.bits(le[a]):
                if le[b] & ~le[a]:
                    le[a] |= le[b]
                    changed = True
    full = [0] * q
    full[u] = (1 << q) - 1
    full[v] = 1 << v
    for a in range(r):
        m = 1 << v
        for b in L.bits(le[a]):
            m |= 1 << (b + 1)
        full[a + 1] = m
    # occasionally tie a bottom element with u or a top element with v
    for a in range(r):
        if rng.random() < 0.08 and all((full[a + 1] >> (b + 1)) & 1 for b in range(r)):
            full[a + 1] |= 1 << u
        elif rng.random() < 0.08 and all((full[b + 1] >> (a + 1)) & 1 for b in range(r)):
            full[v] |= 1 << (a + 1)
    # closure again
    changed = True
    while changed:
        changed = False
        for a in range(q):
            for b in L.bits(full[a]):
                if full[b] & ~full[a]:
                    full[a] |= full[b]
                    changed = True
    if (full[v] >> u) & 1:
        return None
    sp = strict_pairs(full, q, u, v)
    pr = rng.choice([0.2, 0.3, 0.45])
    R = [e for e in sp if rng.random() < pr]
    zz = L.ZZ(q, full, R, u, v)
    # P2 repair: add a witness edge pair for every incomparable pair without one
    nb = {}
    for x in range(q):
        for y in range(x + 1, q):
            if zz.leq(x, y) or zz.leq(y, x):
                continue
            if zz.p2():
                break
            ws = [z for z in range(q) if (zz.lt(z, x) and zz.lt(z, y)) or (zz.lt(x, z) and zz.lt(y, z))]
            if not ws:
                return None
            z = rng.choice(ws)
            for a in (x, y):
                e = (z, a) if zz.lt(z, a) else (a, z)
                if {e[0], e[1]} != {u, v}:
                    zz.R.add(e)
    return zz if zz.p2() else None


def main():
    mode = sys.argv[1]
    if os.environ.get("QPR_ALLCOV"):
        L.ALLCOV[0] = True
    if os.environ.get("QPR_ADV"):
        L.ADV[0] = True
    stats = {}
    errs = []
    t0 = time.time()
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    tag = mode + "-" + "-".join(sys.argv[2:]) + ("-adv" if L.ADV[0] else "")
    if mode == "zz":
        r = int(sys.argv[2])
        part = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        parts = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        run_zz_exhaustive(r, part, parts, stats, errs)
    elif mode == "zzr":
        seed, count, lo, hi = map(int, sys.argv[2:6])
        rng = random.Random(seed)
        done = 0
        while done < count:
            zz = random_zz(rng, rng.randint(lo, hi))
            if zz is None:
                continue
            done += 1
            stats["instances"] = stats.get("instances", 0) + 1
            try:
                check_zz(zz, stats)
            except L.Fail as e:
                errs.append({"q": zz.q, "le": zz.le, "R": sorted(zz.R), "err": str(e)})
            except Exception as e:
                errs.append({"q": zz.q, "le": zz.le, "R": sorted(zz.R), "err": "EXC " + repr(e),
                             "tb": traceback.format_exc()})
    elif mode == "rsw":
        gen8 = foreign_gen8()
        seed, count, lo, hi = map(int, sys.argv[2:6])
        rng = random.Random(seed)
        for it in range(count):
            m = rng.randint(lo, hi)
            I = gen8.random_sw(rng, m, rng.randint(2, 6), rng.choice([0.15, 0.25, 0.35]), rng.choice([0.2, 0.35, 0.5]),
                               rng.choice([0.0, 0.1]), rng.choice([0.0, 0.1, 0.3]))
            sf = from_sw(I)
            stats["instances"] = stats.get("instances", 0) + 1
            try:
                check_sf(sf, stats)
            except L.Fail as e:
                errs.append({"it": it, "err": str(e)})
            except Exception as e:
                errs.append({"it": it, "err": "EXC " + repr(e), "tb": traceback.format_exc()})
    elif mode in ("rigid", "deep"):
        gen8 = foreign_gen8()
        seed, count, a, b = map(int, sys.argv[2:6])
        rng = random.Random(seed)
        done = 0
        tries = 0
        while done < count and tries < 20 * count:
            tries += 1
            if mode == "rigid":
                n = rng.randint(a, b)
                w = [rng.choice("EF") for _ in range(n)]
                if rng.random() < 0.5:
                    w = ["EF"[i % 2] for i in range(n)]
                if "E" not in w:
                    w[0] = "E"
                if "F" not in w:
                    w[-1] = "F"
                g = gen8.rigid_design(rng, "".join(w), rng.randint(1, max(2, n // 3)), rng.randint(1, max(2, n // 3)),
                                      rng.randint(1, 3), rng.randint(1, 3), pbad=rng.choice([0.3, 0.6, 1.0]),
                                      pchain=rng.choice([0.0, 0.1, 0.3]), ptie_ex=rng.choice([0.0, 0.1, 0.3]),
                                      ptie_mem=rng.choice([0.0, 0.05, 0.15]), pme=rng.choice([0.0, 0.05, 0.2]),
                                      hub=rng.random() < 0.3)
            else:
                pert = done % 4
                g = gen8.deep_design(rng, a, b, ny=b + rng.randint(0, 3), ptie_ex=0.15 if pert == 1 else 0.0,
                                     ptie_mem=0.1 if pert == 2 else 0.0, pme=0.1 if pert == 3 else 0.0,
                                     hub=rng.random() < 0.5, extra_x=rng.randint(0, 3) if pert else 0)
            if g is None:
                continue
            I, P0, info = g
            sf = from_sw(I)
            P = [(w, "E" if ty == 0 else "F") for (w, ty) in P0]
            try:
                sf.check_def17()
            except L.Fail:
                stats["designs violating Def 1.7 (skipped)"] = stats.get("designs violating Def 1.7 (skipped)", 0) + 1
                continue
            if not sf.p2():
                stats["designs without P2 (skipped)"] = stats.get("designs without P2 (skipped)", 0) + 1
                continue
            if not L.is_valid(sf, P):
                stats["planted path not valid (skipped)"] = stats.get("planted path not valid (skipped)", 0) + 1
                continue
            done += 1
            stats["instances"] = stats.get("instances", 0) + 1
            try:
                if sf.m <= 13:
                    Ps = L.shortest_valid_paths(sf, cap=50, rmax=len(P))
                    if Ps is not None:
                        L.need(Ps and len(Ps[0]) == len(P), "planted path not shortest")
                        stats["planted path shortest (own search)"] = stats.get("planted path shortest (own search)", 0) + 1
                    check_sf(sf, stats, brute=True, paths=Ps if Ps else [P])
                else:
                    # unique valid path by the generator's rigidity argument (r4-general.md Section 6); not re-proved
                    check_sf(sf, stats, brute=False, paths=[P], idesc=False)
            except L.Fail as e:
                errs.append({"it": done, "m": sf.m, "err": str(e)})
            except Exception as e:
                errs.append({"it": done, "m": sf.m, "err": "EXC " + repr(e), "tb": traceback.format_exc()})
    else:
        raise SystemExit(__doc__)
    with open(os.path.join(HERE, "runs", tag + ".txt"), "w") as f:
        f.write("%s (%.0fs, pid %d)\n" % (tag, time.time() - t0, os.getpid()))
        for k in sorted(stats, key=str):
            f.write("  %-36s %s\n" % (k, stats[k]))
        f.write("  errors: %d\n" % len(errs))
        for e in errs[:30]:
            f.write("  " + json.dumps(e, default=str) + "\n")
    print(open(os.path.join(HERE, "runs", tag + ".txt")).read())


if __name__ == "__main__":
    main()
