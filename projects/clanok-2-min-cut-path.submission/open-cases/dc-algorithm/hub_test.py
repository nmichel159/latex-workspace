"""Common-bottom (hub) 2CH + P2 instances: every E-side contains the hub node beta, so P2 holds.
Chain construction: s = c0 - c1 - ... - ck = a by F-sides, a - beta by E_w, beta - b by E_v, b = d0 - ... - dk = t by
F-sides; the F-side of v sits at position i of the c-chain, the F-side of w at position j of the d-chain.
No-instance: the c-chain needs v in F-mode, the hub exit needs v in E-mode.
Usage: python hub_test.py"""
import chlib


def hub(k, i, j):
    b = chlib.Builder()
    b.node("s")
    b.node("t")
    c = ["s"] + ["c%d" % l for l in range(1, k)] + ["a"]
    d = ["b"] + ["d%d" % l for l in range(1, k)] + ["t"]
    for l in range(1, k + 1):
        if l == i:
            b.switch("v", ["beta", "b"], [c[l - 1], c[l]])
        else:
            b.switch("f%d" % l, ["beta"], [c[l - 1], c[l]])
    for l in range(1, k + 1):
        if l == j:
            b.switch("w", ["beta", "a"], [d[l - 1], d[l]])
        else:
            b.switch("g%d" % l, ["beta"], [d[l - 1], d[l]])
    return b.inst("s", "t")


if __name__ == "__main__":
    for k in (1, 2, 3, 4):
        for i in range(1, k + 1):
            for j in range(1, k + 1):
                chlib.report("hub k=%d i=%d j=%d" % (k, i, j), hub(k, i, j))
