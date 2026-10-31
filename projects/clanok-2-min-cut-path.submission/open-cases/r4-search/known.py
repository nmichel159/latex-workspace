"""Known families of ZZ + P2 instances, built with the other agents' generators (read-only imports), returned as
(name, zz.ZZ, names, 2CH form or None).

ladder K(k), KW(k)           dc-algorithm/ladder.py
hub H(m, m') (classes, po)   dc-algorithm/hubimp.py
A14                          dc-algorithm.md Section 11.6 (table)
R_L (2CH), R_L Helly form    dc-hardness/rigid_pc.py, helly2ch.add_t_to_flips
T_L (interval form) with mates 'tie' / 'oneway'; R_L 2CH form with mates   dc-general/families.py
"""
from common import zz, make_zz, sw_to_zz, zz_to_sw
import ladder as _ladder        # noqa: E402
import hubimp as _hubimp        # noqa: E402
import rigid_pc as _rigid_pc    # noqa: E402
import helly2ch as _helly2ch    # noqa: E402
import families as _families    # noqa: E402  (dc-general)


def from_gc(I):
    return make_zz(I.n, I.le, I.R, I.u, I.v)


def ladder(k, hubs=False):
    z, path, A, B = _ladder.ladder(k, hubs)
    return ("K(%d)%s" % (k, "W" if hubs else ""), z, None, None)


def hub(m, mp, strict=False):
    z, names = _hubimp.hubimp(m, mp, strict=strict)
    return ("H(%d,%d)%s" % (m, mp, "po" if strict else "cl"), z, names, None)


def a14():
    N = 7
    E = [[0, 2], [2, 3], [3, 4], [4], [2], [2, 4]]
    F = [[4], [5], [4, 5], [4, 5], [5, 6], [1, 6]]
    sw = (N, [sum(1 << x for x in e) for e in E], [sum(1 << x for x in f) for f in F], 0, 1)
    z, names = sw_to_zz(sw)
    return ("A14", z, names, sw)


def rigid_2ch(L, helly=False):
    sw = _helly2ch.add_t_to_flips(L) if helly else _rigid_pc.rigid_named(L)
    z, names = sw_to_zz(sw)
    return ("R_%d%s" % (L, "H" if helly else ""), z, names, sw)


def tic_mates(L, mates):
    I, names, info = _families.tic_rigid(L, mates)
    z = from_gc(I)
    return ("T_%d^%s" % (L, mates), z, names, None)


def rigid_mates(L, mates, helly=True):
    I, names, info = _families.rigid(L, mates, helly)
    z = from_gc(I)
    return ("RM_%d^%s%s" % (L, mates, "H" if helly else ""), z, names, None)
