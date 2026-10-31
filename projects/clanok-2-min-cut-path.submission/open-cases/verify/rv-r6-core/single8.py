"""Single GDESC terms (r5-core.md 8.4, side claims; own code): does one term with few tools, anchors and flips
connect s and t?

usage: python single8.py TOOLS ANCHORS FLIPS FILES... [--log LOG] [--r5]
  --r5 : the files are r5-core JSON instances (read as data by cross_r5data.load_r5); otherwise own JSON (adv8.dump).
Enumerates both kinds, every tool set of size <= TOOLS, every flag pattern, every anchor set of size <= ANCHORS
(F-anchors for E-terms, E-anchors for F-terms, any switches), every flip set of size <= FLIPS inside U; stops at the
first connecting term and prints it.
"""
import sys
import os
import itertools
import time
from zzl import bits, popcount, term_D


def search(I, tools, anchors, flips):
    m = I.m
    sw = list(range(m))
    cnt = 0
    for t in range(0, tools + 1):
        for T in itertools.combinations(sw, t):
            for kind in ("E", "F"):
                U = 0
                for x in T:
                    U |= I.NEs[x] if kind == "E" else I.NFs[x]
                Ul = list(bits(U))
                for fl in range(1 << t):
                    Tp = [T[i] for i in range(t) if (fl >> i) & 1]
                    for a in range(0, anchors + 1):
                        for anc in itertools.combinations(sw, a):
                            am = sum(1 << x for x in anc)
                            for f in range(0, flips + 1):
                                for ph in itertools.combinations(Ul, f):
                                    Phi = sum(1 << x for x in ph)
                                    D, U2, S, G = term_D(I, kind, list(T), Tp, am, Phi)
                                    cnt += 1
                                    if I.connects(D):
                                        return (kind, T, Tp, anc, ph), cnt
    return None, cnt


def main():
    args = [a for a in sys.argv[1:]]
    logp = None
    if "--log" in args:
        i = args.index("--log")
        logp = args[i + 1]
        del args[i:i + 2]
    r5 = "--r5" in args
    if r5:
        args.remove("--r5")
    tools, anchors, flips = map(int, args[:3])
    files = args[3:]
    logf = open(logp, "a", encoding="utf-8") if logp else None

    def out(s):
        print(s, flush=True)
        if logf:
            logf.write(s + "\n")
            logf.flush()
    out("single8 tools<=%d anchors<=%d flips<=%d, %d files, pid=%d" % (tools, anchors, flips, len(files), os.getpid()))
    t0 = time.time()
    acc = 0
    for fp in files:
        if r5:
            from cross_r5data import load_r5
            I, P, d = load_r5(fp)
        else:
            from adv8 import load
            I, P = load(fp)
        res, cnt = search(I, tools, anchors, flips)
        if res:
            acc += 1
        out("  %s m=%d: %s after %d terms (%.0fs)" % (os.path.basename(fp), I.m, res, cnt, time.time() - t0))
    out("SUMMARY single8: %d of %d accepted by one term with <= %d tools, <= %d anchors, <= %d flips" % (
        acc, len(files), tools, anchors, flips))


if __name__ == "__main__":
    main()
