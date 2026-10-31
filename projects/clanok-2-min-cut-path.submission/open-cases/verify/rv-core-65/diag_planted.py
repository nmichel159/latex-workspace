"""Diagnostic: how often does the planted path stay shortest (reviewer rv-core-65)."""
import sys
import random
from collections import Counter
from planted import planted_inst

seed, count, r = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
extra = sys.argv[4:] if len(sys.argv) > 4 else []
rng = random.Random(seed)
st = Counter()
for it in range(count):
    kw = dict(r=r, n_up=rng.randint(1, 3), n_down=rng.randint(1, 3), n_free=0,
              p_rel=0.3, p_bad=0.8, p_tie=0.0, p_side=float(extra[0]) if extra else 0.1,
              p_contact=float(extra[1]) if len(extra) > 1 else 0.1, p_med=float(extra[2]) if len(extra) > 2 else 0.2)
    I = planted_inst(rng, **kw)
    I.validate()
    assert I.p2()
    ok = I.is_valid_path(I.planted)
    L = I.shortest_length()
    st["planted valid"] += ok
    st["shortest = %s" % L] += 1
print(dict(sorted(st.items())))
