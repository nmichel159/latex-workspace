"""Describe a ZZ instance: classes, middle order (covers), real edges, P2 witness kinds, solution down-sets with
generator numbers, least guess / certificate sizes.  Usage: python describe.py FILE.json [KMAX]"""
import sys
from common import zz, load, to_gc, bits, width, zz_to_sw
import mixed
import gcert
from portfolio import Masks, guess, lattice2, omega_bound


def classes(z):
    n, le = z.n, z.le
    seen = set()
    out = []
    for x in range(n):
        if x in seen:
            continue
        cl = [y for y in range(n) if le[x][y] and le[y][x]]
        seen |= set(cl)
        out.append(cl)
    return out


def describe(z, names=None, kmax=4, sols_limit=30, gc_k=None):
    nm = (lambda x: names[x]) if names else (lambda x: str(x))
    n, le = z.n, z.le
    lines = []
    cls = classes(z)
    B = [x for x in range(n) if le[x][z.u]]
    T = [x for x in range(n) if le[z.v][x]]
    lines.append("q=%d |R|=%d  B(class of u)=%s  T(class of v)=%s" % (n, len(z.R), [nm(x) for x in B],
                                                                     [nm(x) for x in T]))
    mids = [c for c in cls if c[0] not in B and c[0] not in T]
    lines.append("middle classes (%d): %s" % (len(mids), " ".join("{%s}" % ",".join(nm(x) for x in c) for c in mids)))
    cov = []
    for a in mids:
        for b in mids:
            x, y = a[0], b[0]
            if a != b and le[x][y] and not le[y][x]:
                if not any(le[x][c[0]] and le[c[0]][y] and c not in (a, b) for c in mids):
                    cov.append("%s<%s" % (nm(x), nm(y)))
    lines.append("middle covers: %s" % " ".join(cov))
    lines.append("width=%d" % width(z))
    lines.append("R: " + " ".join("%s-%s" % (nm(a), nm(b)) for a, b in z.R))
    kinds = mixed.witness_kinds(z)
    kk = {}
    for (x, y), ks in kinds.items():
        key = "".join(sorted(ks)) or "NONE"
        kk[key] = kk.get(key, 0) + 1
    lines.append("incomparable pairs by witness kinds: %s" % kk)
    try:
        oU, oL = omega_bound(z)
        lines.append("omega(U)=%d omega(Lambda)=%d" % (oU, oL))
    except Exception:
        pass
    I = mixed.Info(z)
    if n <= 40:
        sols = [D for D in zz.downsets(z) if zz.zigzag_in(z, D) is not None]
        lines.append("solution down-sets: %d" % len(sols))
        for D in sols[:sols_limit]:
            out = [nm(x) for x in range(n) if not (D >> x) & 1 and x not in T]
            ins = [nm(x) for x in range(n) if (D >> x) & 1 and x not in B]
            p = zz.zigzag_in(z, D)
            lines.append("  D: middle in D=%s, middle out=%s, g_low=%d g_up=%d, path=%s" % (
                ins, out, mixed.g_low(I, D), mixed.g_up(I, D), [nm(x) for x in p]))
    M = Masks(z)
    for k in range(kmax + 1):
        if guess(M, k) is not None:
            lines.append("least guess K = %d" % k)
            break
    else:
        lines.append("guess fails for K <= %d" % kmax)
    lines.append("LAT2: %s" % (lattice2(M) is not None))
    if gc_k is not None:
        c = gcert.certificate(to_gc(z), gc_k)
        lines.append("least GC certificate (k <= %d): %s" % (gc_k, c))
    r = zz_to_sw(z)
    lines.append("switch model: %s" % (r is not None))
    return "\n".join(lines)


if __name__ == "__main__":
    z, sw, names = load(sys.argv[1])
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    print(describe(z, names, kmax, gc_k=int(sys.argv[3]) if len(sys.argv) > 3 else None))
