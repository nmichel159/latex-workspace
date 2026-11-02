"""Instances of the earlier rounds as Inst objects: hub families, ladders, saved searches.  The old modules are imported read-only."""
import glob
import json
import os
import sys

from wd import HERE, Inst

OC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "clanok-2-min-cut-path.submission", "open-cases"))
for sub in ("dc-hardness", "dc-general", "dc-algorithm", "r4-general"):
    p = os.path.join(OC, sub)
    if p not in sys.path:
        sys.path.append(p)


def from_le(n, le, R, u, v):
    up = [0] * n
    for x in range(n):
        for y in range(n):
            if le[x][y]:
                up[x] |= 1 << y
    return Inst(n, up, [tuple(e) for e in R], u, v)


def from_zz(z):
    return from_le(z.n, z.le, z.R, z.u, z.v)


def hubs():
    import hubimp
    out = []
    for m, mp in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 3)):
        for strict in (False, True):
            out.append(("H(%d,%d)%s" % (m, mp, "po" if strict else "cl"), from_zz(hubimp.hubimp(m, mp, strict=strict)[0])))
    return out


def ladders():
    import ladder
    out = []
    for k in (2, 3, 4, 5, 6):
        for h in (False, True):
            z = ladder.ladder(k, h)[0]
            out.append(("K(%d)%s" % (k, "h" if h else ""), from_zz(z)))
    return out


def saved():
    out = []
    for f in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", "*.json"))):
        d = json.load(open(f))
        if "le" in d and "R" in d:
            out.append((os.path.basename(f), from_le(d["n"], d["le"], d["R"], d["u"], d["v"])))
    return out


def general_families():
    """X_L, Y_k, Z_k in the general switch form converted to ZZ."""
    out = []
    try:
        import xfam
        import yfam
        import zfam
        import common_r4
    except Exception as e:
        print("families not loaded:", e)
        return out
    return out
